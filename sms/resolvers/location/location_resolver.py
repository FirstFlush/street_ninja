
import logging
from typing import Any, Callable
from common.enums import LocationType
from .location_rulesets import (
    AddressRuleset, 
    IntersectionRuleset, 
    LandmarkRuleset,
    PriorityRuleset
)
from ..base_resolver import BaseKeywordResolver

logger = logging.getLogger(__name__)


class LocationResolver(BaseKeywordResolver):

    RULES = [
        AddressRuleset.has_preceding_number,
        AddressRuleset.has_proceeding_suffix,
        AddressRuleset.has_proceeding_direction,
        IntersectionRuleset.is_potential_intersection,
    ]
    RULES_PRIORITY = [
        PriorityRuleset.detect_full_address,
        PriorityRuleset.detect_landmark,
    ]


    def try_rules(self):
        for i, token in enumerate(self.tokens):
            for rule in self.RULES:
                score = rule(token_index=i, tokens=self.tokens)
                if score > 0:
                    ...

    def try_rules_priority(self) -> tuple[str, LocationType] | None:
        for rule in self.RULES_PRIORITY:
            result = rule(msg=self.msg)
            if isinstance(result, tuple):
                return result

    def _build_scoreboard(self) -> dict[int, dict[LocationType, float]]:
        """
        Initializes a scoreboard to track location type scores for each token.

        Returns:
            dict[int, dict[LocationType, float]]:
                A nested dictionary where:
                - The outer dictionary maps `token_index` (int) to a dictionary of scores.
                - The inner dictionary maps `LocationType` enums to their respective scores (float), initialized to 0.

        Example:
            {
                0: {LocationType.ADDRESS: 0.0, LocationType.INTERSECTION: 0.0, LocationType.LANDMARK: 0.0},
                1: {LocationType.ADDRESS: 0.0, LocationType.INTERSECTION: 0.0, LocationType.LANDMARK: 0.0},
                2: {LocationType.ADDRESS: 0.0, LocationType.INTERSECTION: 0.0, LocationType.LANDMARK: 0.0}
            }

        This structure is used to accumulate rule-based scoring for each token,
        allowing the system to determine the most likely location type based on the highest score.
        """
        return {
            token_index: {
                LocationType.ADDRESS: 0,
                LocationType.INTERSECTION: 0,
                LocationType.LANDMARK: 0
            }
            for token_index in range(len(self.tokens))
        }

    def __init__(self, msg:str):
        self.msg = msg
        self.tokens = self._tokenize_msg(msg, keep_ampersand=True)
        self.scoreboard = self._build_scoreboard()