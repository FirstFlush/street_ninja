import logging
from abc import ABC
from typing import Any
from django.contrib.gis.geos import Point
from cache.dataclasses import PhoneSessionData
from cache.redis.clients import ResourceCacheClient, PhoneSessionCacheClient
from geo.geospatial import GeospatialService
from resources.abstract_models import ResourceModel
from sms.models import SMSFollowUpInquiry, SMSInquiry
from .redis.access_patterns.base_access_patterns import AccessPatternDB
from .redis.access_patterns.phone_session import PhoneSessionAccessPattern


logger = logging.getLogger(__name__)


class BaseCacheService(ABC):

    def __init__(
            self, 
            inquiry: SMSInquiry | SMSFollowUpInquiry,
            session_cache_client: PhoneSessionCacheClient,
            resource_access_pattern: AccessPatternDB,
            session_access_pattern: PhoneSessionAccessPattern = PhoneSessionAccessPattern
    ):
        self.inquiry = inquiry
        self.session_cache_client = session_cache_client
        self.resource_access_pattern = resource_access_pattern
        self.session_access_pattern = session_access_pattern
        self.resource_cache_client = ResourceCacheClient(access_pattern=self.resource_access_pattern)

    @staticmethod
    def _get_session_cache_client(
            convo_id: int, 
            phone_session_access_pattern: PhoneSessionAccessPattern = PhoneSessionAccessPattern
    ) -> PhoneSessionCacheClient:
        redis_key = PhoneSessionCacheClient.get_redis_key(
            convo_id=convo_id,
            phone_session_access_pattern=phone_session_access_pattern
        )
        return PhoneSessionCacheClient(
            redis_key=redis_key, 
            access_pattern=phone_session_access_pattern,
        )

    def get_resources_by_proximity(self, location: Point, inquiry_params: dict[str, Any]=None) -> list[ResourceModel]:
        """
        SMS Inquiries will supply their own location
        """
        resources = self.resource_cache_client.get_or_set_db()#.closest_to(location)
        if inquiry_params:
            resources = self._filter_resources(resources=resources, inquiry_params=inquiry_params)
        return GeospatialService.sort_by_distance(resources=resources, location=location)

    def _filter_resources(self, resources:list[ResourceModel], inquiry_params:dict[str, Any]):
        return [res for res in resources if all(getattr(res, k, None) == v for k, v in inquiry_params.items())]

    def get_phone_session(self) -> PhoneSessionData | None:
        return self.session_cache_client.get_session()

    def _set_phone_session(self, session_data: PhoneSessionData) -> PhoneSessionData:
        """Returns session_data just to be consistent with get_phone_session() flow."""
        return self.session_cache_client.set_session(session_data=session_data)
