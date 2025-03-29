from common.enums import StreetNinjaEnum


class EmailRouteEnum(StreetNinjaEnum):

    CELERY = "celery"
    LOCATION_PARSING = "location-parsing"
    LOGGING = "logging"
    SENTRY = "sentry"

