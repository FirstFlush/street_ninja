from .base_api_client import BaseAPIClient
from ..enums import APIClientEnum, WigleEndpointsEnum


class WigleAPIClient(BaseAPIClient):

    endpoints = WigleEndpointsEnum
    BASE_URL = APIClientEnum.WIGLE.value

    @property
    def api_header(self) -> dict[str, str]:
        return {"Authorization": f"Basic {self.api_key}"}
