from abc import ABC, abstractmethod
from geopy.location import Location


class BaseGeocoder(ABC):

    geopy_geocoder = None

    def __init__(self, config:dict[str, str]):
        self.config = config


    @abstractmethod
    def geocode(self, query: str) -> Location:
        pass

    @abstractmethod
    def reverse(self, latitude: float, longitude: float) -> Location:
        pass
