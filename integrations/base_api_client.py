from abc import ABC
from dataclasses import asdict
import logging
import requests
from requests.exceptions import RequestException
from typing import Optional
from common.dataclasses import RequestData

logger = logging.getLogger(__name__)





class BaseAPIClient(ABC):

    BASE_URL = ''

    def make_request(self, request_data:RequestData, **kwargs):

        url = f"{self.BASE_URL}/{request_data.endpoint}"
        try:
            response = requests.request(url=url, request_data.to_request_dict(), **kwargs)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logger.error(e, exc_info=True)
            raise