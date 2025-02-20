from dataclasses import dataclass
from cache.redis.access_patterns import WebSessionAccessPattern
from typing import Type
from django.contrib.sessions.backends.base import SessionBase


@dataclass
class WebServiceData:

    session: SessionBase
    access_pattern: Type[WebSessionAccessPattern]
    query: str