import logging
from typing import Type

from django.conf import settings
from common.enums import GeocoderEnum
from .geocoders import *
from .geocoding_config import GeocoderConfig, GeocoderConfigData
from geo.exc import AllGeocodersFailed


logger = logging.getLogger(__name__)


class GeocodingService:
    """
    Service-layer for all things geocoding.
    """

    GEOCODER_MAPPING = {
        GeocoderEnum.NOMINATIM : NominatimGeocoder,
        GeocoderEnum.OPENCAGE : OpenCageGeocoder,
    }

    def __init__(self):
        self.config_data = self._config_data()

    def _config_data(self) -> GeocoderConfigData:
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

    def geocode(self, query:str) -> Location:
        """
        Attempt geocoding with primary geocoder, then fallbacks. 
        Raise AllGeocodersFailed exception if all fail.
        """
        print(self.config_data)
        result = self._try_primary(query=query)
        if result:
            return result
        result = self._try_fallbacks(query=query)
        if result:
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
        return self._try_geocoder(
            query=query, 
            geocoder_enum=self.config_data.primary_enum, 
            config=self.config_data.primary_config,
        )

    def _try_fallbacks(self, query:str) -> Location | None:

        for (fallback_enum, fallback_config) in self.config_data.fallbacks:
            location = self._try_geocoder(
                query=query, 
                geocoder_enum=fallback_enum,
                config=fallback_config,
            )
            if location:
                return location

