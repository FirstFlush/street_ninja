from abc import ABC, abstractmethod
from .token_navigator import TokenNavigator
from .location_data import (
    VANCOUVER_LANDMARKS, 
    JUNK_WORDS, 
    STREET_DIRECTIONS, 
    STREET_SUFFIXES
)

class BaseExpander(ABC):

    def __init__(self, token_navigator: TokenNavigator):
        self.token_navigator = token_navigator

    @abstractmethod
    def expand_outward(self, token_index:int) -> str:
        ...

    def _token_value(self, token_index: int) -> str:
        return self.token_navigator.tokens[token_index]


class AddressExpander(BaseExpander):

    def expand_outward(self, token_index:int) -> str:
        backwards = self._backwards(token_index)
        forwards = self._forwards(token_index)
        return f"{backwards} {self._token_value(token_index)} {forwards}"

    def _backwards(self, token_index: int) -> str:
        """
        Expands backward to capture the full address number if present.
        Handles cases like:
        - "104 Hastings"
        - "A-321 Main"
        - "#7-104 Main"
        """
        collected_tokens = []
        for step in range(1, 3):  # Look up to two tokens back
            before = self.token_navigator.get_before(token_index, count=step)
            if before is None:
                break
            if before.isalnum() and before not in JUNK_WORDS:
                collected_tokens.insert(0, before)  # Insert at the beginning
            if before.isdecimal():
                possible_prefix = self.token_navigator.get_before(token_index, count=step+1)
                if possible_prefix is not None and possible_prefix in STREET_DIRECTIONS:
                    collected_tokens.insert(0, possible_prefix)
                break

        return " ".join(collected_tokens)

    def _forwards(self, token_index: int) -> str:
        collected_tokens = []
        for step in range(1, 4):  # Look up to 3 tokens forward
            after = self.token_navigator.get_after(token_index, count=step)
            if after is None or after in JUNK_WORDS:
                break
            if step >= 2:
                if after not in STREET_SUFFIXES and after not in STREET_DIRECTIONS:
                    break
            if after.isalnum():
                collected_tokens.append(after)
        return " ".join(collected_tokens)


class IntersectionExpander(BaseExpander):

    def expand_outward(self, token_index:int) -> str:
        backwards = self._backwards(token_index)
        forwards = self._forwards(token_index)
        return f"{backwards} {self._token_value(token_index)} {forwards}"

    def _backwards(self, token_index:int) ->str:

        collected_tokens = []
        for step in range(1, 5):
            before = self.token_navigator.get_before(token_index, count=step)
            if before is None:
                break
            collected_tokens.insert(0, before)
            
        max_length = 4
        tokens_set = set(collected_tokens)
        if not tokens_set & STREET_SUFFIXES:
            max_length -= 1
        if not tokens_set & STREET_DIRECTIONS:
            max_length -= 1
        if len(collected_tokens) > max_length:
            collected_tokens = collected_tokens[-max_length:]

        return " ".join(collected_tokens)
    
    def _forwards(self, token_index:int) ->str:
        """
        Expands forward from an intersection keyword ("&" or "and").
        - Captures alphanumeric tokens.
        - Stops at a street suffix (e.g., "St", "Ave"), but allows one optional street direction (e.g., "NW").
        - If no suffix or direction is found, takes only the first token (if it's not junk).
        """
        collected_tokens = []
        for step in range(1, 4):
            after = self.token_navigator.get_after(token_index, count=step)
            if after is None:
                break
            collected_tokens.append(after)
            if after in STREET_SUFFIXES:
                possible_direction = self.token_navigator.get_after(token_index, count=step + 1)
                if possible_direction and possible_direction in STREET_DIRECTIONS:
                    collected_tokens.append(possible_direction)
                break
        max_length = 3
        tokens_set = set(collected_tokens)
        if not tokens_set & STREET_SUFFIXES:
            max_length -= 1
        if not tokens_set & STREET_DIRECTIONS:
            max_length -= 1
        if len(collected_tokens) > max_length:
            collected_tokens= collected_tokens[:max_length]

        return " ".join(collected_tokens)

class LandmarkExpander(BaseExpander):

    def expand_outward(self, token_index:int) -> str:
        return self._token_value(token_index)




