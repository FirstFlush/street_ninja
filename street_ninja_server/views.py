import logging
from rest_framework.views import APIView, Request, Response

logger = logging.getLogger(__name__)


from common.dataclasses import RequestData
from integrations.clients.vancouver import VancouverAPIClient
from integrations.enums import BaseURLEnum, VancouverEndpointsEnum
from django.conf import settings 

class HomeView(APIView):


    def get(self, request:Request, *args, **kwargs):

        api_client = VancouverAPIClient(
            api_key=settings.VANCOUVER_OPEN_DATA_API_KEY
        )
        request_data = RequestData(
            method="GET",
            endpoint=api_client.endpoints.SHELTERS.value,
            headers=api_client.api_header,
        )

        # print(request_data.to_request_dict())

        data = api_client.make_request(request_data=request_data)
        print(data)

        return Response({"ok":"good"})
