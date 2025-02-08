from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from common.enums import SMSKeywordEnum


@dataclass
class PhoneSessionData:
    """Ensures phone session data is always structured correctly."""

    last_updated: datetime
    keyword: str
    batch_ids: List[int]
    offset: int

    def __post_init__(self):
        """Validate that keyword is a valid SMSKeywordEnum value (or None)."""
        if self.keyword and self.keyword not in SMSKeywordEnum.values:
            raise ValueError(f"Invalid keyword `{self.keyword}`. Must be one of: {SMSKeywordEnum.values}")
