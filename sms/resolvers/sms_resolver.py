import logging
from typing import Any
from dataclasses import dataclass
from common.enums import SMSKeywordEnum, LanguageEnum
from .location.location_resolver import LocationResolver
from .keyword_and_language_resolver import KeywordLanguageResolver
from .param_resolver import KeywordParamResolver


logger = logging.getLogger(__name__)


@dataclass
class ResolvedSMS:
    location: str
    params: dict[str, Any]
    keyword_enum: SMSKeywordEnum
    language: LanguageEnum


class SMSResolver:
    
    _address_resolver = LocationResolver
    _keyword_lang_resolver = KeywordLanguageResolver
    _param_resolver = KeywordParamResolver

    def __init__(self, inquiry:str):
        self.inquiry = inquiry


    def resolve_sms(self) -> ResolvedSMS:
        ...

