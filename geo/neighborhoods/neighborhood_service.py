from django.contrib.gis.geos import Point
from django.db import transaction
from rest_framework.exceptions import ValidationError
from geo.models import Neighborhood
from .dataclasses import IncomingNeighborhoodData
from .exc import NeighborhoodServiceError, NeighborhoodFileError
from common.dataclasses import RequestData
from common.enums import HttpMethodEnum
from geo.serializers import NeighborhoodSerializer
from integrations.clients.vancouver import VancouverAPIClient
from integrations.clients.enums import VancouverEndpointsEnum
from typing import Any
from geo.geospatial.polygon_service import PolygonService
import logging
from django.conf import settings
from django.core.management import call_command


logger = logging.getLogger(__name__)


class NeighborhoodService:
    """
    Service layer for managing City of Vancouver neighborhood data.
    Used by the custom manage.py command get_neighborhoods to populate the Neighborhood table.
    If the OpenData API is unavailable or fails validation, the system can fall back to loading a static local JSON file.
    
    -Raises NeighborhoodFileError if there is an issue loading JSON data from file
    -Raises NeighborhoodServiceError if it fails for any other reason.
    """

    _serializer_cls = NeighborhoodSerializer

    def __init__(self):
        self.api_client = VancouverAPIClient(api_key=settings.VANCOUVER_OPEN_DATA_API_KEY)
        self.json_data_file_path = f"{settings.BASE_DIR}/street_ninja_server/tests/testdata/model_dumps/neighborhoods.json"

    def load_neighborhoods_from_file(self):
        try:
            call_command("loaddata", self.json_data_file_path)
        except Exception as e:
            msg = f"Neighborhood model data at file path `{self.json_data_file_path}` could not be loaded into DB due to an unexpected `{e.__class__.__name__}`"
            logger.critical(msg, exc_info=True)
            raise NeighborhoodFileError(msg) from e

    def get_neighborhoods(self) -> list[IncomingNeighborhoodData]:
        try:
            api_data = self._fetch_neighborhood_data()
        except Exception as e:
            msg = "Failed to fetch neighborhood data from Vancouver OpenData API"
            logger.error(msg, exc_info=True)
            raise NeighborhoodServiceError(msg) from e
        try:
            parsed_data = self._shape_neighborhood_data(data=api_data)
        except Exception as e:
            msg = "Failed to shape neighborhood data from Vancouver OpenData API"
            logger.error(msg, exc_info=True)
            raise NeighborhoodServiceError(msg) from e
        try:
            return self._validate_neighborhood_data(neighborhood_data=parsed_data)
        except Exception as e:
            msg = "Failed to validate neighborhood data from Vancouver OpenData API"
            logger.error(msg, exc_info=True)
            raise NeighborhoodServiceError(msg) from e

    def save_neighborhoods(self, neighborhood_data: list[IncomingNeighborhoodData]):
        try:
            with transaction.atomic():
                for neighborhood in neighborhood_data:
                    Neighborhood.objects.create(
                        name=neighborhood.name,
                        boundary=PolygonService.create_polygon_from_list_of_points(neighborhood.coordinates),
                        centroid=neighborhood.centroid,
                    )
        except Exception as e:
            msg = "Failed to save neighborhood data from Vancouver OpenData API"
            logger.error(msg, exc_info=True)
            raise NeighborhoodServiceError(msg) from e

    def _shape_neighborhood_data(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        hoods = []
        for d in data["results"]:
            coordinates = d["geom"]["geometry"]["coordinates"][0]
            hoods.append({
                "name": d["name"],
                "coordinates": coordinates,
            })
        return hoods

    def _fetch_neighborhood_data(self) -> dict[str, Any]:
        request_data = RequestData(
            method=HttpMethodEnum.GET.value,
            endpoint=VancouverEndpointsEnum.NEIGHBORHOODS,
            params={
                'limit': 100,
                'offset': 0,
            }
        )
        return self.api_client.make_request(request_data=request_data)
    
    def _create_neighborhood_data(self, data: dict[str, Any]) -> IncomingNeighborhoodData:
        return IncomingNeighborhoodData(
            name = data["name"],
            coordinates = [Point(x=x, y=y) for x, y in  data["coordinates"]],
            centroid = PolygonService.get_centroid(boundary_coordinates=data["coordinates"])
        )

    def _validate_neighborhood_data(self, neighborhood_data: list[dict[str, Any]]) -> list[IncomingNeighborhoodData]:
        serializer = self._serializer_cls(data=neighborhood_data, many=True)
        if serializer.is_valid():
            return [self._create_neighborhood_data(d) for d in serializer.validated_data]
        else:
            logger.error(f"`{self._serializer_cls.__name__}` failed due to the following errors: {serializer.errors}")
            raise ValidationError({
                "message": f"{self._serializer_cls.__name__} failed validation",
                "errors": serializer.errors,
            })
