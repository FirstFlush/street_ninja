from django.conf import settings
from common.enums import StreetNinjaEnum


class EmailRouteEnum(StreetNinjaEnum):

    CELERY = settings.EMAIL_ROUTE_CELERY
    DIRECTIONS = settings.EMAIL_ROUTE_DIRECTIONS
    LOCATION_PARSING = settings.EMAIL_ROUTE_LOCATION_PARSING
    LOGGING = settings.EMAIL_ROUTE_LOGGING
    SENTRY = settings.EMAIL_ROUTE_SENTRY
