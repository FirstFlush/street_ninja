from dataclasses import dataclass
import logging
from typing import Any, Optional
from .base_resolver import BaseKeywordResolver
from .exc import FollowUpSMSResolutionError
from ..enums import ResolvedSMSType
from ..enums import SMSFollowUpKeywordEnum


logger = logging.getLogger(__name__)


@dataclass
class ResolvedSMSFollowUp:
    msg: str
    follow_up_keyword_enum: Optional[SMSFollowUpKeywordEnum] = None
    follow_up_params: Optional[dict[str, Any]] = None


class FollowUpResolver(BaseKeywordResolver):

    def __init__(self, msg: str):
        self.msg = msg
        self.tokens = self._tokenize_msg(msg=self.msg)
        self.keyword_set = set(SMSFollowUpKeywordEnum.values)

    def resolve_follow_up_sms(self) -> ResolvedSMSFollowUp | None:
        keyword_enum = self._resolve_keyword()
        if keyword_enum:
            params = self._resolve_params()
            return ResolvedSMSFollowUp(
                msg=self.msg,
                follow_up_keyword_enum=keyword_enum,
                follow_up_params=params,
            )
        else:
            logger.warning("Failed to resolve FollowUp keyword...")
            None

    def _resolve_keyword(self) -> SMSFollowUpKeywordEnum | None:
        for token in self.tokens:
            if self._try_token(token):
                keyword = SMSFollowUpKeywordEnum(token)
                logger.info(f"Resolved follow-up keyword: `{keyword.value.upper()}`")
                return SMSFollowUpKeywordEnum(token)
        return None

    def _resolve_params(self) -> dict[str, Any]:
        """Currently params are only an int that can be passed in on 
        "INFO" and "DIRECTIONS" keywords. Future params may be added,
        so params dict keys can change. Currently it returns an int
        value with the key 'param'
        """
        params = {}
        for token in self.tokens:
            if self._try_param(token):
                params['param'] = int(token)
                break
        return params

    def _try_param(self, token: str) -> bool:
        """
        Currently params would just be integers. 
        So this method will be kept simple and only 
        check the tokens for the first integer.
        """
        return token.isdecimal()


    def _try_token(self, token:str) -> bool:
        return token in self.keyword_set