from abc import ABC, abstractmethod
from ..response_templates import QuerySetResponseTemplate
from ..dataclasses import SMSInquiryResponseData
from ..response_templates import WelcomeResponseTemplate



class BaseResponseWrapper(ABC):

    def __init__(self, response_data: SMSInquiryResponseData, new_session: bool = False):
        self.response_data = response_data 
        self.new_session = new_session





    abstractmethod
    def top(self) -> str:
        ...

    abstractmethod
    def bottom(self) -> str:
        ...


class QuerySetResponseWrapper(BaseResponseWrapper):

    def __init__(self, template: QuerySetResponseTemplate, response_data: SMSInquiryResponseData, new_session: bool = False):
        self.template = template
        super().__init__(response_data=response_data, new_session=new_session)


    def create_complete_response(self) -> str:
        if self.new_session:
            self.welcome_template = WelcomeResponseTemplate()
            top = self._welcome_top()
            bottom = self._welcome_bottom()
        else:
            top = self._top()
            bottom = self._bottom()
        return f"{top}\n{self.response_data.msg}\n{bottom}"


    def _welcome_top(self) -> str:
        return f"{self.welcome_template.HEADER}\n{self.template.TITLE}"

    def _welcome_bottom(self) -> str:
        return f"{self.welcome_template.FOOTER}"

    def _top(self) -> str:
        return self.template.TITLE

    
    def _bottom(self) -> str:
        return self.template.FOOTER


class GeneralResponseWrapper(BaseResponseWrapper):

    
    def top(self) -> str:
        ...

    
    def bottom(self) -> str:
        ...