from typing import Any
from .base_api_client import BaseAPIClient
from .enums import APIClientEnum, VancouverEndpointsEnum


class VancouverAPIClient(BaseAPIClient):

    endpoints = VancouverEndpointsEnum
    BASE_URL = APIClientEnum.CITY_OF_VANCOUVER.value

    @property
    def api_header(self) -> dict[str, str]:
        """City Of Vancouver rejects the 'Bearer' convention and instead uses the keyword 'Apikey'. Bold move."""
        return {"Authorization": f"Apikey {self.api_key}"}

    def normalize_data(self, data:dict[str, Any]) -> list[dict[str, Any]]:
        return data['results']