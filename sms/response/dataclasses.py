from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class BaseResponseData:
    msg: str

@dataclass
class SMSInquiryResponseData(BaseResponseData):
    ids: list[int]

    @property
    def offset(self) -> int:
        return len(self.ids)

@dataclass
class SMSFollowUpResponseData(BaseResponseData):
    ids: Optional[list[int]] = None
    directions_text: Optional[str] = None 
    # params: Optional[dict[str, Any]] = None