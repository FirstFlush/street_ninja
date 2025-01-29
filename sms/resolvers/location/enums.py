from common.base_enum import StreetNinjaEnum


class RegexEnum(StreetNinjaEnum):

    @classmethod
    def regex_string(cls) -> str:
        return "|".join(cls.values)


class StreetDirectionEnum(RegexEnum):
    NORTH = "n"
    EAST = "e"
    WEST = "w"
    SOUTH = "s"
    NORTH_WEST = "nw"
    NORTH_EAST = "ne"
    SOUTH_WEST = "sw"
    SOUTH_EAST = "se"
    NORTH_LONG = "north"
    EAST_LONG = "east"
    WEST_LONG = "west"
    SOUTH_LONG = "south"
    NORTH_WEST_LONG = "northwest"
    NORTH_EAST_LONG = "northeast"
    SOUTH_WEST_LONG = "southwest"
    SOUTH_EAST_LONG = "southeast"


class StreetSuffixEnum(RegexEnum):
    STREET = "st"
    ROAD = "rd"
    AVENUE = "ave"
    LANE = "lane"
    COURT = "crt"
    DRIVE = "dr"
    BOULEVARD = "blvd"
    WAY = "way"
    PLACE = "pl"
    HIGHWAY = "hwy"
    STREET_LONG = "street"
    ROAD_LONG = "road"
    AVENUE_LONG = "avenue"
    COURT_LONG = "court"
    DRIVE_LONG = "drive"
    BOULEVARD_LONG = "boulevard"
    PLACE_LONG = "place"
    HIGHWAY_LONG = "highway"
    AVENUE_SHORT = "av"

