

class RedisClientException(Exception):
    """Raised when the Redis Client fails"""
    pass


class InvalidAccessPattern(Exception):
    """Raised when an invalid access pattern is used"""
    pass


class NoSessionFound(Exception):
    """Raised when no session has been found for the key."""
    pass