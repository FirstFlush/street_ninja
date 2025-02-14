from .base_response_templates import GeneralResponseTemplate


class DirectionsTemplate(GeneralResponseTemplate):

    def wrap_response(self, msg:str, new_session: bool = False) -> str:
        return msg
