


class AllGeocodersFailed(Exception):
    """Raised when all geocoders failed to determine a location for the given input."""
    pass


class GeospatialException(Exception):
    """Raised when the GeospatialService fails to sort the queryset objects by distance."""
    pass