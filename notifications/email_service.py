import logging
from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from .enums import EmailRouteEnum
from .exc import SendEmailError, SuspiciousEmailError


logger = logging.getLogger(__name__)


class EmailService:

    EMAIL_HOST_USER = settings.EMAIL_HOST_USER
    EMAIL_PORT = settings.EMAIL_PORT
    EMAIL_HOST = settings.EMAIL_HOST
    EMAIL_APP_PASSWORD = settings.EMAIL_HOST_PASSWORD
    EMAIL_USE_TLS = settings.EMAIL_USE_TLS

    def __init__(self, route_enum: EmailRouteEnum):
        self.route_enum = route_enum
        self._security_check()

    def _security_check(self):
        if not self.to_email.endswith(settings.STREET_NINJA_DOMAIN):
            msg = f"Suspicious email recipient detected: `{self.to_email}`"
            logger.error(msg)
            raise SuspiciousEmailError(msg)

    def _preview_email(self, subject: str, message: str, fail_silently: bool):
        """
        Prints email details to the terminal instead of sending the actual email.
        Used when DEBUG=True in settings.py so I don't flood my inbox in development.
        """
        print()
        print("="*50)
        print("[DEV EMAIL PREVIEW]")
        print()
        print(f"From: {self.from_email}",)
        print(f"To: {self.to_email}")
        print()
        print(f"Subject: {subject}")
        print()
        print("Message:")
        print(message)
        print()
        print(f"Fail silently: {fail_silently}")
        print()
        print("="*50)
        print()

    @property
    def from_email(self) -> str:
        return settings.EMAIL_HOST_USER

    @property
    def to_email(self) -> str:
        return f"{self.route_enum.value}@{settings.STREET_NINJA_DOMAIN}"

    def send_email(self, message: str, subject: str, fail_silently: bool=False):
        if settings.DEBUG:
            self._preview_email(
                subject=subject, 
                message=message, 
                fail_silently=fail_silently
            )
        else:
            try:
                django_send_mail(
                    subject=subject,
                    message=message,
                    from_email=self.from_email,
                    recipient_list=[self.to_email],
                    fail_silently=fail_silently,
                )
            except Exception as e:
                msg = f"Failed to send email due to unexpected error: `{e.__class__.__name__}`"
                logger.error(msg, exc_info=True)
                raise SendEmailError(msg) from e