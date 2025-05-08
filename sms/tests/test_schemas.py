from dataclasses import dataclass, field
from typing import Optional
from sms.enums import ResolvedSMSType, SMSFollowUpKeywordEnum, FollowUpParams
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.params import ParamDict


@dataclass
class InquirySample:
    message: str
    location: ResolvedLocation
    keyword_and_language: ResolvedKeywordAndLanguage
    params: Optional[ParamDict] = field(default_factory=ParamDict)


@dataclass
class FollowUpSample:
    message: str
    location: None
    follow_up_enum: SMSFollowUpKeywordEnum
    params: Optional[dict[FollowUpParams.SELECTION.value, int]] = field(default_factory=dict)


@dataclass
class UnresolvedSample:
    message: str
    location: None
    sms_type: ResolvedSMSType.UNRESOLVED