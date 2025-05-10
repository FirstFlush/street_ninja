from dataclasses import dataclass
from cache.redis.access_patterns.web_session import WebSessionAccessPattern
from typing import Type
from django.contrib.sessions.backends.base import SessionBase


@dataclass
class WebServiceData:

    session: SessionBase
    access_pattern: Type[WebSessionAccessPattern]
    query: str