
class SendHelpError(Exception):
    """
    Raised when the system can not support the user's request
    and the 'Help' message should be sent to explain to the 
    user how the system works.
    """
    pass