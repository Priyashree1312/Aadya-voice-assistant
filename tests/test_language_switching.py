import sys
sys.path.append("src")
from language_detector import LanguageDetector

def test_english_detection():
    ld = LanguageDetector()
    assert ld.detect_language("Hello how are you") == "en"

def test_hindi_devanagari():
    ld = LanguageDetector()
    assert ld.detect_language("नमस्ते आप कैसे हैं") == "hi"

def test_hindi_keywords():
    ld = LanguageDetector()
    assert ld.detect_language("namaste aap kaise hain") == "hi"

def test_switch_to_english():
    ld = LanguageDetector()
    ld.current_lang = "hi"
    assert ld.detect_language("speak english please") == "en"

def test_switch_to_hindi():
    ld = LanguageDetector()
    assert ld.detect_language("hindi mein baat karo") == "hi"

def test_switch_count():
    ld = LanguageDetector()
    ld.detect_language("namaste aap kaise hain")
    ld.detect_language("speak english please")
    assert ld.switch_count == 2

def test_odia_keywords():
    ld = LanguageDetector()
    assert ld.detect_language("namaskar kemiti acha") == "or"

def test_context_preserved():
    ld = LanguageDetector()
    ld.detect_language("namaste aap kaise hain")
    assert ld.current_lang == "hi"
    assert ld.detect_language("yeh product kaisa hai") == "hi"