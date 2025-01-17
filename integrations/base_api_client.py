from abc import ABC, abstractmethod
from dataclasses import asdict
import logging
import requests
from requests.exceptions import RequestException
from common.dataclasses import RequestData


logger = logging.getLogger(__name__)


class BaseAPIClient(ABC):

    MAX_RETRIES = 5
    BACKOFF_FACTOR = 2  # Exponential backoff factor 2 -> 2^1, 2^2, etc..

    @property
    @abstractmethod
    def BASE_URL(self) -> str:
        """Base URL for the API. Must be defined in subclasses."""
        pass

    def make_request(self, request_data:RequestData, **kwargs):

        url = f"{self.BASE_URL}/{request_data.endpoint}"
        try:
            response = requests.request(url=url, **request_data.to_request_dict(), **kwargs)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                logger.warning(f"Non-JSON response received from `{url}`")
                return response.text
        except RequestException as e:
            msg = f"Request failed: `{request_data.method}` `{url}` | Error: `{e}`",
            logger.error(msg, exc_info=True)
            raise