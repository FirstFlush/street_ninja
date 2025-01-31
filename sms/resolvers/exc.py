

class KeywordResolverError(Exception):
    """Raised when SMS keyword can not be determined."""
    pass

class LocationResolutionError(Exception):
    """Raised when a location can not be determined"""
    pass

class ParamResolutionError(Exception):
    """Raised when there is any error resolving params. Should not happen."""
    pass

class SMSResoltuionError(Exception):
    """Raised when the SMS resolver fails."""
    pass