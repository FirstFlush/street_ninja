from .base_response_templates import GeneralResponseTemplate
from resources.abstract_models import ResourceModel


class DirectionsTemplate(GeneralResponseTemplate):

    def __init__(self, start_text:str, resource: ResourceModel):
        self.start_text = start_text
        self.resource = resource

    def _header(self) -> str:
        return f'Directions from "{self.start_text}"'

    def wrap_response(self, msg:str, new_session: bool = False) -> str:
        return f"{self._header()}\n\n{self.resource.keyword_enum.value.title()}\n{self.resource.resource_name}\n\n{msg}"