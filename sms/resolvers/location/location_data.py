from .enums import StreetSuffixEnum, StreetDirectionEnum


STREET_SUFFIXES = {e.value for e in StreetSuffixEnum}
STREET_DIRECTIONS = {e.value for e in StreetDirectionEnum}
JUNK_WORDS = {
    "i", "the", "a", "an", "some", "any",
    "and", "or", "but", "so", "because",
    "is", "are", "was", "were", "be", "been", "being",
    "where", "what", "why", "when", "which", "who", 
    "that", "this", "those", "these", "it", "its",
    "near", "by", "close", "around", "at", "to",
    "in", "on", "under", "over", "between", "with",
    "need", "want", "have", "get", "looking", "find", 
    "my", "your", "his", "her", "their", "our", 
    "me", "him", "her", "them", "us", "you",  "there",
}

VANCOUVER_LANDMARKS = {
    "canada place",
    "science world",
    "granville island",
    "robson square",
    "steam clock",
    "capilano suspension bridge",
    "queen elizabeth theatre",
    "vancouver art gallery",
    "harbour centre",
    "pacific coliseum",
    "bc place",
    "rogers arena",
    "victory square",
}

# Parks & Beaches
VANCOUVER_LANDMARKS.update({
    "english bay",
    "kitsilano beach",
    "spanish banks",
    "vanier park",
    "queen elizabeth park",
    "stanley park",
    "sunset beach",
    "spanish bank",
    "jericho beach",
})


# Transit
VANCOUVER_LANDMARKS.update({
    "waterfront station",
    "broadway city hall",
    "city hall",
    "main street science world",
    "granville station",
    "burrard station",
    "king edward station",
    "king edward stn",
    "metrotown",
    "metro stn",
    "metro station",
    "commercial broadway",
    "broadway skytrain",
    "broadway station",
    "stadium chinatown",
    "stadium-chinatown",
    "broadway stn",
    "joyce skytrain",
    "joyce stn",
    "joyce station",
})

# Medical
VANCOUVER_LANDMARKS.update({
    "vgh",  # Vancouver General Hospital
    "vancouver general hospital"
    "st. paul's hospital",
    "ubc hospital",
    "mount saint joseph hospital",
    "bc childrens hospital",
    "downtown eastside womens centre",
    "union gospel mission",
    "carnegie center",
    "carnegie centre",
    "carnegie community center",
})

# Shopping
VANCOUVER_LANDMARKS.update({
    "pacific centre",
    "tinseltown",
    "international village",
})

# Education
VANCOUVER_LANDMARKS.update({
    "ubc",
})