from common.enums import StreetNinjaEnum


class APIClientEnum(StreetNinjaEnum):
    CITY_OF_VANCOUVER = "https://opendata.vancouver.ca"
    WIGLE = "https://api.wigle.net"



class EndpointsEnum(StreetNinjaEnum):
    ...


class VancouverEndpointsEnum(EndpointsEnum):

    SHELTERS = "/api/explore/v2.1/catalog/datasets/homeless-shelter-locations/records?limit=-1"
    FOOD_PROGRAMS = "/api/explore/v2.1/catalog/datasets/free-and-low-cost-food-programs/records?limit=-1"
    DRINKING_FOUNTAINS = "api/explore/v2.1/catalog/datasets/drinking-fountains/records"
    PUBLIC_WASHROOM = "/api/explore/v2.1/catalog/datasets/public-washrooms/records"
    PARK_WASHROOM = "/api/explore/v2.1/catalog/datasets/parks-washrooms/records"


class WigleEndpointsEnum(EndpointsEnum):

    PUBLIC_WIFI = "/api/v2/network/search"