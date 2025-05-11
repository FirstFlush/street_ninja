import logging
from rest_framework.views import APIView, Request, Response, status
from .resource_service import ResourceService
from .serializers.map import MapDataSerializer, MapPinSerializer

logger = logging.getLogger(__name__)


class MapView(APIView):

    def get(self, request: Request, *args, **kwargs):
        
        resource_service = ResourceService()
        map_data = resource_service.build_map_data()
        if map_data:
            serializer = MapDataSerializer(map_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)


class MapPinView(APIView):

    def get(self, request: Request, id: int, resourceType: str, *args, **kwargs):

        serializer = MapPinSerializer(data={
            "resourceType": resourceType,
            "id": id,
        })
        if serializer.is_valid():
            resource_service = ResourceService()
            resource_enum = resource_service.get_enum(serializer.validated_data["resourceType"])
            if resource_enum:
                model_instance = resource_service.get_instance(
                    id=serializer.validated_data["id"], 
                    enum=resource_enum
                )
                if model_instance:
                    template = resource_service.get_info_template(model=model_instance)
                    if template:
                        point_data = resource_service.build_point_data(
                            template=template,
                            model=model_instance,
                        )
                        return Response(point_data.data, status=status.HTTP_200_OK)
        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)