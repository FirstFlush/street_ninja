import logging
from sms.enums import SMSKeywordEnum
from resources.abstract_models import ResourceQuerySet, ResourceModel
from .base_response_service import BaseResponseService
from .respones_templates.base_response_templates import ResourceResponseTemplate
from .respones_templates.resources import (
    ShelterResponseTemplate,
    FoodResponseTemplate,
)


logger = logging.getLogger(__name__)


class QuerySetResponseService(BaseResponseService):

    MAPPING = {
        SMSKeywordEnum.SHELTER : ShelterResponseTemplate,
        SMSKeywordEnum.FOOD : FoodResponseTemplate,
    }

    def __init__(self, queryset: ResourceQuerySet):
        self.queryset = queryset
        if isinstance(self.queryset, ResourceQuerySet) and len(self.queryset) > 0:
            self.keyword_enum = self.queryset.first().keyword_enum
        else:
            msg = f"QuerySetResponseService received invalid queryset upon instantiation: `{type(self.queryset)}`"
            logger.error(msg)
            raise TypeError(msg)
        try:
            self.template = self.MAPPING[self.keyword_enum]
        except KeyError as e:
            msg = f"Invalid keyword_enum `{self.keyword_enum}` passed to `{self.__class__.__name__}`'s MAPPING attribute. Error: {e}"
            logger.error(msg, exc_info=True)
            raise

    def create_response(self):
        response_items = []
        for instance in self.queryset:
            res = self._create_resource_response(
                instance=instance,
                template=self.template,
                include_optional_params=True,
            )
            response_items.append(res)
        return "\n".join(response_items)


    def _create_resource_response(
            self, 
            instance: ResourceModel, 
            template: ResourceResponseTemplate,
            include_optional_params: bool = True,
    ) -> str:
        """Formats the SMS response based on the template rules."""
        data = {field: getattr(instance, field, "-") for field in template.always_show}
        extra_params = []
        
        if include_optional_params:
            for param in template.optional_params:
                value = getattr(instance, param, None)
                if value:
                    extra_params.append(f"{param}: {value}")

        data["extra_params"] = ", ".join(extra_params) if extra_params else ""
        return template.response_format.format(**data)