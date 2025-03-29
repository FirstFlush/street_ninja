import logging
from typing import Type

from django.conf import settings
from django.contrib.gis.geos import Point
from street_ninja_server.global_mappings import GEOCODER_ENUM_TO_GEOCODER
from ..enums import GeocoderEnum
from .geocoders import *
from .geocoding_config import GeocoderConfig, GeocoderConfigData
from .exc import AllGeocodersFailed


logger = logging.getLogger(__name__)


class GeocodingService:
    """
    Service-layer for all things geocoding.
    """
    GEOCODER_MAPPING = GEOCODER_ENUM_TO_GEOCODER

    def __init__(self, config_data:GeocoderConfigData):
        self.config_data = config_data

    @classmethod
    def geocode(cls, query:str) -> Point:
        geocoding_service = cls(config_data=cls._build_config_data())
        location_object = geocoding_service._geocode(query=query)
        return geocoding_service._location_to_point(location_object)

    @staticmethod
    def _location_to_point(location:Location) -> Point:
        return Point(x=location.longitude, y=location.latitude, srid=4326)


    @staticmethod
    def _build_config_data() -> GeocoderConfigData:
        return GeocoderConfig.from_settings(
            settings_data=settings.GEOCODER_CONFIG,
            primary_geocoder_str=settings.PRIMARY_GEOCODER,
            use_fallbacks=True,
        )

    def _get_geocoder_class_from_mapping(self, geocoder_enum:GeocoderEnum) -> Type[BaseGeocoder]:
        try:
            return self.GEOCODER_MAPPING[geocoder_enum]
        except KeyError:
            logger.error(f"Geocoder `{geocoder_enum}` not found in GeocodingService.GEOCODER_MAPPING!", exc_info=True)
            raise

    def _normalize_query(self, query: str) -> str:
        remove_words = (
            "vancouver,", "canada,", "british columbia,", " bc, "
            "vancouver", "canada", "british columbia", " bc ",
        )
        query = query.lower()
        for word in remove_words:
            query = query.replace(word, "")

        return f"{' '.join(query.split())}, Vancouver, Canada"


    def _geocode(self, query: str) -> Location:
        """
        Attempt geocoding with primary geocoder, then fallbacks. 
        Raise AllGeocodersFailed exception if all fail.
        """
        query = self._normalize_query(query)
        logger.info(f"QUERY: `{query}`")
        
        result = self._try_primary(query=query)
        if result:
            logger.info(f"Geocoding succeeded using primary geocoder `{self.config_data.primary_enum}`. Coordinates: `{result.point.__str__()}`")
            return result

        result = self._try_fallbacks(query=query)
        if result:
            logger.info(f"Geocoding succeeded using a fallback geocoder.")
            return result

        msg = f"All geocoders failed for query: `{query}`."
        logger.error(msg, exc_info=True)
        raise AllGeocodersFailed(msg)


    def _try_geocoder(self, query:str, geocoder_enum:GeocoderEnum, config:dict[str, str]) -> Location | None:
        """
        Instantiate the geocoder and call .geocode(query).
        Return a geopy Location or None on error/no result.
        """
        try:
            geocoder_class = self._get_geocoder_class_from_mapping(geocoder_enum)
            geocoder_instance = geocoder_class(config=config)
            result = geocoder_instance.geocode(query=query)
            if not result:
                logger.warning(f"`{geocoder_enum}` returned no results for address `{query}`.")
            return result
        except Exception as e:
            logger.error(f"Exception `{e.__class__.__name__}` occurred using geocoder `{geocoder_enum}` for query `{query}`.", exc_info=True)
            return None

    def _try_primary(self, query:str) -> Location | None:
        location = self._try_geocoder(
            query=query, 
            geocoder_enum=self.config_data.primary_enum, 
            config=self.config_data.primary_config,
        )
        if not location:
            logger.warning(f"Primary geocoder `{self.config_data.primary_enum}` failed for `{query}`.")
        return location

    def _try_fallbacks(self, query:str) -> Location | None:
        for (fallback_enum, fallback_config) in self.config_data.fallbacks:
            logger.info(f"Trying fallback geocoder `{fallback_enum}` for query `{query}`.")
            location = self._try_geocoder(
                query=query, 
                geocoder_enum=fallback_enum,
                config=fallback_config,
            )
            if location:
                logger.info(f"Fallback geocoder `{fallback_enum}` succeeded for `{query}`.")
                return location
        logger.warning(f"All fallbacks failed for `{query}`.")
        return None

