import logging
import traceback
from .integration_service import IntegrationService, IntegrationServiceParams
from notifications.tasks import send_celery_beat_failure_email


logger = logging.getLogger(__name__)


class ResourceFetcher:
    """
    Handles the standardized fetch-and-save flow for integration tasks.

    This class is used by Celery tasks to retrieve data from third-party APIs,
    serialize it, and persist it to the database using the IntegrationService.

    It centralizes error handling, logging, and optional email notifications
    when failures occur, ensuring consistent behavior across all resource-fetching
    tasks.

    Usage:
        params = IntegrationServiceParams(...)
        ResourceFetcher(params).run()
    """
    def __init__(self, params: IntegrationServiceParams):
        self.params = params
        self.integration_service = IntegrationService(params)

    def _logger_msg(self, e: Exception):
        return f"`{e.__class__.__name__}` while attempting to fetch data from `{self.params.url}`"

    def run(self, email_on_error: bool=True):
        try:
            self.integration_service.fetch_and_save()
        except Exception as e:
            if email_on_error:
                trace = traceback.format_exc()
                send_celery_beat_failure_email.delay(
                    resource=self.params.endpoint_enum.value,
                    url=self.params.url,
                    exception_name=e.__class__.__name__,
                    trace=trace,
                )
            logger.error(self._logger_msg(e), exc_info=True)
            raise

