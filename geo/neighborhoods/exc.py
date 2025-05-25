
class NeighborhoodServiceError(Exception):
    """Raised whent he NeighborhoodService fails to fetch/validate/save neighborhood data."""
    pass

class NeighborhoodFileError(Exception):
    """
    Raised when the JSON model dump of Vancouver Neighborhood objects isn't 
    found or has an error while loading.
    """
    pass