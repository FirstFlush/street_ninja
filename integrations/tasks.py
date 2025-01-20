from celery import shared_task


@shared_task
def fetch_data_from_city_api():
    # Placeholder task
    return "Fetched data from City API"

@shared_task
def fetch_wifi_data_from_wigle():
    # Placeholder task
    return "Fetched WiFi data from WiGLE"
