import logging
from django.conf import settings
from common.enums import HttpMethodEnum
from resources.models import (
    Shelter,
    FoodProgram,
    Toilet,
    DrinkingFountain,
    PublicWifi,
)
from resources.serializers import (
    ShelterSerializer,
    FoodProgramSerializer,
    PublicToiletSerializer,
    DrinkingFountainSerializer,
    WigleSerializer,
)
from street_ninja_server.celery import app
from .integration_service import IntegrationService, IntegrationServiceParams
from .clients import VancouverAPIClient, WigleAPIClient
from .clients.enums import VancouverEndpointsEnum, WigleEndpointsEnum


logger = logging.getLogger(__name__)


@app.task(bind=True)
def fetch_shelter(self):
    params = IntegrationServiceParams(
        api_client_class=VancouverAPIClient,
        api_key=settings.VANCOUVER_OPEN_DATA_API_KEY,
        endpoint_enum=VancouverEndpointsEnum.SHELTERS,
        http_method_enum=HttpMethodEnum.GET,
        serializer_class=ShelterSerializer,
        model_class=Shelter,
        http_params = {
            'limit': 100,
            'offset': 0,
        }
    )
    integration_service = IntegrationService(params)
    integration_service.fetch_and_save()


@app.task(bind=True)
def fetch_food(self):
    params = IntegrationServiceParams(
        api_client_class=VancouverAPIClient,
        api_key=settings.VANCOUVER_OPEN_DATA_API_KEY,
        endpoint_enum=VancouverEndpointsEnum.FOOD_PROGRAMS,
        http_method_enum=HttpMethodEnum.GET,
        serializer_class=FoodProgramSerializer,
        model_class=FoodProgram,
        http_params = {
            'limit': 100,
            'offset': 0,
        }
    )
    integration_service = IntegrationService(params)
    integration_service.fetch_and_save()


@app.task(bind=True)
def fetch_toilet(self):
    params = IntegrationServiceParams(
        api_client_class=VancouverAPIClient,
        api_key=settings.VANCOUVER_OPEN_DATA_API_KEY,
        endpoint_enum=VancouverEndpointsEnum.PUBLIC_WASHROOM,
        http_method_enum=HttpMethodEnum.GET,
        serializer_class=PublicToiletSerializer,
        model_class=Toilet,
        http_params = {
            'limit': 100,
            'offset': 0,
        }
    )
    integration_service = IntegrationService(params)
    integration_service.fetch_and_save()


@app.task(bind=True)
def fetch_water(self):
    params = IntegrationServiceParams(
        api_client_class=VancouverAPIClient,
        api_key=settings.VANCOUVER_OPEN_DATA_API_KEY,
        endpoint_enum=VancouverEndpointsEnum.DRINKING_FOUNTAINS,
        http_method_enum=HttpMethodEnum.GET,
        serializer_class=DrinkingFountainSerializer,
        model_class=DrinkingFountain,
        http_params = {
            'limit': 100,
            'offset': 0,
        }
    )
    integration_service = IntegrationService(params)
    integration_service.fetch_and_save()



