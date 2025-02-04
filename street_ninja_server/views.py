import logging
from rest_framework.views import APIView, Request, Response
from common.enums import HttpMethodEnum
from integrations.clients import VancouverAPIClient, WigleAPIClient
from integrations.clients.enums import VancouverEndpointsEnum
from django.conf import settings 
import json
from resources.models import (
    Shelter, 
    FoodProgram, 
    DrinkingFountain,
    Toilet,
)
from resources.serializers import (
    ShelterSerializer, 
    FoodProgramSerializer,
    DrinkingFountainSerializer,
    ParkToiletSerializer,
    PublicToiletSerializer
)
from integrations.integration_service import IntegrationService, IntegrationServiceParams

from sms.resolvers import SMSResolver
from common.enums import SMSKeywordEnum

logger = logging.getLogger(__name__)


class RedisTestView(APIView):

    def get(self, request:Request, *args, **kwargs):

        from common.redis import RedisClient, ShelterAccessPattern
        from resources.abstract_models import ResourceQuerySet

        data:ResourceQuerySet = RedisClient.get_or_set_db(access_pattern=ShelterAccessPattern)

        return Response({"ok":"ok"})


class KeywordTestView(APIView):

    def get(self, request:Request, *args, **kwargs):
        """
        For testing the SMS keyword mapping data structures
        """
        msg = "shelter womens 1140 Hastings St pet"
        sms_resolver = SMSResolver(inquiry=msg)
        params = sms_resolver._param_resolver.resolve_params(msg=msg, sms_keyword_enum=SMSKeywordEnum.SHELTER)


        return Response({"hihi":"hoho"})


class HomeView(APIView):


    def get(self, request:Request, *args, **kwargs):
        """
        This view currently serves as an all-purpose, quick-n-dirty testing route.
        """
        params = IntegrationServiceParams(
            api_client_class=VancouverAPIClient,
            endpoint_enum=VancouverEndpointsEnum.PUBLIC_WASHROOM,
            http_method_enum=HttpMethodEnum.GET,
            serializer_class=PublicToiletSerializer,
            model_class=Toilet,
            api_key=settings.VANCOUVER_OPEN_DATA_API_KEY,
        )

        integration_service = IntegrationService(params=params)
        integration_service.fetch_and_save()



        # api_client = WigleAPIClient(api_key=settings.WIGLE_API_KEY)
        # request_data = RequestData(
        #     method="GET",
        #     endpoint=api_client.endpoints.PUBLIC_WIFI,
        #     headers=api_client.api_header,
        #     params={
        #         "latrange1":49.275,
        #         "latrange2":49.295,
        #         "longrange1":-123.075,
        #         "longrange2":-123.100,
        #         "freenet":True,
        #     }
        # )

        # data = api_client.make_request(request_data=request_data)



        # api_client = VancouverAPIClient(
        #     api_key=settings.VANCOUVER_OPEN_DATA_API_KEY
        # )
        # request_data = RequestData(
        #     method="GET",
        #     endpoint=api_client.endpoints.SHELTERS.value,
        #     headers=api_client.api_header,
        # )


        # data = api_client.make_request(request_data=request_data)
        # serializer = ResourceSerializer(data=data['results'], many=True)

        return Response({"ok":"good"})
