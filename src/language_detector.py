import re
from langdetect import detect

HINDI_KEYWORDS = [
    "namaste", "kya", "aap", "main", "hoon", "hai", "mera", "tera",
    "yeh", "woh", "kaise", "theek", "accha", "nahi", "haan", "baat",
    "chahta", "chahti", "jana", "karna", "dena", "lena", "bolna"
]

ODIA_KEYWORDS = [
    "namaskar", "aapana", "mora", "tumara", "kemiti", "thika", "accha",
    "nahi", "haan", "kahuchi", "kahibi", "debi", "jibu", "aste"
]

HINDI_SWITCH_PHRASES = [
    "hindi mein", "hindi me", "hindi bolo", "hindi boliye",
    "speak hindi", "switch to hindi"
]

ENGLISH_SWITCH_PHRASES = [
    "speak english", "english please", "switch to english",
    "english mein", "english me"
]

ODIA_SWITCH_PHRASES = [
    "odia re", "odia boli", "speak odia", "switch to odia"
]

SUPPORTED = {"en": "English", "hi": "Hindi", "or": "Odia"}


class LanguageDetector:
    def __init__(self):
        self.current_lang = "en"
        self.history = []
        self.switch_count = 0

    def detect_language(self, text: str) -> str:
        lower = text.lower().strip()

        # Layer 1 — explicit switch phrases
        for phrase in ENGLISH_SWITCH_PHRASES:
            if phrase in lower:
                return self._switch("en")
        for phrase in HINDI_SWITCH_PHRASES:
            if phrase in lower:
                return self._switch("hi")
        for phrase in ODIA_SWITCH_PHRASES:
            if phrase in lower:
                return self._switch("or")

        # Layer 2 — Devanagari Unicode (Hindi script)
        if re.search(r'[\u0900-\u097F]', text):
            return self._switch("hi")

        # Layer 3 — keyword heuristics
        words = lower.split()
        hindi_score = sum(1 for w in words if w in HINDI_KEYWORDS)
        odia_score = sum(1 for w in words if w in ODIA_KEYWORDS)

        if hindi_score >= 2:
            return self._switch("hi")
        if odia_score >= 2:
            return self._switch("or")

        # Layer 4 — langdetect fallback
        try:
            detected = detect(text)
            if detected == "hi":
                return self._switch("hi")
            elif detected == "or":
                return self._switch("or")
            elif detected == "en":
                return self._switch("en")
        except Exception:
            pass

        return self.current_lang

    def _switch(self, lang: str) -> str:
        if lang != self.current_lang:
            self.history.append(self.current_lang)
            self.current_lang = lang
            self.switch_count += 1
        return lang