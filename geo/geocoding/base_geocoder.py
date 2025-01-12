from abc import ABC, abstractmethod


class BaseGeocoder(ABC):

    @abstractmethod
    def geocode(self, location: str):
        pass

    @abstractmethod
    def reverse_geocode(self, latitude: float, longitude: float):
        pass
