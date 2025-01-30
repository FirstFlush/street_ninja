import logging
from typing import Any
from dataclasses import dataclass
from common.enums import SMSKeywordEnum, LanguageEnum
from .location.location_resolver import LocationResolver, ResolvedLocation
from .keyword_and_language_resolver import KeywordLanguageResolver
from .param_resolver import KeywordParamResolver


logger = logging.getLogger(__name__)


@dataclass
class ResolvedSMS:
    location: ResolvedLocation
    params: dict[str, Any]
    keyword_enum: SMSKeywordEnum
    language: LanguageEnum


class SMSResolver:
    
    _location_resolver = LocationResolver
    _keyword_lang_resolver = KeywordLanguageResolver
    _param_resolver = KeywordParamResolver

    def __init__(self, msg:str):
        self.msg = msg


    def resolve_sms(self) -> ResolvedSMS:
        resolved_location = self._resolve_location()    


    def _resolve_location(self) -> ResolvedLocation:
        location_resolver = self._location_resolver(msg=self.msg)
        return location_resolver.resolve_location()

    def _resolve_keyword_and_language(self):
        ...
    def _resolve_params(self):
        ...