from geopy.geocoders import Nominatim, OpenCage
from geopy.location import Location
from .base_geocoder import BaseGeocoder


class NominatimGeocoder(BaseGeocoder):

    geopy_geocoder = Nominatim

    def geocode(self, query:str) -> Location:
        geocoder = self.geopy_geocoder(user_agent=self.config['user_agent']) 
        return geocoder.geocode(query)

    def reverse(self, latitude:float, longitude:float) -> Location:
        geocoder = self.geopy_geocoder(user_agent=self.config['user_agent']) 
        return geocoder.reverse((latitude, longitude))


class OpenCageGeocoder(BaseGeocoder):

    geopy_geocoder = OpenCage

    def geocode(self, query:str) -> Location: 
        geocoder = self.geopy_geocoder(api_key=self.config['api_key'])
        return geocoder.geocode(query)

    def reverse(self, latitude:float, longitude:float) -> Location:
        geocoder = self.geopy_geocoder(api_key=self.config['api_key'])
        return geocoder.reverse((latitude, longitude))
