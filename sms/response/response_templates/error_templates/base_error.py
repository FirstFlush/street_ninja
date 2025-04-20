from ..base_response_templates import BaseSMSResponseTemplate


class BaseErrorResponseTemplate(BaseSMSResponseTemplate):

    @classmethod
    def msg(cls, msg: str | None=None) -> str:
        raise NotImplementedError(f"{cls.__name__} must implement msg() method.")