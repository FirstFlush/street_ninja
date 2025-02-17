import logging
from .response_builders import QuerySetResultBuilder
from .dataclasses import InquiryResponseContext, SMSInquiryResponseData


logger = logging.getLogger(__name__)


class InquiryResponseHandler:

    def __init__(self, context: InquiryResponseContext):
        self.instance = context.instance
        self.caching_service = context.caching_service
        self.queryset = context.queryset
        self.offset = 0
        self.queryset_result_builder = self._queryset_result_builder()

    def _queryset_result_builder(self) -> QuerySetResultBuilder:
        return QuerySetResultBuilder(
            queryset=self.queryset,
            offset=self.offset,
            params=self.instance.params if self.instance.params else None,
        )


    def build_response_data(self) -> SMSInquiryResponseData:
        session_data = self.caching_service.get_phone_session()
        response_data = self.queryset_result_builder.create_response_data()
        if session_data:
            session_data = self.caching_service.update_phone_session(
                session_data=session_data,
                ids=response_data.ids,
            )
        else:
            session_data = self.caching_service.create_phone_session(
                ids=response_data.ids,
                params=self.instance.params if self.instance.params else None,
            )
        return response_data

