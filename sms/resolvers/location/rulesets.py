from abc import ABC
import re
from common.enums import LocationType
from sms.enums import SMSKeywordEnum
from .location_data import (
    STREET_SUFFIXES, 
    STREET_DIRECTIONS, 
    JUNK_WORDS, 
    VANCOUVER_LANDMARKS
)
from .regex_library import RegexLibrary
from .token_navigator import TokenNavigator


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
    def detect_neighborhood(msg: str) -> tuple[str, LocationType] | None:
        ...


    @staticmethod
    def detect_landmark(msg: str) -> tuple[str, LocationType] | None:
        normalized_msg = re.sub(RegexLibrary.normalize_string, "", msg).lower().replace(" ", "")
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

        if msg.isalpha():
            tokens = re.sub(RegexLibrary.normalize_string, "", msg).split()
            nav = TokenNavigator(tokens)
            for i, token in enumerate(tokens):
                if token not in {"&", "and"}:
                    continue
                if i == 0 or i >= len(tokens) - 1:
                    continue

                before = nav.get_before(i)
                after = nav.get_after(i)

                # Skip if either side is junky
                if before and before.lower() in JUNK_WORDS:
                    continue
                if after and after.lower() in JUNK_WORDS:
                    continue

                left_phrase = PriorityRuleset._backwards(nav, i)
                right_phrase = PriorityRuleset._forwards(nav, i)

                if left_phrase and right_phrase:
                    return f"{left_phrase} {token} {right_phrase}", LocationType.INTERSECTION

        return None

    @staticmethod
    def _backwards(nav: TokenNavigator, and_index: int) -> str:
        tokens = []
        
        # step 1: suffix (e.g., "ave")
        suffix = nav.get_before(and_index)
        if not suffix or suffix.lower() in JUNK_WORDS:
            return ""

        tokens.insert(0, suffix)

        # step 2: ordinal or numeric (e.g., "34th", "33")
        street_number = nav.get_before(and_index, count=2)
        if street_number and re.match(r"^\d+(st|nd|rd|th)?$", street_number.lower()):
            tokens.insert(0, street_number)

            # optional: direction before number
            direction = nav.get_before(and_index, count=3)
            if direction and direction.lower() in STREET_DIRECTIONS:
                tokens.insert(0, direction)

        return " ".join(tokens)
    

    @staticmethod
    def _forwards(nav: TokenNavigator, and_index: int) -> str:
        tokens = []

        # Step 1: grab possible street name
        first = nav.get_after(and_index, count=1)
        if not first or first.lower() in JUNK_WORDS:
            return ""

        tokens.append(first)

        # Step 2: grab suffix
        second = nav.get_after(and_index, count=2)
        if not second or second.lower() not in STREET_SUFFIXES:
            return " ".join(tokens)  # no suffix, stop early

        tokens.append(second)

        # Step 3: optional direction
        third = nav.get_after(and_index, count=3)
        if third and third.lower() in STREET_DIRECTIONS:
            tokens.append(third)

        return " ".join(tokens)




    # @staticmethod
    # def detect_full_intersection(msg: str) -> tuple[str, LocationType] | None:
    #     tokens = msg.split()
    #     token_nav = TokenNavigator(tokens)

    #     for i, token in enumerate(tokens):
    #         if token not in {"&", "and"}:
    #             continue
    #         if i == 0 or i == len(tokens) - 1:
    #             continue  # can't form intersection if '&' is at start or end

    #         before = token_nav.get_before(i)
    #         after_tokens = token_nav.get_window(i, after=3)[1:]  # skip '&' itself
    #         after_phrase = " ".join(after_tokens).strip()

    #         # Skip if before or early after tokens are junk
    #         if before and before.lower() in JUNK_WORDS:
    #             continue
    #         if any(t.lower() in JUNK_WORDS for t in after_tokens[:2]):
    #             continue

    #         # Suffix/direction heuristic (strong signal)
    #         before_is_suffix = before and before.lower() in STREET_SUFFIXES
    #         after_has_suffix = any(t.lower() in STREET_SUFFIXES for t in after_tokens)
    #         after_has_direction = any(t.lower() in STREET_DIRECTIONS for t in after_tokens)

    #         if before_is_suffix or after_has_suffix or after_has_direction:
    #             return f"{before} {token} {after_phrase}", LocationType.INTERSECTION

    #         # Weak fallback: both sides look like plausible street words
    #         if before and before.isalpha() and after_tokens and after_tokens[0].isalpha():
    #             return f"{before} {token} {after_phrase}", LocationType.INTERSECTION

    #     return None

    # @staticmethod
    # def detect_full_intersection(msg: str) -> tuple[str, LocationType] | None:
    #     tokens = msg.split()

    #     for i, token in enumerate(tokens):
    #         if token not in {"&", "and"}:
    #             continue
    #         if i == 0 or i == len(tokens) - 1:
    #             continue  # can't have an intersection at the start or end

    #         before = tokens[i - 1]
    #         after_tokens = tokens[i + 1 : i + 4]  # up to 3 tokens after
    #         after_phrase = " ".join(after_tokens).strip()

    #         # Skip if before or early after tokens are junk
    #         if before.lower() in JUNK_WORDS:
    #             continue
    #         if any(t.lower() in JUNK_WORDS for t in after_tokens[:2]):
    #             continue

    #         # Match: either side has suffix/direction (strong intersection signal)
    #         before_is_suffix = before.lower() in STREET_SUFFIXES
    #         after_has_suffix = any(t.lower() in STREET_SUFFIXES for t in after_tokens)
    #         after_has_direction = any(t.lower() in STREET_DIRECTIONS for t in after_tokens)

    #         if before_is_suffix or after_has_suffix or after_has_direction:
    #             intersection_text = f"{before} {token} {after_phrase}"
    #             return intersection_text, LocationType.INTERSECTION

    #         # Fallback: both sides look like real words (we'll take a guess)
    #         if before.isalpha() and after_tokens and after_tokens[0].isalpha():
    #             intersection_text = f"{before} {token} {after_phrase}"
    #             return intersection_text, LocationType.INTERSECTION

    #     return None



    # @staticmethod
    # def detect_full_intersection(msg: str) -> tuple[str, LocationType] | None:
    #     tokens = msg.split()

    #     for i, token in enumerate(tokens):
    #         if token not in {"&", "and"}:
    #             continue
    #         if i == 0 or i == len(tokens) - 1:
    #             continue

    #         before = tokens[i - 1]
    #         after_tokens = tokens[i + 1 : i + 4]  # up to 3 tokens after
    #         after_phrase = " ".join(after_tokens).strip()

    #         # Heuristic: if before/after are real words and not junk
    #         if before.lower() in JUNK_WORDS:
    #             continue
    #         if any(t in JUNK_WORDS for t in after_tokens[:2]):
    #             continue

    #         # If either before or after phrase has suffix/direction, it's enough
    #         if (
    #             before in STREET_SUFFIXES or
    #             any(t in STREET_SUFFIXES or t in STREET_DIRECTIONS for t in after_tokens)
    #         ):

    #             return f"{before} {token} {after_phrase}", LocationType.INTERSECTION

    #         # If both sides are alphanumeric and not junk, still might be an intersection
    #         if before.isalpha() and after_tokens and after_tokens[0].isalpha():

    #             return f"{before} {token} {after_phrase}", LocationType.INTERSECTION

    #     return None



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


class NeighborhoodRuleset(BaseLocationRuleset):

    location_type_enum = LocationType.NEIGHBORHOOD

    @classmethod
    def is_potential_neighborhood(cls, token_index: int, tokens: list[str]):
        s = " ".join(tokens)
        