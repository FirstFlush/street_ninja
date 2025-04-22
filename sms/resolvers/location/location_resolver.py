from dataclasses import dataclass
import logging
from common.enums import LocationType
from .rulesets import (
    AddressRuleset, 
    IntersectionRuleset, 
    LandmarkRuleset,
    PriorityRuleset
)
from ..exc import LocationResolutionError
from .expanders import BaseExpander, AddressExpander, IntersectionExpander, LandmarkExpander
from .token_navigator import TokenNavigator
from ..base_resolver import BaseKeywordResolver

logger = logging.getLogger(__name__)


@dataclass
class ResolvedLocation:
    location: str
    location_type: LocationType


class LocationResolver(BaseKeywordResolver):

    RULES_COMMON = [
        AddressRuleset.has_preceding_number,
        AddressRuleset.has_street_direction_nearby,
        AddressRuleset.has_street_suffix_nearby,
        IntersectionRuleset.is_potential_intersection,
    ]
    RULES_PRIORITY = [
        PriorityRuleset.detect_full_address,
        PriorityRuleset.detect_full_intersection,
        PriorityRuleset.detect_landmark,
    ]
    LOCATION_TYPE_TO_EXPANDER: dict[LocationType, BaseExpander] = {
        LocationType.ADDRESS : AddressExpander,
        LocationType.INTERSECTION : IntersectionExpander,
        LocationType.LANDMARK : LandmarkExpander,
    }

    @classmethod
    def resolve_location(cls, msg:str) -> ResolvedLocation:
        instance = cls(msg=msg)
        try:
            return instance._resolve_location()
        except Exception as e:
            logger.error(f"LocationResolutionError for msg: `{msg}` from: {e}")
            raise LocationResolutionError(f"Could not resolve location for msg: `{msg}`") from e

    def __init__(self, msg:str):
        self.msg = msg
        self.tokens = self._tokenize_msg(msg, keep_ampersand=True)
        self.scoreboard = self._build_scoreboard()
        self.token_navigator = TokenNavigator(tokens=self.tokens)

    def _get_expander(
            self, 
            location_type_enum: LocationType,
            token_navigator: TokenNavigator,
    ) -> BaseExpander:
        """Factory method for building the Expander object"""
        expander = self.LOCATION_TYPE_TO_EXPANDER[location_type_enum]
        return expander(token_navigator=token_navigator)

    def _resolve_location(self) -> ResolvedLocation:
        resolved_location = self._try_rules_priority()
        if resolved_location:
            return resolved_location
        
        self._try_rules_common()
        hot_token, location_type_enum = self._analyze_scoreboard()
        expander = self._get_expander(
            location_type_enum=location_type_enum,
            token_navigator=self.token_navigator,
        )
        location = expander.expand_outward(token_index=hot_token)
        return ResolvedLocation(
            location=location,
            location_type=location_type_enum
        )

    def _analyze_scoreboard(self) -> tuple[int, LocationType]:
        """
        Determines the 'hot token' (most confident location word)
        and the dominant LocationType (Address, Intersection, or Landmark).
        """
        best_token_index = None
        best_location_type = None
        best_score = 0.0  # Keep track of the highest confidence score

        for token_index, scores in self.scoreboard.items():
            for location_type, score in scores.items():
                if score > best_score:  # Found a new best
                    best_score = score
                    best_token_index = token_index
                    best_location_type = location_type
                elif score == best_score:
                    # Tie-breaking logic: Address > Intersection > Landmark
                    if best_location_type in {LocationType.LANDMARK, LocationType.INTERSECTION} and location_type == LocationType.ADDRESS:
                        best_token_index = token_index
                        best_location_type = location_type

        return best_token_index, best_location_type

    def _try_rules_common(self):
        for i, _ in enumerate(self.tokens):
            for rule in self.RULES_COMMON:
                score = rule(token_index=i, tokens=self.tokens)
                location_type_enum = rule.__self__.location_type_enum
                self.scoreboard[i][location_type_enum] += score

    def _try_rules_priority(self) -> ResolvedLocation | None:
        for rule in self.RULES_PRIORITY:
            result = rule(msg=self.msg)
            if isinstance(result, tuple) and len(result) == 2:
                return ResolvedLocation(result[0], result[1])

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
