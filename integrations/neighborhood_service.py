from django.contrib.gis.geos import Point
from django.db import transaction
from rest_framework.exceptions import ValidationError
from geo.models import Neighborhood
from .dataclasses import NeighborhoodData
from .exc import NeighborhoodServiceError
from common.dataclasses import RequestData
from common.enums import HttpMethodEnum
from geo.serializers import NeighborhoodSerializer
from .clients.vancouver import VancouverAPIClient
from .clients.enums import VancouverEndpointsEnum
from django.conf import settings
from typing import Any
from geo.geospatial.polygon_service import PolygonService
import logging


logger = logging.getLogger(__name__)


class NeighborhoodService:
    """
    This class handles fetching/validating/saving neighborhood data
    get_neighborhoods and save_neighborhoods are the two main public methods.
    the custom manage.py command `get_neighborhoods` calls this class to
    populate the Neighborhood table.

    Raises NeighborhoodServiceError if it fails for any reason.
    """

    _serializer_cls = NeighborhoodSerializer
    api_client = VancouverAPIClient(api_key=settings.VANCOUVER_OPEN_DATA_API_KEY)
    
    def get_neighborhoods(self) -> list[NeighborhoodData]:
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

    def save_neighborhoods(self, neighborhood_data: list[NeighborhoodData]):
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
    
    def _create_neighborhood_data(self, data: dict[str, Any]) -> NeighborhoodData:
        return NeighborhoodData(
            name = data["name"],
            coordinates = [Point(x=x, y=y) for x, y in  data["coordinates"]],
            centroid = PolygonService.get_centroid(boundary_coordinates=data["coordinates"])
        )

    def _validate_neighborhood_data(self, neighborhood_data: list[dict[str, Any]]) -> list[NeighborhoodData]:
        serializer = self._serializer_cls(data=neighborhood_data, many=True)
        if serializer.is_valid():
            return [self._create_neighborhood_data(d) for d in serializer.validated_data]
        else:
            logger.error(f"`{self._serializer_cls.__name__}` failed due to the following errors: {serializer.errors}")
            raise ValidationError({
                "message": f"{self._serializer_cls.__name__} failed validation",
                "errors": serializer.errors,
            })
