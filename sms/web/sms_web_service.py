from django.contrib.sessions.backends.base import SessionBase
from cache.redis.access_patterns.web_session import WebSessionAccessPattern
from cache.redis.clients.web_session_client import WebSessionCacheClient
from .dataclasses import WebServiceData


class SMSWebService:

    def __init__(self, web_service_data: WebServiceData):
        self.query = web_service_data.query
        self.cache_client = WebSessionCacheClient(
            access_pattern = web_service_data.access_pattern,
            session = web_service_data.session
        )

    @classmethod
    def init(cls, query: str, session: SessionBase) -> "SMSWebService":
        data = WebServiceData(
            query=query,
            session=session,
            access_pattern=WebSessionAccessPattern
        )
        return cls(web_service_data=data)

    def get_phone_number(self) -> str:
        return self.cache_client.get_or_set_phone_number()