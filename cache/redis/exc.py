

class RedisClientException(Exception):
    """Raised when the Redis Client fails"""
    pass


class InvalidAccessPattern(Exception):
    """Raised when an invalid access pattern is used"""
    pass