from typing import Any
from .base_api_client import BaseAPIClient
from .enums import APIClientEnum, OpenRouteServiceEndpointsEnum


class OpenRouteServiceAPIClient(BaseAPIClient):

    endpoints = OpenRouteServiceEndpointsEnum
    BASE_URL = APIClientEnum.OPEN_ROUTE_SERVICE.value

    @property
    def api_header(self) -> dict[str, str]:
        return {"Authorization": f"{self.api_key}"}

    def normalize_data(self, data: dict[str, Any]) -> list[str]:
        # with open("bleh.json", "w") as file:
        #     file.write(json.dumps(data))
        steps = data["features"][0]["properties"]["segments"][0]["steps"]
        directions_data = [{"instruction": step["instruction"], "distance": int(
            round(step["distance"], 0))} for step in steps]

        return directions_data