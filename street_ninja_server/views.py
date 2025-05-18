from rest_framework.views import APIView, Request, Response
from integrations.clients import VancouverAPIClient
from integrations.clients.enums import VancouverEndpointsEnum


class TestView(APIView):

    def get(self, request: Request, *args, **kwargs):

        return Response({"ping":"pong"})


# class HomeView(APIView):


#     def get(self, request:Request, *args, **kwargs):
#         """
#         This view currently serves as an all-purpose, quick-n-dirty testing route.
#         """
#         from integrations.integration_service import IntegrationService, IntegrationServiceParams
#         from common.enums import HttpMethodEnum
#         from integrations.clients import VancouverAPIClient, WigleAPIClient
#         from integrations.clients.enums import VancouverEndpointsEnum
#         from resources.serializers import (
#             ShelterSerializer, 
#             FoodProgramSerializer,
#             DrinkingFountainSerializer,
#             PublicToiletSerializer
#         )
#         from resources.models import (
#             Shelter, 
#             FoodProgram, 
#             DrinkingFountain,
#             Toilet,
#         )
#         from django.conf import settings


#         params = IntegrationServiceParams(
#             api_client_class=VancouverAPIClient,
#             endpoint_enum=VancouverEndpointsEnum.PUBLIC_WASHROOM,
#             http_method_enum=HttpMethodEnum.GET,
#             serializer_class=PublicToiletSerializer,
#             model_class=Toilet,
#             api_key=settings.VANCOUVER_OPEN_DATA_API_KEY,
#             http_params = {
#                 'limit': 100,
#                 'offset': 0,
#             }
#         )
        
#         integration_service = IntegrationService(params=params)
#         integration_service.fetch_and_save()

#         return Response({"ok":"good"})
