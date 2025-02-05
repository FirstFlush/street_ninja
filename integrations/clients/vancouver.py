import logging
from typing import Any
from common.dataclasses import RequestData
from .base_api_client import BaseAPIClient
from .enums import APIClientEnum, VancouverEndpointsEnum


logger = logging.getLogger(__name__)


class VancouverAPIClient(BaseAPIClient):

    endpoints = VancouverEndpointsEnum
    BASE_URL = APIClientEnum.CITY_OF_VANCOUVER.value

    @property
    def api_header(self) -> dict[str, str]:
        """
        City Of Vancouver rejects the usual 'Bearer' or 'Basic' schemes and instead opts for the keyword 'Apikey'. Bold move.
        """
        return {"Authorization": f"Apikey {self.api_key}"}

    def make_request(self, request_data:RequestData, **kwargs) -> dict[str, Any]:
        all_results = []
        limit = request_data.params.get('limit', 100) # API-enforced max of 100 records per request
        for i in range(0, 100):
            request_data.params['offset'] = i* limit
            if request_data.params['offset'] + limit >= 10000: # API specifies limit + offset must be below 10,000. If you need more records, use endpoint 'exports/'
                break
            data = super().make_request(request_data=request_data, **kwargs)
            results = data.get('results', [])
            all_results.extend(results)
            logger.info(f"offset: `{request_data.params['offset']}`, records: `{len(results)}`")
            if len(results) < 100:
                break
            
            self.jitter()

        return {"results": all_results}

    def normalize_data(self, data:dict[str, Any]) -> list[dict[str, Any]]:
        return data["results"]