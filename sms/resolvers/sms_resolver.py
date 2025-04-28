import logging
from typing import Any, Optional
from dataclasses import dataclass
from ..enums import ResolvedSMSType
from .exc import (
    KeywordResolverError, 
    LocationResolutionError, 
    ParamResolutionError, 
    SMSResolutionError, 
    FollowUpSMSResolutionError,
)
from .location.location_resolver import LocationResolver, ResolvedLocation
from .keyword_and_language_resolver import KeywordLanguageResolver, ResolvedKeywordAndLanguage
from .params.param_resolver import ParamResolver, ParamDict
from .follow_up_resolver import ResolvedSMSFollowUp, FollowUpResolver


logger = logging.getLogger(__name__)


@dataclass
class ResolvedSMSInquiry:
    msg: str
    keyword_language_data: Optional[ResolvedKeywordAndLanguage] = None
    location_data: Optional[ResolvedLocation] = None
    params: Optional[ParamDict] = None

    @property
    def is_resolved(self) -> bool:
        return self.keyword_language_data is not None and self.location_data is not None


@dataclass
class UnresolvedSMS:
    msg: str
    location_data = None


@dataclass
class ResolvedSMS:
    resolved_sms_type: ResolvedSMSType
    phone_number: str
    data: ResolvedSMSInquiry | ResolvedSMSFollowUp | UnresolvedSMS
    message_sid: Optional[str] = None


class SMSResolver:

    _location_resolver = LocationResolver
    _keyword_lang_resolver = KeywordLanguageResolver
    _param_resolver = ParamResolver
    _follow_up_resolver = FollowUpResolver

    def __init__(self, msg:str):
        self.msg = msg

    def resolve_sms(self, message_sid: str, phone_number: str) -> ResolvedSMS:
        try:
            resolved_sms_data = self._resolve_sms()
        except Exception as e:
            logger.error(f"SMS Resolver failed for message: `{self.msg}`", exc_info=True)
            raise SMSResolutionError("SMS Resolver failed") from e
        else:
            resolved_sms_type = self._get_sms_type_enum(resolved_sms_data)
            return ResolvedSMS(
                resolved_sms_type=resolved_sms_type,
                message_sid=message_sid,
                phone_number=phone_number,
                data=resolved_sms_data,
            )

    def _get_sms_type_enum(self, resolved_sms_data: Any) -> ResolvedSMSType:
        if isinstance(resolved_sms_data, ResolvedSMSInquiry):
            return ResolvedSMSType.INQUIRY
        elif isinstance(resolved_sms_data, ResolvedSMSFollowUp):
            return ResolvedSMSType.FOLLOW_UP
        elif isinstance(resolved_sms_data, UnresolvedSMS):
            return ResolvedSMSType.UNRESOLVED
        else:
            logger.error(f"Unexpected data type for resolved_sms_data: `{resolved_sms_data}` from SMS message: `{self.msg}`", exc_info=True)
            raise SMSResolutionError(f"Unexpected data type for resolved_sms_data: `{type(resolved_sms_data)}`")
        

    def _resolve_sms(self) -> ResolvedSMSInquiry | ResolvedSMSFollowUp | UnresolvedSMS:
        resolved_keyword_and_language = self._resolve_keyword_and_language()
        if resolved_keyword_and_language is None:
            resolved_sms = self._resolve_follow_up_sms()
            if resolved_sms is None:
                resolved_sms = self._unresolved_sms()

        else:
            resolved_location = self._resolve_location()
            resolved_params = self._resolve_params(
                sms_keyword_enum=resolved_keyword_and_language.sms_keyword_enum,
            )
            resolved_sms = ResolvedSMSInquiry(
                msg=self.msg,
                keyword_language_data=resolved_keyword_and_language,
                location_data=resolved_location,
                params=resolved_params,
            )
        return resolved_sms


    def _unresolved_sms(self) -> UnresolvedSMS:
        logger.warning(f"Unresolved SMS: `{self.msg}`")
        return UnresolvedSMS(
            msg=self.msg,
        )

    def _resolve_location(self) -> ResolvedLocation | None:
        try:
            return self._location_resolver.resolve_location(msg=self.msg)
        except LocationResolutionError as e:
            logger.error(e, exc_info=True)
            raise


    def _resolve_follow_up_sms(self) -> ResolvedSMSFollowUp | None:
        try:
            follow_up_resolver = self._follow_up_resolver(self.msg).resolve_follow_up_sms()
        except FollowUpSMSResolutionError:
            return None
        else:
            if follow_up_resolver is None:
                return None
            return follow_up_resolver


    def _resolve_keyword_and_language(self) -> ResolvedKeywordAndLanguage | None:
        try:
            return KeywordLanguageResolver.get_keyword_and_language(msg=self.msg)
        except KeywordResolverError:
            return None

    def _resolve_params(self, sms_keyword_enum) -> ParamDict:
        try:
            return ParamResolver.resolve_params(
                msg=self.msg, 
                sms_keyword_enum=sms_keyword_enum
            )
        except ParamResolutionError:
            return None