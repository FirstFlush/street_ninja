import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional, Type

from django.db import transaction, IntegrityError

from common.dataclasses import RequestData
from common.enums import HttpMethodEnum
from resources.serializers.base_resource import ResourceSerializer
from resources.abstract_models.base_model import ResourceModel
from .clients import BaseAPIClient
from .clients.enums import EndpointsEnum
from .exc import IntegrationServiceError
from psycopg2.errors import UniqueViolation

logger = logging.getLogger(__name__)


@dataclass
class IntegrationServiceParams:
    api_client_class:Type[BaseAPIClient]
    endpoint_enum:EndpointsEnum
    http_method_enum:HttpMethodEnum
    api_key:str
    serializer_class:Type[ResourceSerializer]
    model_class:Optional[Type[ResourceModel]] = None
    http_params:Optional[dict[str, str] | None] = None   # GET data
    http_data:Optional[dict[str, str] | None] = None     # POST data

    @property
    def url(self) -> str:
        return f"{self.api_client_class.BASE_URL}{self.endpoint_enum.value}"


class IntegrationService:
    """
    Orchestrates the fetching, processing, and saving of resource data from various API integrations.

    This service is responsible for:
    - Fetching data from the specified APIClient at the specified endpoint, identified by an `EndpointsEnum` value.
    - Validating and deserializing the fetched data using a specified deserializer.
    - Persisting the validated data into the database using a specified model.
    """

    def __init__(
            self, 
            params:IntegrationServiceParams,
    ):
        self.saved_data = None
        self.api_client = self._build_api_client(
            api_client_class=params.api_client_class, 
            api_key=params.api_key
        )
        self.endpoint_enum = params.endpoint_enum
        self.request_data = self._build_request_data(
            http_method_enum=params.http_method_enum, 
            http_params=params.http_params, 
            http_data=params.http_data,
        )
        self.serializer_class = params.serializer_class
        self.model_class = params.model_class

    def _build_api_client(
            self, 
            api_client_class:Type[BaseAPIClient], 
            api_key:str
    ) -> BaseAPIClient:
        return api_client_class(api_key=api_key)

    def _build_request_data(
            self, 
            http_method_enum:HttpMethodEnum,
            http_params:dict[str, str] | None,
            http_data:dict[str, str] | None,
    ) -> RequestData:
        return RequestData(
            method=http_method_enum.value,
            endpoint=self.endpoint_enum.value,
            headers=self.api_client.api_header,
            params=http_params,
            data=http_data,
        )



    def fetch(self) -> Any:
        try:
            return self._fetch_data()
        except Exception as e:
            msg = f"Failed to fetch data from {self.api_client.__class__.__name__} endpoint `{self.endpoint_enum.value}`"
            raise IntegrationServiceError(msg) from e
 
    def deserialize(self, data:list[dict[str, Any]]): 
        deserializer = self._serialize_data(data=data)
        if not deserializer.is_valid():
            msg = f"Deserialization for `{self.serializer_class.__name__}` failed. deserializer.errors: `{deserializer.errors}`"
            logger.error(msg, exc_info=True)
            raise IntegrationServiceError(msg)
        return deserializer.validated_data

    def save_data(self, data: list[dict, str, Any]):
        """
        Used when performing fetch/deserialize/save flow outside of self.fetch_and_save()
        """
        self._save_data(data=data)

    def fetch_and_save(self, no_save:bool=False):
        """
        Orchestrates the process of fetching data from the API, 
        deserializing it, and saving it to the DB.

        Raises:
            IntegrationServiceError: If data fetching, deserialization, or saving to the DB fails.
        """
        data = self.fetch()
        validated_data = self.deserialize(data=data)
        self.model_class.validate_unique_key()
        data_to_save = self._normalize_data(data=validated_data)
        if no_save:
            logger.info(json.dumps(data, indent=2))
            logger.info("Skipping save...")
        else:
            try:
                self.saved_data = self._save_data(data=data_to_save)
            except Exception as e:
                msg = f"Failed to save data to DB from `{self.api_client.__class__.__name__}` endpoint `{self.endpoint_enum.value}`"
                logger.error(msg, exc_info=True)
                raise IntegrationServiceError(msg) from e

    def _fetch_data(self) -> list[dict[str, Any]]:
        data = self.api_client.make_request(request_data=self.request_data)
        return self.api_client.normalize_data(data=data)

    def _serialize_data(self, data:list[dict[str, Any]]) -> ResourceSerializer:
        return self.serializer_class(data=data, many=True)

    def _normalize_data(self, data:list[dict[str, Any]]) -> dict[str, Any]:
        return [self.model_class.normalize_data(data=record) for record in data]        

    def _prepare_bulk_operations(
            self, 
            data: list[dict[str, Any]], 
            key_to_record_map: dict[str, Any], 
            time_fetched: datetime
    ) -> tuple[list[dict[str, Any]], list[ResourceModel]]:
        """
        Prepares lists of records for bulk insertion and updates.
        """
        to_insert = []
        to_update = []

        for record in data:
            record['last_fetched'] = time_fetched
            unique_field = record[self.model_class._unique_key]
            if unique_field in key_to_record_map:
                # Check for changes and update if necessary
                existing_record = key_to_record_map[unique_field]
                updated = False
                for key, value in record.items():
                    if getattr(existing_record, key, None) != value:
                        setattr(existing_record, key, value)
                        updated = True
                if updated:
                    to_update.append(existing_record)
            else:
                # New record
                to_insert.append(self.model_class(**record))
        return to_insert, to_update

    def _get_existing_records(self, data: list[dict[str, Any]]) -> dict[Any, ResourceModel]:
        """
        Fetches existing records from the database and indexes them by their _unique_key attribute.
        Args:
            data: The list of incoming records to process.

        Returns:
            A dictionary mapping unique key values to database records.
        """
        unique_keys = [item[self.model_class._unique_key] for item in data]
        filter_kwarg = {f"{self.model_class._unique_key}__in": unique_keys}
        existing_records = self.model_class.objects.filter(**filter_kwarg)
        key_to_record_map = {getattr(record, self.model_class._unique_key): record for record in existing_records}
        return key_to_record_map


    def _create(self, data: list[dict[str, Any]]):
        try:
            self.model_class.objects.bulk_create(data)
        except IntegrityError:
            for resource in data:
                try:
                    self.model_class.objects.create(**resource)
                except IntegrityError:
                    logger.warning(f"Resource `{resource.keyword}: {resource.resource_name}` already exists. Skipping...")

    def _update(self, data: list[ResourceModel]):

        update_fields = [field.name for field in self.model_class._meta.fields if field.name != "id"]
        try:
            with transaction.atomic():
                self.model_class.objects.bulk_update(data, fields=update_fields)
        except IntegrityError:
            for resource in data:
                try:
                    with transaction.atomic():
                        resource.save()
                except IntegrityError:
                    logger.warning(f"Resource `{resource._keyword_enum}: {resource.resource_name}` already exists. Skipping...")
                    continue


    def _save_data(self, data: list[dict[str, Any]]):
        """
        Saves data to the database, performing inserts for new records and updates for existing ones.
        """
        key_to_record_map = self._get_existing_records(data=data)        
        time_fetched = datetime.now(timezone.utc)
        to_insert, to_update = self._prepare_bulk_operations(
            data=data,
            key_to_record_map=key_to_record_map,
            time_fetched=time_fetched,
        )
        # with transaction.atomic():
        if to_insert:
            self._create(data=to_insert)
            # self.model_class.objects.bulk_create(to_insert)
        if to_update:
            self._update(data=to_update)
            # update_fields = list(data[0].keys())  # Explicitly track fields to update
            # self.model_class.objects.bulk_update(to_update, fields=update_fields)

        logger.info(f"Inserted `{len(to_insert)}` new records and synced `{len(to_update)}` existing records.")
        return to_insert + to_update
































    # def fetch_and_save(self, no_save:bool=False):
    #     """
    #     Orchestrates the process of fetching data from the API, 
    #     deserializing it, and saving it to the DB.

    #     Raises:
    #         IntegrationServiceError: If data fetching, deserialization, or saving to the DB fails.
    #     """
    #     # Fetch
    #     try:
    #         data = self._fetch_data()
    #     except Exception as e:
    #         msg = f"Failed to fetch data from {self.api_client.__class__.__name__} endpoint `{self.endpoint_enum.value}`"
    #         raise IntegrationServiceError(msg) from e

    #     # Deserialize
    #     deserializer = self._serialize_data(data=data)
    #     if not deserializer.is_valid():
    #         msg = f"Deserialization for `{self.serializer_class.__name__}` failed. deserializer.errors: `{deserializer.errors}`"
    #         logger.error(msg, exc_info=True)
    #         raise IntegrationServiceError(msg)

    #     self.model_class.validate_unique_key()
    #     data_to_save = self._normalize_data(data=deserializer.validated_data)
    #     if no_save:
    #         logger.info(json.dumps(data, indent=2))
    #         logger.info("Skipping save...")
    #     else:
    #         try:
    #             self.saved_data = self._save_data(data=data_to_save)
    #         except Exception as e:
    #             msg = f"Failed to save data to DB from `{self.api_client.__class__.__name__}` endpoint `{self.endpoint_enum.value}`"
    #             logger.error(msg, exc_info=True)
    #             raise IntegrationServiceError(msg) from e
