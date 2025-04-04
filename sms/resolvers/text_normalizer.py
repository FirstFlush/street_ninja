import re
import logging


logger = logging.getLogger(__name__)


class TextNormalizer:
    """
    Handles normalization of data received in text messages,
    and enforces the same rules on param mappings.
    """
    def __init__(self, keep_ampersand: bool = False, keep_dash: bool = False):
        """
        - keep_ampersand: preserves '&' for intersection detection (e.g. "Main & Hastings")
        - keep_dash: preserves or replaces dashes (e.g. "11-132 Hastings")
        """
        self.keep_ampersand = keep_ampersand
        self.keep_dash = keep_dash
        self.pattern = self._build_regex_pattern()

    def _build_regex_pattern(self) -> str:
        return r"[^a-zA-Z0-9\u4e00-\u9fff\u0a00-\u0a7f\s&'#/]" if self.keep_ampersand \
            else r"[^a-zA-Z0-9\u4e00-\u9fff\u0a00-\u0a7f\s'#/]"

    def tokenize_text(self, text: str) -> list[str]:
        if isinstance(text, str):
            cleaned = self._strip_special_chars(text)
            return cleaned.lower().split()
        else:
            msg = f"`text` must be of type str or str. Value recieve `{text}`"
            logger.error(msg)
            raise TypeError(msg)
        
    def tokenize_list(self, untokenized_list: list[str]) -> list[str]:
        if isinstance(untokenized_list, list) and all(isinstance(i, str) for i in untokenized_list):
            return self.tokenize_text(", ".join(untokenized_list))
        else:
            msg = f"`token` must be of type str or list[str]. Value received: `{untokenized_list}`"
            logger.error(msg)
            raise TypeError(msg)

    def _strip_special_chars(self, text: str) -> str:
        # Remove '#' unless followed by a digit
        text = re.sub(r"(?<!\w)#(?!\d)", "", text)

        if self.keep_dash:
            text = text.replace('-', ' ')
        else:
            text = text.replace('-', '')

        return re.sub(self.pattern, '', text)


