from .enums import StreetSuffixEnum, StreetDirectionEnum
import re

class RegexLibrary:

    number_preceeding_word = r"\b\d+[-#]?\w*\b"
    street_suffix_after_word = rf"\b({StreetSuffixEnum.regex_string()})\b"
    street_direction_after_suffix = rf"\b({StreetDirectionEnum.regex_string()})\b"
    intersection = r"\b(\w+)\s+(?:&|and)\s+(\w+)\b"
    # normalize_string = re.compile(r"[^\w\s]")
    normalize_string = re.compile(r"[^\w\s&]")  # Strip special chars but keep `&` since it appears intersections
    multiple_whitespace = re.compile(r"\s+")    # collapse multiple whitespace:  "   " -> ""
    # full_address = rf"\b(\d+[-#]?\w*)\s+(\w+(\s+\w+)*)\s+({StreetSuffixEnum.regex_string()})(\s+({StreetDirectionEnum.regex_string()}))?\b"

    full_address = fr"""
\b
(?:[#A-Z]?-?\d+[-]?\d*)\s+
([\w]+(?:\s+[\w]+)?)\s+
({StreetSuffixEnum.regex_string()})
(?:\s+({StreetDirectionEnum.regex_string()}))?
\b
"""