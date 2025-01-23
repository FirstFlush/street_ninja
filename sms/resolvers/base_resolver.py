from abc import ABC
import re


class BaseKeywordResolver(ABC):

    @classmethod
    def _prepare_words(cls, msg:str) -> list[str]:
        return cls._strip_special_chars(msg).lower().split()
    
    @staticmethod

    def _strip_special_chars(text:str) -> str:
        return re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff\u0a00-\u0a7f\s]', '', text)