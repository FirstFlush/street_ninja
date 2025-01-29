from abc import ABC
import re


class BaseKeywordResolver(ABC):

    @classmethod
    def _tokenize_msg(cls, msg:str, keep_ampersand:bool=False) -> list[str]:
        return cls._strip_special_chars(msg, keep_ampersand).lower().split()
    
    @staticmethod
    def _strip_special_chars(text: str, keep_ampersand: bool = False) -> str:
        """
        Strips out most non-alphanumeric characters but:
        - Keeps '&' if `keep_ampersand=True`
        - Replaces '-' with a space (to prevent merging numbers)
        - Preserves '#' if it's attached to a number (e.g., "#305")
        - Preserves apostrophes in words (e.g., "O'Reilly")
        """
        pattern = r"[^a-zA-Z0-9\u4e00-\u9fff\u0a00-\u0a7f\s&'#/]" if keep_ampersand else r"[^a-zA-Z0-9\u4e00-\u9fff\u0a00-\u0a7f\s'#/]"
        
        # Keep '#' only if it's part of "#123" (apartment/unit numbers)
        text = re.sub(r"(?<!\w)#(?!\d)", "", text)  # Removes '#' unless followed by a digit
        
        return re.sub(pattern, '', text.replace('-', ' '))