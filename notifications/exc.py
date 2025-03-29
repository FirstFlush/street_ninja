
class SendEmailError(Exception):
    """Raised when EmailService fails to send an email"""
    pass


class SuspiciousEmailError(Exception):
    """Raised when the EmailService tries to send an email to a domain that isn't explicitly Street Ninja's domain"""
    pass