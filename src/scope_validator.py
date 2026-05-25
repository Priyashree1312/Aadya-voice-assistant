OUT_OF_SCOPE_KEYWORDS = [
    "price", "cost", "how much", "discount", "offer", "quote",
    "invoice", "contract", "order", "buy", "purchase", "payment",
    "kitna", "daam", "mol", "kharcha",
    "dama", "kete", "kinna",
]

REDIRECT = {
    "en": "That's a great question! For pricing and contract details, our sales team would be best placed to help. May I schedule a quick call for you?",
    "hi": "Bahut achha sawaal hai! Pricing ke liye hamari sales team aapki behtar madad kar sakti hai. Kya main aapke liye ek call schedule kar sakta hoon?",
    "or": "Eta eka bhala prashna! Dama sambandhe amara sales team apananka saahajya karibe. Mun eka call schedule karibe ki?",
}

def is_in_scope(text: str) -> bool:
    lower = text.lower()
    return not any(kw in lower for kw in OUT_OF_SCOPE_KEYWORDS)

def get_redirect(lang: str = "en") -> str:
    return REDIRECT.get(lang, REDIRECT["en"])