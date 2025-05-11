import logging
from rest_framework.views import APIView, Request, Response, status
from .resource_service import ResourceService
from .serializers.map import MapDataSerializer, MapPinSerializer


logger = logging.getLogger(__name__)


class MapView(APIView):

    def get(self, request: Request, *args, **kwargs):

        map_data = ResourceService.build_map_data()
        if map_data is not None:
            serializer = MapDataSerializer(map_data)
            return Response({
                "success": True,
                "data": serializer.data,
            }, status=status.HTTP_200_OK)

        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)


class MapPinView(APIView):

    def get(self, request: Request, id: int, resourceType: str, *args, **kwargs):

        serializer = MapPinSerializer(data={
            "resourceType": resourceType,
            "id": id,
        })
        if serializer.is_valid():
            point_data = ResourceService.build_map_point_data(
                resource_type=serializer.validated_data["resourceType"],
                id=serializer.validated_data["id"]
            )
            if point_data is not None:
                return Response({
                    "success": True,
                    "data": point_data.info_template_data,
                }, status=status.HTTP_200_OK)
        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)