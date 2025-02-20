import logging
from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from .resource_service import ResourceService
from .serializers import MapDataSerializer

logger = logging.getLogger(__name__)


class MapView(APIView):

    def get(self, request: Request, *args, **kwargs):
        
        resource_service = ResourceService()
        map_data = resource_service.build_map_data()
        if map_data:
            serializer = MapDataSerializer(map_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response("Failed to fetch map data", status=status.HTTP_400_BAD_REQUEST)