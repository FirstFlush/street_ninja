import logging
from typing import Type, Any
from django.conf import settings
from sms.enums import SMSKeywordEnum
from resources.abstract_models import ResourceQuerySet
from ..dataclasses import SMSInquiryResponseData, SMSFollowUpResponseData
from ..response_templates.base_response_templates import QuerySetResponseTemplate
from ..response_templates.queryset_templates import (
    ShelterResponseTemplate,
    FoodResponseTemplate,
    WaterResponseTemplate,
    ToiletResponseTemplate,
    WifiResponseTemplate,
)


logger = logging.getLogger(__name__)


class QuerySetResultBuilder:

    MAPPING = {
        SMSKeywordEnum.SHELTER: ShelterResponseTemplate,
        SMSKeywordEnum.FOOD: FoodResponseTemplate,
        SMSKeywordEnum.TOILET: ToiletResponseTemplate,
        SMSKeywordEnum.WATER: WaterResponseTemplate,
        SMSKeywordEnum.WIFI: WifiResponseTemplate,
    }

    def __init__(self, queryset: ResourceQuerySet, offset: int, params: dict[str, Any ] | None = None):
        self.queryset = queryset
        self.offset = offset
        self.params = params
        if isinstance(self.queryset, ResourceQuerySet) and len(self.queryset) > 0:
            self.keyword_enum = self.queryset.first().keyword_enum
        else:
            msg = f"{self.__class__.__name__} received invalid queryset upon instantiation. Type: `{self.queryset.__class__.__name__}`, QuerySet: `{self.queryset}`"
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
        indexed_queryset = self.queryset[self.offset:]
        formatted_response = self._create_queryset_response(indexed_queryset)
        truncated_response, count = self._truncate_response(formatted_response)
        return SMSFollowUpResponseData(
            msg=truncated_response,
            ids=self._get_ids(indexed_queryset, count=count),
            template=self.template,
        )


    def _create_response_data(self) -> SMSInquiryResponseData:
        indexed_queryset = self.queryset[self.offset:]
        formatted_response = self._create_queryset_response(indexed_queryset)
        truncated_response, count = self._truncate_response(formatted_response)
        return SMSInquiryResponseData(
            msg=truncated_response,
            ids=self._get_ids(indexed_queryset, count=count),
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


    def _create_queryset_response(self, queryset:ResourceQuerySet) -> str:
        response_items = []
        for instance in queryset:
            res = self.template.format_result(instance=instance)
            response_items.append(res)
        # print(template.TITLE + "\n" + "\n".join(response_items))
        return "\n".join(response_items)


    def _get_ids(self, qs:ResourceQuerySet, count: int) -> list[int]:
        return [instance.id for instance in qs[:count]]

