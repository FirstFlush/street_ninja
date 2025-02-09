from dataclasses import dataclass
from .base_response_templates import FollowUpResponseTemplate


@dataclass
class DirectionsResponseTemplate(FollowUpResponseTemplate):
    ...


@dataclass
class InfoResponseTemplate(FollowUpResponseTemplate):
    ...


