from django.conf import settings
import logging
from geo.models import Neighborhood
from geo.neighborhoods.neighborhood_service import NeighborhoodService
from geo.neighborhoods.exc import NeighborhoodServiceError, NeighborhoodFileError
from street_ninja_server.base_commands import StreetNinjaCommand


logger = logging.getLogger(__name__)


class Command(StreetNinjaCommand):

    help = "Populate the Neighborhood table with GIS data from Vancouver OpenData API"

    def handle(self, *args, **kwargs):
        try:
            if settings.CI:
                self._handle_from_file(*args, **kwargs)
            else:
                try:
                    self._handle_api_call(*args, **kwargs)
                except NeighborhoodServiceError:
                    self._handle_from_file(*args, **kwargs)
        except Exception as e:
            msg = f"NeighborhoodService failed due to an unexpected error: `{e.__class__.__name__}`. Neighborhood table has not been populated!"
            logger.critical(msg, exc_info=True)
        else:
            self._count_neighborhoods()

    def _handle_from_file(self, *args, **kwargs):
        """Populate Neighborhood table with JSON data instead of API call"""
        ns = NeighborhoodService()
        try:
            ns.load_neighborhoods_from_file()
        except NeighborhoodFileError:
            msg = "Could not load neighborhood data from JSON file!"
            logger.critical(msg)      

    def _count_neighborhoods(self):
        count = Neighborhood.objects.count()
        msg = f"Neighborhood table populated successfully with `{count}` neighborhoods."
        logger.info(msg)

    def _handle_api_call(self, *args, **kwargs):
        if Neighborhood.objects.exists():
            count = Neighborhood.objects.count()
            msg = f"Neighborhoods already exist (count: `{count}`). Skipping fetch."
            logger.warning(msg)
            return
        ns = NeighborhoodService()
        try:
            neighborhoods = ns.get_neighborhoods()
        except NeighborhoodServiceError:
            msg = "Could not get neighborhood data!"
            logger.critical(msg)
            return
        try:
            ns.save_neighborhoods(neighborhoods)
        except NeighborhoodServiceError:
            msg = "Could not save neighborhood data!"
            logger.critical(msg)
            return
