import logging
from .base_handler import FollowUpHandlerWithParams
from street_ninja_server.global_mappings import SMS_KEYWORD_ENUM_TO_INFO_TEMPLATE
from ..dataclasses import FollowUpContext, SMSFollowUpResponseData
from ..response_templates.info_templates import InfoTemplate
from cache.dataclasses import PhoneSessionData


logger = logging.getLogger(__name__)


class InfoHandler(FollowUpHandlerWithParams):

    MAPPING = SMS_KEYWORD_ENUM_TO_INFO_TEMPLATE

    def __init__(self, context: FollowUpContext):
        super().__init__(context=context)
        self.info_template = self._info_template()
    
    def _create_response_msg(self) -> str:
        return self.info_template.display_info()


    def _info_template(self) -> InfoTemplate:
        try:
            return self.MAPPING[self.sms_inquiry.keyword_enum](self.resource)
        except KeyError:
            msg = f"InfoHandler received invalid SMSKeywordEnum: `{self.sms_inquiry.keyword_enum}`. Can not fetch InfoTemplate!"
            logger.error(msg)
            raise


    def build_response_data(self) -> SMSFollowUpResponseData:
        return SMSFollowUpResponseData(
            msg=self._create_response_msg(),
            template=self.info_template,
            resource=self.resource,
        )