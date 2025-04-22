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

    # @staticmethod
    # def detect_landmark(msg: str) -> tuple[str, LocationType] | None:
    #     words = set(msg.split())
    #     matches = words & VANCOUVER_LANDMARKS
    #     if matches:
    #         return next(iter(matches)), LocationType.LANDMARK


    @staticmethod
    def detect_landmark(msg: str) -> tuple[str, LocationType] | None:
        normalized_msg = re.sub(RegexLibrary.normalize_string, "", msg).lower().replace(" ", "")

        if normalized_msg == "wificarnegiecenter":
            print(normalized_msg)
            print(msg)

        for landmark in VANCOUVER_LANDMARKS:
            normalized_landmark = re.sub(RegexLibrary.normalize_string, "", landmark).lower().replace(" ", "")
            if normalized_landmark in normalized_msg:

                return landmark, LocationType.LANDMARK

    @staticmethod
    def detect_full_address(msg: str) -> tuple[str, LocationType] | None:
        compiled_regex = re.compile(RegexLibrary.full_address)
        match = compiled_regex.search(msg)
        if match:
            return match.group(0), LocationType.ADDRESS
        
    @staticmethod
    def detect_full_intersection(msg: str) -> tuple[str, LocationType] | None:
        tokens = msg.split()

        for i, token in enumerate(tokens):
            if token not in {"&", "and"}:
                continue
            if i == 0 or i == len(tokens) - 1:
                continue

            before = tokens[i - 1]
            after_tokens = tokens[i + 1 : i + 4]  # up to 3 tokens after
            after_phrase = " ".join(after_tokens).strip()

            # Heuristic: if before/after are real words and not junk
            if before.lower() in JUNK_WORDS:
                continue
            if any(t in JUNK_WORDS for t in after_tokens[:2]):
                continue

            # If either before or after phrase has suffix/direction, it's enough
            if (
                before in STREET_SUFFIXES or
                any(t in STREET_SUFFIXES or t in STREET_DIRECTIONS for t in after_tokens)
            ):
                return f"{before} {token} {after_phrase}", LocationType.INTERSECTION

            # If both sides are alphanumeric and not junk, still might be an intersection
            if before.isalpha() and after_tokens and after_tokens[0].isalpha():
                return f"{before} {token} {after_phrase}", LocationType.INTERSECTION

        return None



    # @staticmethod
    # def detect_full_intersection(msg:str) -> tuple[str, LocationType] | None:
    #     if "and" not in msg and "&" not in msg:
    #         return None

    #     tokens = msg.split()
    #     for i, token in enumerate(tokens):
    #         if token in {"&", "and"} and 0 < i < len(tokens) - 1:
    #             before = tokens[i - 1]
    #             after = tokens[i + 1]
    #             after_after = tokens[i + 2] if i + 2 < len(tokens) else None
    #             after_after_after = tokens[i + 3] if i + 3 < len(tokens) else None

    #             if (
    #                 after_after in STREET_SUFFIXES or after_after in STREET_DIRECTIONS or
    #                 after_after_after in STREET_SUFFIXES or after_after_after in STREET_DIRECTIONS
    #             ):
    #                 return f"{before} {token} {after}", LocationType.INTERSECTION

    #     return None


class AddressRuleset(BaseLocationRuleset):
    
    location_type_enum = LocationType.ADDRESS

    @classmethod
    def has_preceding_number(cls, token_index:int, tokens:list[str]) -> float:
        """
        Checks if the token immediately before the current one is a number.
        """
        return 1.0 if token_index > 0 and tokens[token_index - 1].isdecimal() else 0.0

    # @classmethod
    # def has_proceeding_suffix(cls, token_index:int, tokens:list[str]) -> float:
    #     """
    #     Checks if the token immediately after the current one is a street suffix.
    #     st/rd/ave/blvd/street/avenue/...etc
    #     """
    #     return 1.0 if token_index < len(tokens) - 1 and tokens[token_index + 1] in STREET_SUFFIXES else 0.0

    @classmethod
    def has_street_suffix_nearby(cls, token_index: int, tokens: list[str]) -> float:
        before = tokens[token_index - 1] if token_index > 0 else ""
        after = tokens[token_index + 1] if token_index + 1 < len(tokens) else ""
        return 1.0 if before in STREET_SUFFIXES or after in STREET_SUFFIXES else 0.0
    
    # @classmethod
    # def has_proceeding_direction(cls, token_index:int, tokens:list[str]) -> float:
    #     """
    #     Checks if the token immediately after the current one is a street direction.
    #     n/e/w/s/nw/ne/sw/se/north/northeast/...etc
    #     """
    #     return 1.0 if token_index < len(tokens) - 1 and tokens[token_index + 1] in STREET_DIRECTIONS else 0.0

    @classmethod
    def has_street_direction_nearby(cls, token_index: int, tokens: list[str]) -> float:
        before = tokens[token_index - 1] if token_index > 0 else ""
        after = tokens[token_index + 1] if token_index + 1 < len(tokens) else ""
        return 1.0 if before in STREET_DIRECTIONS or after in STREET_DIRECTIONS else 0.0



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