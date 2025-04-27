from cache.redis.clients import LocationCacheClient
from cache.redis.access_patterns.location import LocationMapAccessPattern
import logging
from geo.models import Location
from django.contrib.gis.geos import Point
from django.db.models import QuerySet
from sms.resolvers.location.regex_library import RegexLibrary
from sms.resolvers.location import ResolvedLocation

logger = logging.getLogger(__name__)


class LocationService:

    def __init__(self):
        self.cache_client = LocationCacheClient(
            access_pattern=LocationMapAccessPattern,
        )

    def _normalize_text(self, location_text: str) -> str:
        text = RegexLibrary.normalize_string.sub("", location_text)
        text = text.lower().replace("&","and")
        text = RegexLibrary.multiple_whitespace.sub("", text)
        return text.strip()

    def _build_mapping(self, locations: QuerySet[Location]) -> dict[str, int]:
        """
        Returns a dict of (normalized) location_text to id
        """
        return {self._normalize_text(location.location_text) : location.id for location in locations}

    def _get_mapping(self) -> dict[str, int]:
        mapping = self.cache_client.get_mapping()
        if mapping is None:
            logger.info("Location cache mapping not found. Creating a new one...")
            mapping = self._build_mapping(self._fetch_locations())
            self._set_mapping_in_cache(mapping)
        return mapping

    def _fetch_locations(self) -> QuerySet[Location]:
        return Location.objects.all()

    def _set_mapping_in_cache(self, mapping: dict[str, int]):
        self.cache_client.set_mapping(mapping)

    def update_mapping(self, location: Location):
        mapping = self._get_mapping()
        mapping[self._normalize_text(location.location_text)] = location.id
        self._set_mapping_in_cache(mapping)

    def check_mapping(self, location_text: str) -> int | None:
        mapping = self._get_mapping()
        return mapping.get(self._normalize_text(location_text))

    def get_location_instance(self, id: int) -> Location:
        return Location.objects.get(id=id)

    def update_location(self, location: Location):
        location.total_inquiries += 1
        location.save()

    def create_location(self, resolved_location: ResolvedLocation, location: Point) -> Location:
        return Location.objects.create(
            location_text = resolved_location.location,
            location_type = resolved_location.location_type,
            location = location
        )