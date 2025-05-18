from common.enums import StreetNinjaEnum


class APIClientEnum(StreetNinjaEnum):
    CITY_OF_VANCOUVER = "https://opendata.vancouver.ca"
    WIGLE = "https://api.wigle.net"
    OPEN_ROUTE_SERVICE = "https://api.openrouteservice.org"
    # GRAPH_HOPPER = "https://graphhopper.com"

class EndpointsEnum(StreetNinjaEnum):
    ...


class VancouverEndpointsEnum(EndpointsEnum):

    SHELTERS = "/api/explore/v2.1/catalog/datasets/homeless-shelter-locations/records"
    FOOD_PROGRAMS = "/api/explore/v2.1/catalog/datasets/free-and-low-cost-food-programs/records"
    DRINKING_FOUNTAINS = "api/explore/v2.1/catalog/datasets/drinking-fountains/records"
    PUBLIC_WASHROOM = "/api/explore/v2.1/catalog/datasets/public-washrooms/records"
    PARK_WASHROOM = "/api/explore/v2.1/catalog/datasets/parks-washrooms/records"
    NEIGHBORHOODS = "/api/explore/v2.1/catalog/datasets/local-area-boundary/records"


class WigleEndpointsEnum(EndpointsEnum):

    PUBLIC_WIFI = "/api/v2/network/search"


class OpenRouteServiceEndpointsEnum(EndpointsEnum):

    # DIRECTIONS_FOOT = "/v2/directions/foot-walking"
    DIRECTIONS = "/v2/directions/driving-car"
    

# class GraphHopperEndpointsEnum(EndpointsEnum):
#     DIRECTIONS = "/api/1/route"