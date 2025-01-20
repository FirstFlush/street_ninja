import logging
from rest_framework.views import APIView, Request, Response
from common.dataclasses import RequestData
from integrations.clients import VancouverAPIClient, WigleAPIClient
from django.conf import settings 
import json
from resources.serializers import ResourceSerializer


logger = logging.getLogger(__name__)


class HomeView(APIView):


    def get(self, request:Request, *args, **kwargs):
        """
        This view currently serves as an all-purpose, quick-n-dirty testing route.
        """

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
        # # print(data)

        # print(json.dumps(data))


        api_client = VancouverAPIClient(
            api_key=settings.VANCOUVER_OPEN_DATA_API_KEY
        )
        request_data = RequestData(
            method="GET",
            endpoint=api_client.endpoints.SHELTERS.value,
            headers=api_client.api_header,
        )


        data = api_client.make_request(request_data=request_data)
        serializer = ResourceSerializer(data=data['results'], many=True)

        # print(serializer.initial_data)
        if serializer.is_valid():
            print(serializer.validated_data)
        else:
            print(serializer.errors)

        return Response({"ok":"good"})
