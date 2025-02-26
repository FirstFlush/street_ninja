import logging
from typing import Any
from django.conf import settings
from common.enums import HttpMethodEnum
from common.utils import coord_string
from integrations.clients import OpenRouteServiceAPIClient
from integrations.clients.enums import OpenRouteServiceEndpointsEnum
from integrations.exc import IntegrationServiceError
from integrations.integration_service import IntegrationService, IntegrationServiceParams
from integrations.serializers import OpenRouteServiceSerializer
from sms.response.dataclasses import SMSFollowUpResponseData
from sms.response.response_templates import DirectionsTemplate
from .base_handler import FollowUpHandlerWithParams
from ..dataclasses import FollowUpContext
from ..exc import SendHelpError

logger = logging.getLogger(__name__)


class DirectionsHandler(FollowUpHandlerWithParams):
    

    @property
    def directions_text(self) -> str:
        if isinstance(self.directions, list):
            return "\n".join([f"{step['instruction']} for {step['distance']}m" for step in self.directions])
        else:
            logger.error(f"DirectionsHandler.directions_text is using invalid self.directions attribute: `{self.directions}` Defaulting to empty string.")
            return ""

    def __init__(self, context: FollowUpContext):
        super().__init__(context=context)
        self.directions: list[dict[str, str|float]] | None = None

    def build_response_data(self) -> SMSFollowUpResponseData:
        return SMSFollowUpResponseData(
            template=DirectionsTemplate(
                start_text=self.sms_inquiry.location_text,
                resource=self.resource
            ),
            msg=self.directions_text,
        )

    def set_directions(self, start_coords: str):
        try:
            self.directions = self._fetch_directions(start_coords)
        except Exception as e:
            msg = f"Unexpected `{e.__class__.__name__}` while fetching directions"
            logger.error(msg, exc_info=True)
            raise SendHelpError(msg) from e


    def _fetch_directions(self, start_coords: str) -> list[str]:
        params = self._build_ors_params(start_coords=start_coords)
        integration_service = self._init_ors(params=params)
        try:
            directions = integration_service.fetch()
        except IntegrationServiceError as e:
            msg = f"`{e.__class__.__name__}` while fetching directions in `{self.__class__.__name__}`"
            logger.error(msg, exc_info=True)
            raise e
        else:
            if directions:
                logger.info(f"Directions found: `{len(directions)}` steps.")
        return directions


    def _build_ors_params(self, start_coords: str) -> IntegrationServiceParams:
        """Builds the required config data for the OpenRouteService API"""
        params = IntegrationServiceParams(
            api_client_class=OpenRouteServiceAPIClient,
            endpoint_enum=OpenRouteServiceEndpointsEnum.DIRECTIONS,
            http_method_enum=HttpMethodEnum.GET,
            serializer_class=OpenRouteServiceSerializer,
            api_key=settings.OPEN_ROUTE_SERVICE_TOKEN,
            http_params={
                "start": start_coords,
                "end": coord_string(self.resource.location),
                "instructions": True,
            }
        )
        logger.info("IntegrationServiceParams built in DirectionsHandler")
        return params

    def _init_ors(self, params: IntegrationServiceParams) -> IntegrationService:
        """
        Initializes IntegrationService with the required params for OpenRouteService's API.
        """
        integration_service = IntegrationService(params=params)
        logger.info("Successfully initialized IntegrationService for OpenRouteService API call")
        return integration_service