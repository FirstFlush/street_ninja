from dataclasses import dataclass
import logging
from typing import Any
from .enums import GeocoderEnum


logger = logging.getLogger(__name__)


@dataclass
class GeocoderConfigData:
    primary_enum: GeocoderEnum
    primary_config: dict[str, str]
    fallbacks: list[tuple[GeocoderEnum, dict[str, str]]]


class GeocoderConfig:
    """
    Retrieves geocoder configuration settings for use in GeocoderService class.
    These are the API keys, headers, and whatever else GeocoderService needs
    to access the 3rd-party Geocoding APIs consumed by Street Ninja.
    """
    @classmethod
    def from_settings(
            cls, 
            settings_data:dict[str, dict[str, str]], 
            primary_geocoder_str:str, 
            use_fallbacks:bool
    ) -> GeocoderConfigData:
        """
            Helper method to get GeocoderConfigData object without explicitly instantiating 
            GeocoderConfig in the calling code.
        """
        config_data = { GeocoderEnum[k] : v for k, v in settings_data.items() }
        primary_geocoder = GeocoderEnum(primary_geocoder_str)
        return cls(
            config_data=config_data
        ).get_config_data(
            primary_geocoder=primary_geocoder, 
            use_fallbacks=use_fallbacks
        )


    def __init__(self, config_data: dict[GeocoderEnum, dict[str, str]]):
        """
        Initialize with geocoder configuration data.

        Args:
            config (dict[str, str]): The configuration mapping geocoder names to settings.
        """
        self.config_data = config_data


    def get_primary(self, primary_geocoder: GeocoderEnum) -> dict[str, Any]:
        """
        Retrieve the primary geocoder configuration.

        Args:
            primary_geocoder (GeocoderEnum): The geocoder to be set as primary.

        Returns:
            dict: Primary geocoder configuration.
        """
        if primary_geocoder not in self.config_data:
            msg = f"Primary geocoder '{primary_geocoder.name}' is not configured."
            logger.error(msg, exc_info=True)
            raise ValueError(msg)
        
        return {
            'primary_enum' : primary_geocoder,
            'primary_config' : self.config_data[primary_geocoder]
        }

    def get_fallbacks(self, primary_geocoder: GeocoderEnum) -> list[tuple[GeocoderEnum, dict[str, str]]]:
        """
        Retrieve fallback geocoder configurations.

        Args:
            primary_geocoder (GeocoderEnum): The primary geocoder to exclude from fallbacks.

        Returns:
            list: List of fallback geocoder configurations.
        """
        return [(geocoder, config_data) for geocoder, config_data in self.config_data.items() if geocoder != primary_geocoder]

    def get_config_data(self, primary_geocoder: GeocoderEnum, use_fallbacks: bool = False) -> GeocoderConfigData:
        """
        Retrieves the geocoder configuration with primary and optional fallbacks.

        Args:
            primary_geocoder (GeocoderEnum): The primary geocoder.
            use_fallbacks (bool): Whether to include fallback geocoders.

        Returns:
            GeocoderConfigData: The structured configuration data.
        """
        primary_data = self.get_primary(primary_geocoder)
        fallbacks = self.get_fallbacks(primary_geocoder) if use_fallbacks else []
        return GeocoderConfigData(
            primary_enum=primary_data['primary_enum'], 
            primary_config=primary_data['primary_config'],
            fallbacks=fallbacks
        )
