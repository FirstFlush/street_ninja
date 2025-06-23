from django.contrib.gis.geos import Point
import logging
from collections import defaultdict
from typing import Type
from sms.enums import SMSKeywordEnum
from sms.response.response_templates.info_templates import InfoTemplate
from .dataclasses import MapData, MapPoint, MapPointData
from street_ninja_server.global_mappings import SMS_KEYWORD_ENUM_TO_RESOURCE_MODEL, SMS_KEYWORD_ENUM_TO_INFO_TEMPLATE
from resources.abstract_models import ResourceModel


logger = logging.getLogger(__name__)


class ResourceService:

    RESOURCE_MODELS = SMS_KEYWORD_ENUM_TO_RESOURCE_MODEL
    INFO_TEMPLATES = SMS_KEYWORD_ENUM_TO_INFO_TEMPLATE

    @classmethod
    def build_map_point_data(cls, resource_type: str, id: int) -> MapPointData | None:
        """
        Orchestration for building the info template to display information about 1 particular map pin.
        This is called when a user visiting the front-end website clicks on a map pin for more details.
        """
        resource_service = cls()
        resource_enum = resource_service._get_enum(resource_type)
        if resource_enum:
            model_instance = resource_service._get_instance(
                id=id,
                enum=resource_enum
            )
            if model_instance:
                template = resource_service._get_info_template(model=model_instance)
                if template:
                    return resource_service._build_point_data(
                        template=template,
                        model=model_instance,
                    )
        logger.error(f"Unable to build MapPointData with resource_type `{resource_type}` & id `{id}`")
        return None

    @staticmethod
    def _get_enum(s: str, raise_error: bool=False) -> SMSKeywordEnum | None:
        try:
            return SMSKeywordEnum[s.upper()]
        except KeyError as e:
            logger.error(e)
            if raise_error: raise

    def _get_instance(self, enum: SMSKeywordEnum, id: int) -> ResourceModel | None:
        model = self.RESOURCE_MODELS[enum]
        try:
            return model.objects.get(id=id)
        except model.DoesNotExist:
            logger.error(f"Invalid id `{id}`for model class `{model}`")
            return None

    def _get_info_template(self, model: ResourceModel) -> Type[InfoTemplate]:
        try:
            return self.INFO_TEMPLATES[model.keyword_enum]
        except KeyError as e:
            logger.error(f"InfoTemplate not found for model object: {model}")
            raise

    def _build_point_data(self, template: Type[InfoTemplate], model: ResourceModel) -> MapPointData:
        return MapPointData(info_template_data=template(model).display_info())


    @classmethod
    def build_map_data(cls) -> MapData | None:
        """  
        Constructs a MapData object containing categorized geospatial resource points.

        This method retrieves active resource records from the database, extracts their 
        geographical locations, and organizes them into a structured format suitable 
        for API responses and map rendering.        
        """
        map_data = defaultdict(list)
        resource_service = cls()

        for keyword_enum, model_class in resource_service.RESOURCE_MODELS.items():
            qs = model_class.objects.filter(is_active=True)
            for model_instance in qs:
                if model_instance.location and isinstance(model_instance.location, Point):
                    map_point = MapPoint(
                        longitude=model_instance.location.x,
                        latitude=model_instance.location.y,
                        id=model_instance.id,
                    )
                    map_data[keyword_enum.value.lower()].append(map_point)
        if len(map_data.keys()) == 0:
            logger.error(f"`{len(map_data.keys())}` resource records found when building MapData")
            return None

        return MapData(resources=dict(map_data))
