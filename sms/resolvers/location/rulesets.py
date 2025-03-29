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

class BaseLocationRuleset(ABC):
    """
    Base class for all rulesets (AddressRuleset, IntersectionRuleset, etc.).

    Provides controlled interactions with regex methods (`search`, `match`, `sub`) 
    with logging and error handling.

    Subclasses should implement rule methods that return a confidence score (float) 
    based on token evaluation.
    """
    location_type_enum: LocationType | None = None


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
    
    @staticmethod
    def detect_full_intersection(msg:str) -> tuple[str, LocationType] | None:
        if "and" not in msg and "&" not in msg:
            return None

        tokens = msg.split()
        for i, token in enumerate(tokens):
            if token in {"&", "and"} and 0 < i < len(tokens) - 1:
                before = tokens[i - 1]
                after = tokens[i + 1]
                after_after = tokens[i + 2] if i + 2 < len(tokens) else None
                after_after_after = tokens[i + 3] if i + 3 < len(tokens) else None

                if (
                    after_after in STREET_SUFFIXES or after_after in STREET_DIRECTIONS or
                    after_after_after in STREET_SUFFIXES or after_after_after in STREET_DIRECTIONS
                ):
                    return f"{before} {token} {after}", LocationType.INTERSECTION

        return None


class AddressRuleset(BaseLocationRuleset):
    
    location_type_enum = LocationType.ADDRESS

    @classmethod
    def has_preceding_number(cls, token_index:int, tokens:list[str]) -> float:
        """
        Checks if the token immediately before the current one is a number.
        """
        return 1.0 if token_index > 0 and tokens[token_index - 1].isdecimal() else 0.0

    @classmethod
    def has_proceeding_suffix(cls, token_index:int, tokens:list[str]) -> float:
        """
        Checks if the token immediately after the current one is a street suffix.
        st/rd/ave/blvd/street/avenue/...etc
        """
        return 1.0 if token_index < len(tokens) - 1 and tokens[token_index + 1] in STREET_SUFFIXES else 0.0

    @classmethod
    def has_proceeding_direction(cls, token_index:int, tokens:list[str]) -> float:
        """
        Checks if the token immediately after the current one is a street direction.
        n/e/w/s/nw/ne/sw/se/north/northeast/...etc
        """
        return 1.0 if token_index < len(tokens) - 1 and tokens[token_index + 1] in STREET_DIRECTIONS else 0.0


class IntersectionRuleset(BaseLocationRuleset):
    
    location_type_enum = LocationType.INTERSECTION

    @classmethod
    def is_potential_intersection(cls, token_index: int, tokens: list[str]) -> float:
        if tokens[token_index] not in {"&", "and"}:
            return 0.0
        
        if 0 < token_index < len(tokens) - 1:
            before = tokens[token_index - 1]
            after = tokens[token_index + 1]
            after_after = tokens[token_index + 2] if token_index + 2 < len(tokens) else None
            after_after_after = tokens[token_index + 3] if token_index + 3 < len(tokens) else None
            if before in STREET_SUFFIXES or before in STREET_DIRECTIONS:
                return 1.0
            elif after_after in STREET_SUFFIXES or after_after in STREET_DIRECTIONS:
                return 1.0
            elif after_after_after in STREET_SUFFIXES or after_after_after in STREET_DIRECTIONS:
                return 1.0
            elif before not in JUNK_WORDS and after not in JUNK_WORDS:
                return 0.5
        return 0.0


class LandmarkRuleset(BaseLocationRuleset):

    location_type_enum = LocationType.LANDMARK