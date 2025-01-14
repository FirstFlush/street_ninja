from geopy.geocoders import Nominatim, GoogleV3, MapBox
from geopy.exc import GeocoderServiceError, GeopyError
from typing import Optional
from common.enums import GeocoderEnum
from .geocoding_config import GeocoderConfigData


class Geocoder:
    """
    Handles geocoding and reverse geocoding operations using primary and fallback geocoders.
    """

    def __init__(self, config_data: GeocoderConfigData):
        """
        Initializes the Geocoder with primary and fallback geocoders.

        Args:
            config_data (GeocoderConfigData): Configuration data for the geocoders.
        """
        self.primary = self._initialize_geocoder(config_data.primary)
        self.fallbacks = [
            self._initialize_geocoder(fallback) for fallback in config_data.fallbacks
        ]

    def _initialize_geocoder(self, geocoder_data: dict[GeocoderEnum, str]):
        """
        Initializes a geopy geocoder based on the GeocoderEnum type.

        Args:
            geocoder_data (dict[GeocoderEnum, str]): Geocoder type and its configuration.

        Returns:
            geopy.geocoder: An instance of the configured geocoder.
        """
        geocoder_type = list(geocoder_data.keys())[0]
        config = geocoder_data[geocoder_type]

        if geocoder_type == GeocoderEnum.NOMINATIM:
            return Nominatim(user_agent=config["user_agent"])
        elif geocoder_type == GeocoderEnum.GOOGLEMAPS:
            return GoogleV3(api_key=config["api_key"])
        elif geocoder_type == GeocoderEnum.MAPBOX:
            return MapBox(api_key=config["api_key"])
        else:
            raise ValueError(f"Unsupported geocoder type: {geocoder_type}")


    def _try_geocode(self, method, *args, **kwargs) -> Optional[dict]:
        """
        Attempts a geocoding method with the primary geocoder and fallbacks.

        Args:
            method (callable): The geocoding or reverse geocoding method to call.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            dict: Geocoding result if successful.

        Raises:
            RuntimeError: If all geocoding attempts fail.
        """
        geocoders = [self.primary] + self.fallbacks

        for geocoder in geocoders:
            try:
                return method(geocoder, *args, **kwargs)
            except (GeocoderServiceError, GeopyError) as e:
                # Log the error and try the next geocoder
                print(f"Geocoder failed: {e}")  # Replace with proper logging

        # If all geocoders fail, raise an error
        raise RuntimeError("All geocoders failed to process the request.")

    def geocode(self, address: str, **kwargs) -> dict:
        """
        Geocodes an address using the primary and fallback geocoders.

        Args:
            address (str): The address to geocode.
            **kwargs: Additional options for geocoding.

        Returns:
            dict: Geocoding result if successful.
        """
        return self._try_geocode(lambda geocoder, addr, **kw: geocoder.geocode(addr, **kw), address, **kwargs)

    def reverse_geocode(self, latitude: float, longitude: float, **kwargs) -> dict:
        """
        Reverse geocodes coordinates using the primary and fallback geocoders.

        Args:
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.
            **kwargs: Additional options for reverse geocoding.

        Returns:
            dict: Reverse geocoding result if successful.
        """
        return self._try_geocode(
            lambda geocoder, lat, lng, **kw: geocoder.reverse((lat, lng), **kw),
            latitude, longitude, **kwargs
        )
