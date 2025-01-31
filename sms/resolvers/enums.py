from common.base_enum import StreetNinjaEnum


class ResolvedSMSType(StreetNinjaEnum):
    INQUIRY = "inquiry"
    FOLLOW_UP = "follow_up"
    UNRESOLVED = "unresolved"