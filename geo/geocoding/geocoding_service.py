import logging
from django.conf import settings
from common.enums import GeoCoder


logger = logging.getLogger(__name__)


class GeocoderConfig:
    """
    Retrieves geocoder configuration settings for use in GeocoderService.

    This class maps GeoCoder enum values to their corresponding configuration 
    settings, ensuring that each geocoder has the necessary parameters for initialization.
    """
    @staticmethod
    def get(geocoder: GeoCoder) -> dict[str, str]:
        try:
            return settings.GEOCODER_CONFIG[geocoder.value]
        except KeyError:
            msg = f"Unsupported geocoder: {geocoder}"
            logger.error(msg, exc_info=True)
            raise
