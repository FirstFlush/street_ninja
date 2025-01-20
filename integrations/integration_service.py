import logging
from dataclasses import dataclass
from typing import Type
from common.dataclasses import RequestData
from common.enums import HttpMethodEnum
from resources.serializers import ResourceSerializer
from resources.base_model import ResourceModel
from .enums import EndpointsEnum
from .clients import BaseAPIClient


# @dataclass
# class IntegrationServiceParams:
#     api_client
#     endpoint_enum
#     request_type_enum
#     api_key
#     serializer
#     model



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
            api_client_class:Type[BaseAPIClient], 
            endpoint_enum:EndpointsEnum,
            http_method_enum:HttpMethodEnum,
            api_key:str, 
            serializer:Type[ResourceSerializer],
            model:Type[ResourceModel],
            params: dict[str, str] | None = None,   # GET params
            data: dict[str, str] | None = None,     # POST data
    ):
        self.api_client = self._build_api_client(api_client_class, api_key)
        self.endpoint_enum = endpoint_enum
        self.request_data = self._build_request_data(http_method_enum, params, data)
        self.serializer = serializer
        self.model = model


    def _build_api_client(self, api_client_class:Type[BaseAPIClient], api_key:str) -> BaseAPIClient:
        return api_client_class(api_key=api_key)


    def _build_request_data(
            self, 
            http_method_enum:HttpMethodEnum,
            params:dict[str, str] | None,
            data:dict[str, str] | None,
    ) -> RequestData:
        return RequestData(
            method=http_method_enum.value,
            endpoint=self.endpoint_enum.value,
            headers=self.api_client.api_header,
            params=params,
            data=data,
        )


    def _fetch_data(self):
        self.api_client.make_request()

    def _serialize_data(self):
        ...


    def _save_data(self):
        ...