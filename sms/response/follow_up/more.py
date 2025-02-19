import logging
from .base_handler import BaseFollowUpHandler
from cache.dataclasses import PhoneSessionData
from resources.abstract_models import ResourceModel
from sms.response.response_builders.queryset_result_builder import QuerySetResultBuilder
from sms.response.dataclasses import FollowUpContext, SMSFollowUpResponseData


logger = logging.getLogger(__name__)


class More(BaseFollowUpHandler):

    END_OF_RESULTS = "End of results, sorry.\n\nPlease Call 211 if you need more immediate assistance."

    def __init__(self, context: FollowUpContext):
        self.sms_inquiry = context.sms_inquiry
        self.current_session = context.current_session
        self.caching_service = context.caching_service
        self.resources = self._resources()
        self.response_builder = self._response_builder()

    def build_response_data(self) -> SMSFollowUpResponseData:
        response_data = self.response_builder.create_response_data(more=True)
        if len(response_data.ids) == 0:
            response_data.msg = self.END_OF_RESULTS
        return response_data

    def _response_builder(self) -> QuerySetResultBuilder:
        return QuerySetResultBuilder(
            resources=self.resources,
            offset=self.current_session.offset,
        )

    def update_session(self, ids:list[int]) -> PhoneSessionData:
        new_session = self.caching_service.update_phone_session(session_data=self.current_session, ids=ids)
        return new_session

    def _resources(self) -> list[ResourceModel]:
        resources = self.caching_service.get_resources_by_proximity(location=self.sms_inquiry.location)
        if len(resources) == 0:
            logger.warning(f"{self.__class__.__name__} received empty queryset: {resources}")
        return resources
