from celery import shared_task
import logging
from .email_service import EmailService
from .enums import EmailRouteEnum
from .exc import SendEmailError


logger = logging.getLogger(__name__)


@shared_task
def send_directions_routing_failure_email(url: str, exception_name: str, trace: str):
    try:
        EmailService.send_email_directions(url=url, exception_name=exception_name, trace=trace)
    except SendEmailError:
        logger.error(f"Failed to send email for directions routing failure!", exc_info=True)


@shared_task
def send_celery_beat_failure_email(url: str, resource: str, exception_name: str, trace: str):
    try:
        EmailService.send_email_celery_beat(
            resource=resource,
            url=url,
            exception_name=exception_name,
            trace=trace,
        )
    except SendEmailError:
        logger.error(f"Failed to send email for celery-beat failure!", exc_info=True)


@shared_task
def send_sms_resolution_failed_email(message: str):
    try:
        EmailService(EmailRouteEnum.LOCATION_PARSING).send_email(
            subject="SMS resolution failed",
            message=message,
        )
    except SendEmailError:
        logger.error(f"Failed to send email for SMS resolution failure!", exc_info=True)

@shared_task
def send_geocoding_failed_email(message: str):
    try:
        EmailService(EmailRouteEnum.LOCATION_PARSING).send_email(
            subject="Geocoding failed",
            message=message,
        )
    except SendEmailError:
        logger.error(f"Failed to send email for geocoding failure!", exc_info=True)