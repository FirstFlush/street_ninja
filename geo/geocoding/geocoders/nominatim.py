from geopy.geocoders import Nominatim
from ..base_geocoder import BaseGeocoder
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..geocoding_service import GeocoderConfig

class NominatimGeocoder(BaseGeocoder):
    def __init__(self, config:"GeocoderConfig"):
        self.geolocator = Nominatim(**config)

    def geocode(self, location: str):
        return self.geolocator.geocode(location)

    def reverse_geocode(self, latitude: float, longitude: float):
        return self.geolocator.reverse((latitude, longitude))
