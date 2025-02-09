import logging
from typing import Type
from django.conf import settings
from sms.enums import SMSKeywordEnum
from resources.abstract_models import ResourceQuerySet, ResourceModel
from cache.dataclasses import PhoneSessionData
from .base_response_service import BaseResponseService
from .dataclasses import SMSResponseData
from .respones_templates.base_response_templates import ResourceResponseTemplate
from .respones_templates.resource_templates import (
    ShelterResponseTemplate,
    FoodResponseTemplate,
)


logger = logging.getLogger(__name__)


class QuerySetResponseService(BaseResponseService):

    MAPPING = {
        SMSKeywordEnum.SHELTER: ShelterResponseTemplate,
        SMSKeywordEnum.FOOD: FoodResponseTemplate,
    }

    def __init__(self, queryset: ResourceQuerySet, offset: int):
        self.queryset = queryset
        self.offset = offset
        if isinstance(self.queryset, ResourceQuerySet) and len(self.queryset) > 0:
            self.keyword_enum = self.queryset.first().keyword_enum
        else:
            msg = f"QuerySetResponseService received invalid queryset upon instantiation. Type: `{type(self.queryset)}`, QuerySet: `{self.queryset}`"
            logger.error(msg)
            raise TypeError(msg)
        self.template_class = self._get_template_class()


    def _get_template_class(self) -> Type[ResourceResponseTemplate]:
        try:
            return self.MAPPING[self.keyword_enum]
        except KeyError as e:
            msg = f"Invalid keyword_enum `{self.keyword_enum}` passed to `{self.__class__.__name__}`'s MAPPING attribute. Error: {e}"
            logger.error(msg, exc_info=True)
            raise


    def create_response(self) -> SMSResponseData:
        indexed_queryset = self.queryset
        formatted_response = self._create_resource_response(indexed_queryset)
        truncated_response, count = self._truncate_response(formatted_response)

        return SMSResponseData(
            msg=truncated_response,
            ids=self._get_ids(indexed_queryset, count=count),
        )

    def _truncate_response(self, formatted_response: str) -> tuple[str, int]:
        if len(formatted_response) > settings.SMS_CHAR_LIMIT:
            truncated_results = formatted_response[:settings.SMS_CHAR_LIMIT].split('\n')[:-1]
            count = len(truncated_results)
            truncated_response = "\n".join(truncated_results)
        else:
            truncated_response = formatted_response
            count = len(formatted_response.split("\n"))
        return truncated_response, count


    def _create_resource_response(self, queryset:ResourceQuerySet) -> str:
        response_items = []
        for instance in queryset:
            res = self.template_class.format_response(instance=instance)
            response_items.append(res)
        return "\n".join(response_items)


    def _get_ids(self, qs:ResourceQuerySet, count: int) -> list[int]:
        return [instance.id for instance in qs[:count]]


    # def _create_resource_response(
    #         self, 
    #         instance: ResourceModel, 
    #         template_class: Type[ResourceResponseTemplate],
    #         include_optional_params: bool = True,
    # ) -> str:
    #     """Formats the SMS response based on the template rules."""
    #     data = {field: getattr(instance, field, "-") for field in template_class.always_show}
    #     extra_params = []
        
    #     if include_optional_params:
    #         for param in template_class.optional_params:
    #             value = getattr(instance, param, None)
    #             if value:
    #                 extra_params.append(f"{param}: {value}")

    #     data["extra_params"] = ", ".join(extra_params) if extra_params else ""
    #     return template_class.response_format.format(**data)