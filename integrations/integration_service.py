import logging
from dataclasses import dataclass
from typing import Any, Optional, Type
from common.dataclasses import RequestData
from common.enums import HttpMethodEnum
from resources.serializers import ResourceSerializer
from resources.base_model import ResourceModel
from .clients import BaseAPIClient
from .enums import EndpointsEnum
from .exc import IntegrationServiceError


logger = logging.getLogger(__name__)


@dataclass
class IntegrationServiceParams:
    api_client_class:Type[BaseAPIClient]
    endpoint_enum:EndpointsEnum
    http_method_enum:HttpMethodEnum
    api_key:str
    serializer_class:Type[ResourceSerializer]
    model_class:Type[ResourceModel]
    http_params:Optional[dict[str, str] | None] = None   # GET data
    http_data:Optional[dict[str, str] | None] = None     # POST data


class IntegrationService:
    """
    Orchestrates the fetching, processing, and saving of external data from various API integrations.

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

    def _build_api_client(self, api_client_class:Type[BaseAPIClient], api_key:str) -> BaseAPIClient:
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
            http_params=http_params,
            http_data=http_data,
        )

    def fetch_and_save(self):
        """
        Orchestrates the process of fetching data from the API, 
        deserializing it, and saving it to the DB.

        Raises:
            IntegrationServiceError: If data fetching, deserialization, or saving to the DB fails.
        """
        # Fetch
        try:
            data = self._fetch_data()
        except Exception as e:
            msg = f"Failed to fetch data from {self.api_client.__class__.__name__} endpoint `{self.endpoint_enum.value}`"
            raise IntegrationServiceError(msg) from e
        
        # Deserialize
        deserializer = self._serialize_data(data=data)
        if not deserializer.is_valid():
            msg = f"Deserialization for `{self.serializer_class.__name__}` failed"
            logger.error(msg, exc_info=True)
            raise IntegrationServiceError(msg)
        
        # Save to DB
        try:
            self.saved_data = self._save_data(data=deserializer.validated_data)
        except Exception as e:
            msg = f"Failed to save data to DB from `{self.api_client.__class__.__name__}` endpoint `{self.endpoint_enum.value}`"
            logger.error(msg, exc_info=True)
            raise IntegrationServiceError(msg) from e
        

    def _fetch_data(self) -> list[dict[str, Any]]:
        data = self.api_client.make_request(request_data=self.request_data)
        return self.api_client.normalize_data(data=data)

    def _serialize_data(self, data:list[dict[str, Any]]) -> ResourceSerializer:
        return self.serializer_class(data=data, many=True)

    def _save_data(self, data):
        raise ValueError()
        print(data)
        print(type(data))
        print(len(data))