from abc import ABC
import re
from common.enums import LocationType
from .location_data import (
    STREET_SUFFIXES, 
    STREET_DIRECTIONS, 
    JUNK_WORDS, 
    VANCOUVER_LANDMARKS
)
from .regex_library import RegexLibrary
from .enums import StreetSuffixEnum, StreetDirectionEnum


# class BaseRuleset:
#     def __init_subclass__(cls):
#         """
#         Ensure all static methods of subclasses match the method signature:
#         (token_index: int, tokens: list[str]) -> float
#         """
#         for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
#             if not name.startswith("_") and isinstance(getattr(cls, name, None), staticmethod):
#                 sig = inspect.signature(method)
#                 params = list(sig.parameters.values())

#                 if (
#                     len(params) != 2 or  # No `self`, so only 2 params now
#                     params[0].annotation != int or
#                     params[1].annotation != list[str]
#                 ):
#                     raise TypeError(f"Method `{name}` in {cls.__name__} must have "
#                                     f"signature (token_index: int, tokens: list[str]) -> float")


class BaseLocationRuleset(ABC):
    """
    Base class for all rulesets (AddressRuleset, IntersectionRuleset, etc.).

    Provides controlled interactions with regex methods (`search`, `match`, `sub`) 
    with logging and error handling.

    Subclasses should implement rule methods that return a confidence score (float) 
    based on token evaluation.
    """
class PriorityRuleset(BaseLocationRuleset):

    @staticmethod
    def detect_landmark(msg: str) -> tuple[str, LocationType] | None:
        words = set(msg.split())
        matches = words & VANCOUVER_LANDMARKS
        if matches:
            return next(iter(matches)), LocationType.LANDMARK
        
    @staticmethod    
    def detect_full_address(msg: str) -> tuple[str, LocationType] | None:
        compiled_regex = re.compile(RegexLibrary.full_address)
        match = compiled_regex.search(msg)
        if match:
            return match.group(0), LocationType.ADDRESS
    

class AddressRuleset(BaseLocationRuleset):
    
    @staticmethod
    def has_preceding_number(token_index:int, tokens:list[str]) -> float:
        """
        Checks if the token immediately before the current one is a number.
        """
        return 1.0 if token_index > 0 and tokens[token_index - 1].isdecimal() else 0.0

    @staticmethod
    def has_proceeding_suffix(token_index:int, tokens:list[str]) -> float:
        """
        Checks if the token immediately after the current one is a street suffix.
        st/rd/ave/blvd/street/avenue/...etc
        """
        return 1.0 if token_index < len(tokens) - 1 and tokens[token_index + 1] in STREET_SUFFIXES else 0.0

    @staticmethod
    def has_proceeding_direction(token_index:int, tokens:list[str]) -> float:
        """
        Checks if the token immediately after the current one is a street direction.
        n/e/w/s/nw/ne/sw/se/north/northeast/...etc
        """
        return 1.0 if token_index < len(tokens) - 1 and tokens[token_index + 1] in STREET_DIRECTIONS else 0.0



class IntersectionRuleset(BaseLocationRuleset):
    
    def is_potential_intersection(token_index: int, tokens: list[str]) -> float:
        if tokens[token_index] not in {"&", "and"}:
            return 0.0
        
        if 0 < token_index < len(tokens) - 1:
            before = tokens[token_index - 1]
            after = tokens[token_index + 1]
            after_after = tokens[token_index + 2] if token_index + 2 < len(tokens) else None
            after_after_after = tokens[token_index + 3] if token_index + 3 < len(tokens) else None
            if before in STREET_SUFFIXES or before in STREET_DIRECTIONS:
                return 1.0
            if after_after in STREET_SUFFIXES or after_after in STREET_DIRECTIONS:
                return 1.0
            if after_after_after in STREET_SUFFIXES or after_after_after in STREET_DIRECTIONS:
                return 1.0
            elif before.isalpha() and after.isalpha():
                if before not in JUNK_WORDS and after not in JUNK_WORDS:
                    return 0.5
        return 0.0

class LandmarkRuleset(BaseLocationRuleset):
    ...