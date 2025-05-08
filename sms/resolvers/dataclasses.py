from dataclasses import dataclass, field
from typing import Any, Optional
from ..enums import ResolvedSMSType, SMSFollowUpKeywordEnum
from .keyword_and_language_resolver import ResolvedKeywordAndLanguage
from .location.location_resolver import ResolvedLocation
from .params.param_resolver import ParamDict


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
class ResolvedSMSFollowUp:
    msg: str
    # follow_up_keyword_enum: Optional[SMSFollowUpKeywordEnum] = None
    follow_up_keyword_enum: SMSFollowUpKeywordEnum
    follow_up_params: Optional[dict[str, Any]] = field(default_factory=dict)


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
