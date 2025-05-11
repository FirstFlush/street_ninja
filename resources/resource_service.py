import logging
from collections import defaultdict
from sms.enums import SMSKeywordEnum
from sms.response.response_templates.info_templates import InfoTemplate
from .dataclasses import MapData, MapPoint, MapPointData
from street_ninja_server.global_mappings import SMS_KEYWORD_ENUM_TO_RESOURCE_MODEL, SMS_KEYWORD_ENUM_TO_INFO_TEMPLATE
from resources.abstract_models import ResourceModel

logger = logging.getLogger(__name__)


class ResourceService:

    RESOURCE_MODELS = SMS_KEYWORD_ENUM_TO_RESOURCE_MODEL

    @staticmethod
    def get_enum(s: str, raise_error: bool=False) -> SMSKeywordEnum | None:
        try:
            return SMSKeywordEnum[s.upper()]
        except KeyError as e:
            logger.error(e)
            if raise_error: raise


    def get_instance(self, enum: SMSKeywordEnum, id: int) -> ResourceModel | None:
        model = self.RESOURCE_MODELS[enum]
        try:
            return model.objects.get(id=id)
        except model.DoesNotExist:
            logger.error(f"Invalid id `{id}`for model class `{model}`")
            return None


    def get_info_template(self, model: ResourceModel) -> InfoTemplate:
        try:
            return SMS_KEYWORD_ENUM_TO_INFO_TEMPLATE[model.keyword_enum]
        except KeyError as e:
            logger.error(f"InfoTemplate not found for model object: {model}")
            raise


    def build_point_data(self, template: InfoTemplate, model: ResourceModel) -> MapPointData:
        return MapPointData(data=template(model).display_info())
        # return model.map_values

    def build_map_data(self) -> MapData | None:
        """  
        Constructs a MapData object containing categorized geospatial resource points.

        This method retrieves active resource records from the database, extracts their 
        geographical locations, and organizes them into a structured format suitable 
        for API responses and map rendering.        
        """
        map_data = defaultdict(list)

        for keyword_enum, model_class in self.RESOURCE_MODELS.items():
            qs = model_class.objects.filter(is_active=True)
            for model_instance in qs:
                if model_instance.location:
                    map_point = MapPoint(
                        longitude=model_instance.location.x,
                        latitude=model_instance.location.y,
                        id=model_instance.id,
                    )
                    map_data[keyword_enum.value.lower()].append(map_point)
        if len(map_data.keys()) == 0:
            logger.warning(f"`{len(map_data.keys())}` resource records found when building MapData")
            return None

        return MapData(resources=dict(map_data))
