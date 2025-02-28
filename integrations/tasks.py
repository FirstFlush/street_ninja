import logging
from street_ninja_server.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def fetch_shelter(self):
    print(self)
    if hasattr(self, "__dict__"):
        print(self.__dict__)
    print()



@app.task(bind=True)
def fetch_data_from_city_api(self):
    # Placeholder task
    logger.info(self)
    return "Fetched data from City API"

@app.task(bind=True)
def fetch_wifi_data_from_wigle(self):
    # Placeholder task
    return "Fetched WiFi data from WiGLE"
