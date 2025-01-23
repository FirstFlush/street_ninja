import re
from common.enums import SMSKeywordEnum, LanguageEnum

class KeywordMapping:


    MAPPING = {
        SMSKeywordEnum.SHELTER: {
            LanguageEnum.ENGLISH: {"shelter", "shelters", "homeless", "roof", "bed"},
            LanguageEnum.FRENCH: {"abri", "toit", "sansabri"},  # sans-abri
            LanguageEnum.PUNJABI: {"saran", "asra", "ghar"},  # Punjabi
            LanguageEnum.CHINESE: {"避难所", "收容所", "住所"},  # Combined Mandarin/Cantonese as "Chinese"
            LanguageEnum.YORUBA: {"abẹ", "ilé"},  # Yoruba
        },
        SMSKeywordEnum.FOOD: {
            LanguageEnum.ENGLISH: {"food", "meal", "meals", "hunger", "hungry", "starving", "eat"},
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
            LanguageEnum.ENGLISH: {"help",}
        }
    }



    def _strip_special_chars(self, text:str) -> str:
        return re.sub(r'[^a-zA-Z0-9]', '', text)


    def _prepare_words(self, msg:str) -> list[str]:
        return self._strip_special_chars(msg).lower().split()


    def get_keyword_and_language(self, msg:str) -> tuple[SMSKeywordEnum, LanguageEnum]:
        word_list = self._prepare_words(msg)
        for word in word_list:
            result = self._try_word(word)
            if result:
                return result


    def _try_word(self, word:str) -> tuple[SMSKeywordEnum, LanguageEnum] | None:

        for sms_keyword_enum, v in self.MAPPING.items():
            for language_enum, v2 in v.items():
                if word in v2:
                    return sms_keyword_enum, language_enum

    