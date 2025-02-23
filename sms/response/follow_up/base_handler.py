import logging
from abc import ABC, abstractmethod
from cache.dataclasses import PhoneSessionData
from resources.abstract_models import ResourceModel
from sms.response.dataclasses import FollowUpContext, SMSFollowUpResponseData
from sms.enums import FollowUpParams
from sms.models import SMSFollowUpInquiry
from ..exc import SendHelpError


logger = logging.getLogger(__name__)


class BaseFollowUpHandler(ABC):

    def __init__(self, context: FollowUpContext):
        self.sms_inquiry = context.sms_inquiry
        self.current_session = context.current_session
        self.caching_service = context.caching_service

    @abstractmethod
    def build_response_data(self) -> SMSFollowUpResponseData:
        ...


class FollowUpHandlerWithParams(BaseFollowUpHandler):

    def __init__(self, context: FollowUpContext):
        super().__init__(context=context)
        self.follow_up_inquiry = context.follow_up_inquiry
        if not isinstance(self.follow_up_inquiry, SMSFollowUpInquiry):
            msg = f"{self.__class__.__name__} received invalid SMSFollowUpInquiry: `{context.follow_up_inquiry}` from FollowUpContext: `{context.__dict__}`"
            logger.error(msg)
            raise TypeError(msg)
        self.selection = self._selection()
        self.resource = self._get_resource()

    def _selection(self) -> int:
        """Returns the user's selection sent with the INFO request."""
        try:
            return self.follow_up_inquiry.params[FollowUpParams.SELECTION.value]
        except KeyError:
            msg = f"SMSFollowUpInquiry #`{self.follow_up_inquiry.id}` params does not contain `{FollowUpParams.SELECTION.value}` key: `{self.follow_up_inquiry.params}`"
            logger.error(msg)
            raise SendHelpError(msg)
        except TypeError:
            msg = f"SMSFollowUpInquiry #`{self.follow_up_inquiry.id}` params invalid type: `{type(self.follow_up_inquiry.params)}`"
            logger.error(msg)
            raise SendHelpError(msg)

    def _get_resource_id(self) -> int:
        try:
            return self.current_session.ids[self.selection - 1]
        except IndexError:
            msg = f"Invalid index position for selection of `{self.selection}` and ID list with length of `{len(self.current_session.ids)}`"
            logger.error(msg)
            raise SendHelpError(msg)

    def _get_resource(self) -> ResourceModel:
        id = self._get_resource_id()
        resources = self.caching_service.resource_cache_client.get_or_set_db(
            **(self.current_session.resource_params or {})
        )
        resource = next((r for r in resources if r.id == id), None)
        if resource is None:
            msg = f"{self.__class__.__name__} can not resolve resource model in list of ResourceModel objects `{resources}` with id of `{id}`."
            logger.error(msg)
            raise ResourceModel.DoesNotExist(msg)
        return resource

    def update_session(self) -> PhoneSessionData:
        new_session = self.caching_service.update_phone_session(
            session_data=self.current_session)
        return new_session
