from common.base_enum import StreetNinjaEnum


class SMSKeywordEnum(StreetNinjaEnum):
    """
    Enum representing the SMS keywords users can text to the Street Ninja app 
    to locate specific resources.

    Keywords:
        - FOOD: Information about nearest meal services or food resources.
        - SHELTER: Assistance finding nearest available shelters.
        - WATER: Locations for accessing nearest clean drinking water.
        - TOILET: Public or accessible restrooms nearby.
        - WIFI: Closest available public WiFi.

    These keywords are case-insensitive when used by the app's SMS interface.
    """
    FOOD = "FOOD"
    SHELTER = "SHELTER"
    WATER = "WATER"
    TOILET = "TOILET"
    WIFI = "WIFI"
    HELP = "HELP"
    # MORE = "MORE"


class SMSFollowUpKeywordEnum(StreetNinjaEnum):
    MORE = "more"
    INFO = "info"
    DIRECTIONS = "directions"


class ConversationStatus(StreetNinjaEnum):
    ACTIVE = "active"
    CLOSED = "closed"
    FLAGGED = "flagged"


class ResolvedSMSType(StreetNinjaEnum):
    INQUIRY = "inquiry"
    FOLLOW_UP = "follow_up"
    UNRESOLVED = "unresolved"


class FollowUpParams(StreetNinjaEnum):
    SELECTION = "selection"