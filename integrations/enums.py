from common.enums import StreetNinjaEnum



class BaseURLEnum(StreetNinjaEnum):
    CITY_OF_VANCOUVER = "https://opendata.vancouver.ca"
    WIGLE = "https://wigle.net"


class VancouverEndpointsEnum(StreetNinjaEnum):

    SHELTERS = "/api/explore/v2.1/catalog/datasets/homeless-shelter-locations/records"
    FOOD_PROGRAMS = "/api/explore/v2.1/catalog/datasets/free-and-low-cost-food-programs/records"