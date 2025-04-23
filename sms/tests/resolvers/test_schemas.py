from dataclasses import dataclass, field
from typing import Optional
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.params import ParamDict

@dataclass
class InquirySample:
    message: str
    location: ResolvedLocation
    keyword_and_language: ResolvedKeywordAndLanguage
    params: Optional[ParamDict] = field(default_factory=dict)

