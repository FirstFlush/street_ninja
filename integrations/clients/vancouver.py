from ..base_api_client import BaseAPIClient
from ..enums import BaseURLEnum, VancouverEndpointsEnum


class VancouverAPIClient(BaseAPIClient):

    endpoints = VancouverEndpointsEnum
    BASE_URL = BaseURLEnum.CITY_OF_VANCOUVER.value

    @property
    def api_header(self) -> dict[str, str]:
        """City Of Vancouver rejects the 'Bearer' convention and instead uses the keyword 'Apikey'. Bold move."""
        return {"Authorization": f"Apikey {self.api_key}"}
