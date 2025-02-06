from dataclasses import dataclass
import logging
from common.enums import SMSKeywordEnum, LanguageEnum
from .exc import KeywordResolverError
from .base_resolver import BaseKeywordResolver

logger = logging.getLogger(__name__)


@dataclass
class ResolvedKeywordAndLanguage:
    sms_keyword_enum: SMSKeywordEnum
    language_enum: LanguageEnum


class KeywordLanguageResolver(BaseKeywordResolver):
    """
    Resolves SMS keywords and their associated languages from a given message.

    This class provides functionality for mapping user-provided messages to specific
    resource keywords (e.g., shelter, food, water) and their corresponding languages
    (e.g., English, French, Punjabi). It uses a pre-defined mapping of keywords to
    resource categories and languages, and employs lazy initialization to build a
    reverse mapping for efficient keyword lookups.

    Attributes:
        REVERSE_MAPPING (dict): A lazily initialized dictionary mapping each keyword
            to its corresponding (SMSKeywordEnum, LanguageEnum) pair.
        MAPPING (dict): A static dictionary containing keywords grouped by
            SMSKeywordEnum and LanguageEnum.
    """
    REVERSE_MAPPING = None
    MAPPING = {
        SMSKeywordEnum.SHELTER: {
            LanguageEnum.ENGLISH: {"shelter", "shelters", "homeless", "roof", "bed"},
            LanguageEnum.FRENCH: {"abri", "toit", "sansabri"},  # sans-abri
            LanguageEnum.PUNJABI: {"saran", "asra", "ghar"},  # Punjabi
            LanguageEnum.CHINESE: {"避难所", "收容所", "住所"},  # Combined Mandarin/Cantonese as "Chinese"
            LanguageEnum.YORUBA: {"abẹ", "ilé"},  # Yoruba
        },
        SMSKeywordEnum.FOOD: {
            LanguageEnum.ENGLISH: {"food", "meal", "meals", "hunger", "hungry", "dinner", "eat", "lunch", "breakfast", "brunch"},
            LanguageEnum.FRENCH: {"nourriture", "repas", "manger", "faim", "affamé"},
            LanguageEnum.PUNJABI: {"khana", "roti", "bhuk", "bhukh", "khaan"},  # Punjabi
            LanguageEnum.CHINESE: {"食物", "饭", "吃", "饥饿", "饿了"},  # Combined as "Chinese"
            LanguageEnum.YORUBA: {"ounje", "jẹun", "ebi", "ebin", "onje"},  # Yoruba
        },
        SMSKeywordEnum.WATER: {
            LanguageEnum.ENGLISH: {"water", "hydration", "drink", "drinking", "fountain"},
            LanguageEnum.FRENCH: {"eau", "hydratation", "boire", "fontaine", "soif"},
            LanguageEnum.PUNJABI: {"pani", "paaniyan", "piyau"},  # Punjabi
            LanguageEnum.CHINESE: {"水", "喝水", "水源", "饮水"},  # Combined as "Chinese"
            LanguageEnum.YORUBA: {"omi"},  # Yoruba
        },
        SMSKeywordEnum.WIFI: {
            LanguageEnum.ENGLISH: {"wifi", "internet", "online", "wireless"},
            LanguageEnum.FRENCH: {"connexion", "sansfil", "ligne"},  # French sans-fil
            LanguageEnum.PUNJABI: {"onlain", "onlayn"},  # Punjabi
            LanguageEnum.CHINESE: {"无线网络", "网络", "在线", "互联网络"},  # Combined as "Chinese"
            LanguageEnum.YORUBA: {"ayelujara", "asopọ"},  # Yoruba
        },
        SMSKeywordEnum.TOILET: {
            LanguageEnum.ENGLISH: {"toilet", "restroom", "washroom", "bathroom", "shit", "crap", "poo", "pee", "piss"},
            LanguageEnum.FRENCH: {"toilettes", "caca", "pipi", "uriner"},
            LanguageEnum.PUNJABI: {"sauchalay", "gusal", "peshab"},  # Punjabi
            LanguageEnum.CHINESE: {"厕所", "卫生间", "洗手间", "大便", "小便"},  # Combined as "Chinese"
            LanguageEnum.YORUBA: {"igbonse", "igbẹ", "nik", "igbe"},  # Yoruba
        },
        SMSKeywordEnum.HELP: {
            LanguageEnum.ENGLISH: {"help",},
            LanguageEnum.FRENCH: {"aide"},
            LanguageEnum.PUNJABI: {"madad", "sahayata"},
            LanguageEnum.CHINESE: {"幫助", "協助"},
            LanguageEnum.YORUBA: {"Iranwọ"},
        },
    }

    @classmethod
    def get_keyword_and_language(cls, msg:str) -> ResolvedKeywordAndLanguage:
        word_list = cls._tokenize_msg(msg)
        for word in word_list:
            # result = cls._try_word(word)
            result = cls._get_reverse_mapping().get(word)
            if result and isinstance(result, tuple) and len(result) == 2:
                return ResolvedKeywordAndLanguage(
                    sms_keyword_enum=result[0],
                    language_enum=result[1],
                )
        msg = f"Failed to resolve SMSKeywordEnum and/or LanguageEnum from msg `{msg}`."
        logger.warning(msg)
        raise KeywordResolverError(msg)

    @classmethod
    def _build_reverse_mapping(cls):
        """Build and cache the reverse mapping."""
        cls.REVERSE_MAPPING = {
            keyword: (sms_keyword_enum, language_enum)
            for sms_keyword_enum, language_map in cls.MAPPING.items()
            for language_enum, keywords in language_map.items()
            for keyword in keywords
        }

    @classmethod
    def _get_reverse_mapping(cls) -> dict[str, tuple[SMSKeywordEnum, LanguageEnum]]:
        """
        Lazily builds and returns the reverse mapping of keywords to their corresponding
        SMSKeywordEnum and LanguageEnum.

        The reverse mapping is built the first time this method is called, and then
        cached in the class-level REVERSE_MAPPING attribute for future use.
        """
        if cls.REVERSE_MAPPING is None:
            cls._build_reverse_mapping()
        return cls.REVERSE_MAPPING

    # @classmethod
    # def _try_word(cls, word:str) -> tuple[SMSKeywordEnum, LanguageEnum] | None:
    #     for sms_keyword_enum, v in cls.MAPPING.items():
    #         for language_enum, v2 in v.items():
    #             if word in v2:
    #                 return sms_keyword_enum, language_enum
