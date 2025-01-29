from .enums import StreetSuffixEnum, StreetDirectionEnum


class RegexLibrary:

    number_preceeding_word = r"\b\d+[-#]?\w*\b"
    street_suffix_after_word = rf"\b({StreetSuffixEnum.regex_string()})\b"
    street_direction_after_suffix = rf"\b({StreetDirectionEnum.regex_string()})\b"
    intersection = r"\b(\w+)\s+(?:&|and)\s+(\w+)\b"
    # full_address = rf"\b(\d+[-#]?\w*)\s+(\w+(\s+\w+)*)\s+({StreetSuffixEnum.regex_string()})(\s+({StreetDirectionEnum.regex_string()}))?\b"

    full_address = fr"""
\b
(?:[#A-Z]?-?\d+[-]?\d*)\s+
([\w]+(?:\s+[\w]+)?)\s+
({StreetSuffixEnum.regex_string()})
(?:\s+({StreetDirectionEnum.regex_string()}))?
\b
"""