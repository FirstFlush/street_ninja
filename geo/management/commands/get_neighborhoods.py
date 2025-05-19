import logging
from geo.models import Neighborhood
from geo.neighborhoods.neighborhood_service import NeighborhoodService
from geo.neighborhoods.exc import NeighborhoodServiceError
from street_ninja_server.base_commands import StreetNinjaCommand


logger = logging.getLogger(__name__)


class Command(StreetNinjaCommand):

    help = "Populate the Neighborhood table with GIS data from Vancouver OpenData API"

    def handle(self, *args, **kwargs):
        try:
            self._handle(*args, **kwargs)
        except Exception as e:
            msg = f"NeighborhoodService failed due to an unexpected error: `{e.__class__.__name__}`. Neighborhood table has not been populated!"
            logger.critical(msg, exc_info=True)

    def _handle(self, *args, **kwargs):
        if Neighborhood.objects.exists():
            count = Neighborhood.objects.count()
            msg = f"Neighborhoods already exist (count: `{count}`). Skipping fetch."
            logger.warning(msg)
            return

        ns = NeighborhoodService()

        try:
            neighborhoods = ns.get_neighborhoods()
        except NeighborhoodServiceError:
            msg = "Could not fetch neighborhood data! Neighborhood table has not been populated!"
            logger.critical(msg)
            return

        try:
            ns.save_neighborhoods(neighborhoods)
        except NeighborhoodServiceError:
            msg = "Could not save neighborhood data! Neighborhood table has not been populated!"
            logger.critical(msg)
            return

        count = Neighborhood.objects.count()
        msg = f"Neighborhood table populated successfully with `{count}` neighborhoods."
        logger.info(msg)
