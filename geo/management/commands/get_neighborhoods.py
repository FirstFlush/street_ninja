import logging
from geo.models import Neighborhood
from street_ninja_server.base_commands import StreetNinjaCommand


logger = logging.getLogger(__name__)


class Command(StreetNinjaCommand):

    help = "Fetch and load neighborhood GIS data (Kitsilano, Dunbar, etc) from Vancouver OpenData API"

    def handle(self, *args, **kwargs):
        logger.info("Derrrrp")