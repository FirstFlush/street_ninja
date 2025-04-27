import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any
from sms.enums import SMSKeywordEnum


logger = logging.getLogger(__name__)


@dataclass
class PhoneSessionData:
    """Ensures phone session data is always structured correctly."""

    last_updated: datetime
    keyword: str
    inquiry_id: int
    ids: list[int]
    resource_params: Optional[dict[str, Any]] = None

    @property
    def offset(self) -> int:
        return len(self.ids)

    @property
    def keyword_enum(self) -> SMSKeywordEnum:
        try:
            return SMSKeywordEnum(self.keyword)
        except ValueError:
            msg = f"Can not create SMSKeywordEnum with invalid PhoneSessionData.keyword : `{self.keyword}`"
            logger.error(msg)
            raise

    def __post_init__(self):
        """Validate that keyword is a valid SMSKeywordEnum value (or None)."""
        if self.keyword and self.keyword not in SMSKeywordEnum.values:
            raise ValueError(f"Invalid keyword `{self.keyword}`. Must be one of: {SMSKeywordEnum.values}")

