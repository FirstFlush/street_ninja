import logging
from typing import Any, Optional
from dataclasses import dataclass
from common.enums import SMSKeywordEnum, LanguageEnum
from .exc import KeywordResolverError, LocationResolutionError, ParamResolutionError
from .location.location_resolver import LocationResolver, ResolvedLocation
from .keyword_and_language_resolver import KeywordLanguageResolver, ResolvedKeywordAndLanguage
from .param_resolver import KeywordParamResolver, ParamDict


logger = logging.getLogger(__name__)


@dataclass
class ResolvedSMS:
    msg: str
    keyword_language_data: Optional[ResolvedKeywordAndLanguage] = None
    location_data: Optional[ResolvedLocation] = None
    params: Optional[ParamDict] = None


class SMSResolver:
    
    _location_resolver = LocationResolver
    _keyword_lang_resolver = KeywordLanguageResolver
    _param_resolver = KeywordParamResolver

    def __init__(self, msg:str):
        self.msg = msg


    def resolve_sms(self) -> ResolvedSMS:
        resolved_keyword_and_language = self._resolve_keyword_and_language()
        resolved_location = self._location_resolver(msg=self.msg)
        if resolved_keyword_and_language is not None:
            resolved_params = self._resolve_params(
                sms_keyword_enum=resolved_keyword_and_language.sms_keyword_enum
            )
        return ResolvedSMS(
            resolved_keyword_and_language=resolved_keyword_and_language,
            resolved_location=resolved_location,
            resolved_params=resolved_params,
        )

    def _resolve_location(self) -> ResolvedLocation | None:
        location_resolver = self._location_resolver(msg=self.msg)
        try:
            return location_resolver.resolve_location()
        except LocationResolutionError:
            return None


    def _resolve_keyword_and_language(self) -> ResolvedKeywordAndLanguage | None:
        try:
            KeywordLanguageResolver.get_keyword_and_language(msg=self.msg)
        except KeywordResolverError:
            ...

    def _resolve_params(self, sms_keyword_enum) -> ParamDict:
        try:
            return KeywordParamResolver.resolve_params(
                msg=self.msg, 
                sms_keyword_enum=sms_keyword_enum
            )
        except ParamResolutionError:
            return None