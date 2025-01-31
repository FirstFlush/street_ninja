from common.base_enum import StreetNinjaEnum


class ConversationStatus(StreetNinjaEnum):

    ACTIVE = "active"
    CLOSED = "closed"
    FLAGGED = "flagged"


class SMSFollowUpKeywordEnum(StreetNinjaEnum):

    MORE = "more"
    DIRECTIONS = "directions"