from common.enums import LocationType

LOCATION_SAMPLES = [

    ("food main and hastings", "main and hastings", LocationType.INTERSECTION),
    ("shelter 123 pender st", "123 pender st", LocationType.ADDRESS),
    ("wifi carnegie centre", "carnegie centre", LocationType.LANDMARK),

    # Standard numeric + suffix
    ("shelter 123 pender st", "123 pender st", LocationType.ADDRESS),
    ("food at 1010 howe street", "1010 howe street", LocationType.ADDRESS),
    
    # Ordinal avenue names
    ("food 33rd ave", "33rd ave", LocationType.ADDRESS),
    ("need toilet 142 21st avenue east", "142 21st avenue east", LocationType.ADDRESS),
    
    # Directional prefixes and suffixes
    ("shower 7 w hastings st", "7 w hastings st", LocationType.ADDRESS),
    ("help needed on main street west", "main street west", LocationType.ADDRESS),
    
    # Letter-number combos
    ("shelter a-321 main st", "321 main st", LocationType.ADDRESS),
    ("food 7B 555 nelson", "555 nelson", LocationType.ADDRESS),
    
    # Missing suffix (still passes based on scoring)
    ("toilet 400 columbia", "400 columbia", LocationType.ADDRESS),
    
    # Direction after suffix
    ("wifi 5665 tyne st e", "5665 tyne st e", LocationType.ADDRESS),
    
    # Lowercase garbage before address
    ("yo fam food 104 hastings st", "104 hastings st", LocationType.ADDRESS),
]