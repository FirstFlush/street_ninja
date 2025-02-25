import logging
from typing import Type, Any
from django.conf import settings
from resources.abstract_models import ResourceModel
from street_ninja_server.global_mappings import SMS_KEYWORD_ENUM_TO_RESPONSE_TEMPLATE
from ..dataclasses import SMSInquiryResponseData, SMSFollowUpResponseData
from ..response_templates.queryset_templates import QuerySetResponseTemplate


logger = logging.getLogger(__name__)


class QuerySetResultBuilder:

    MAPPING = SMS_KEYWORD_ENUM_TO_RESPONSE_TEMPLATE

    def __init__(self, resources: list[ResourceModel], offset: int, params: dict[str, Any ] | None = None):
        self.resources = resources
        self.offset = offset
        self.params = params
        if isinstance(self.resources, list) and all(isinstance(i, ResourceModel) for i in self.resources) and len(self.resources) > 0:
            self.keyword_enum = self.resources[0].keyword_enum
        else:
            msg = f"{self.__class__.__name__} received invalid resources upon instantiation. Type: `{self.resources.__class__.__name__}`, resources: `{self.resources}`"
            logger.error(msg)
            raise TypeError(msg)
        template_class = self._get_template_class()
        self.template = template_class(params=params)

    def _get_template_class(self) -> Type[QuerySetResponseTemplate]:
        try:
            return self.MAPPING[self.keyword_enum]
        except KeyError as e:
            msg = f"Invalid keyword_enum `{self.keyword_enum}` passed to `{self.__class__.__name__}`'s MAPPING attribute. Error: {e}"
            logger.error(msg, exc_info=True)
            raise

    def create_response_data(self, more: bool=False, verbose: bool=True) -> SMSInquiryResponseData:
        if more:
            response_data = self._create_response_data_more()
        else:
            response_data = self._create_response_data()
        logger.info(f"Successfully created `{response_data.__class__.__name__}`")
        if verbose:
            logger.info(f"{response_data}")
        return response_data

    def _create_response_data_more(self) -> SMSFollowUpResponseData:
        indexed_queryset = self.resources[self.offset:]
        formatted_response = self._create_queryset_response(indexed_queryset)
        truncated_response, count = self._truncate_response(formatted_response)
        return SMSFollowUpResponseData(
            msg=truncated_response,
            ids=self._get_ids(indexed_queryset, count=count),
            template=self.template,
        )

    def _create_response_data(self) -> SMSInquiryResponseData:
        indexed_resources = self.resources[self.offset:]
        formatted_response = self._create_queryset_response(indexed_resources)
        truncated_response, count = self._truncate_response(formatted_response)
        return SMSInquiryResponseData(
            msg=truncated_response,
            ids=self._get_ids(indexed_resources, count=count),
            template=self.template,
        )

    def _truncate_response(self, formatted_response: str) -> tuple[str, int]:
        logger.info(f"SMS Character limit: `{settings.SMS_CHAR_LIMIT}`")
        if len(formatted_response) > settings.SMS_CHAR_LIMIT:
            truncated_results = formatted_response[:settings.SMS_CHAR_LIMIT].split('\n')[:-1]
            count = len(truncated_results)
            truncated_response = "\n".join(truncated_results)
        else:
            truncated_response = formatted_response
            count = len(truncated_response.split("\n"))
        return truncated_response, count

    def _get_index(self, i:int) -> int:
        """
        Example SMS response:
        🏠 SHELTERS
        1) 0.2km The Haven (Men)
        2) 0.2km Anchor of Hope (Adults - all genders)
        3) 0.2km Lookout Downtown (Adults - all genders)
        
        This method generates the index number for each resource shown to the user.
        Offset is used because if the user requests 'MORE', 
        the indexing must start from where the previous message left off.
        """
        return i + self.offset + 1

    def _create_queryset_response(self, resources: list[ResourceModel]) -> str:
        response_items = []
        for i, instance in enumerate(resources):
            res = f"{self._get_index(i)}) {self.template.format_result(instance=instance)}"
            response_items.append(res)
        return "\n".join(response_items)

    def _get_ids(self, resources:list[ResourceModel], count: int) -> list[int]:
        return [instance.id for instance in resources[:count]]

