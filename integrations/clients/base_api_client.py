from abc import ABC
import logging
import requests
from requests.exceptions import RequestException
from typing import Any
from common.base_enum import StreetNinjaEnum
from common.dataclasses import RequestData


logger = logging.getLogger(__name__)


class BaseAPIClient(ABC):

    MAX_RETRIES = 5
    BACKOFF_FACTOR = 2  # Exponential backoff factor 2 -> 2^1, 2^2, etc..
    BASE_URL = ""

    @property
    def api_header(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}
    
    def __init__(self, api_key:str|None=None):
        self.api_key = api_key

    def url(self, endpoint: str) -> str:
        if isinstance(endpoint, StreetNinjaEnum):
            endpoint = endpoint.value
        elif not isinstance(endpoint, str):
            msg = f"endpoint argument must be a string, not type `{type(endpoint)}`"
            logger.error(msg, exc_info=True)
            raise TypeError(msg)
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        return f"{self.BASE_URL}{endpoint}"

    def make_request(self, request_data:RequestData, **kwargs) -> dict[str, Any]:
        url = self.url(request_data.endpoint)
        try:
            response = requests.request(url=url, **request_data.to_request_dict(), **kwargs)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                logger.warning(f"Non-JSON response received from `{url}`")
                return {"data": response.text}
        except RequestException as e:
            msg = f"Request failed: `{request_data.method}` `{url}` | Error: `{e}`",
            logger.error(msg, exc_info=True)
            raise





    # @property
    # @abstractmethod
    # def BASE_URL(self) -> str:
    #     """Base URL for the API. Must be defined in subclasses."""
    #     pass