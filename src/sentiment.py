POSITIVE_EN = ["great", "excellent", "awesome", "thank", "love", "helpful", "amazing", "wonderful", "perfect", "good"]
NEGATIVE_EN = ["bad", "terrible", "frustrated", "angry", "useless", "hate", "problem", "broken", "worst", "horrible"]
POSITIVE_HI = ["bahut accha", "shukriya", "zabardast", "dhanyawad", "accha"]
NEGATIVE_HI = ["bura", "pareshaan", "gussa", "kharab", "bekar"]

def analyze_sentiment(text: str) -> str:
    lower = text.lower()
    pos = sum(1 for w in POSITIVE_EN if w in lower)
    neg = sum(1 for w in NEGATIVE_EN if w in lower)
    pos += sum(1 for w in POSITIVE_HI if w in lower)
    neg += sum(1 for w in NEGATIVE_HI if w in lower)
    if pos > neg:
        return "positive"
    elif neg > pos:
        return "negative"
    return "neutral"