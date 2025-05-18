

class IntegrationServiceError(Exception):
    """Raised when the IntegrationService class fails to validate or save data."""
    pass

class NeighborhoodServiceError(Exception):
    """Raised whent he NeighborhoodService fails to fetch/validate/save neighborhood data."""
    pass