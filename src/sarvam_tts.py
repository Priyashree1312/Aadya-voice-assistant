import os
import httpx
import base64

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

LANGUAGE_CODE_MAP = {
    "en": "en-IN",
    "hi": "hi-IN",
    "or": "od-IN"
}

async def synthesize(text: str, language: str = "en") -> bytes:
    lang_code = LANGUAGE_CODE_MAP.get(language, "en-IN")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.sarvam.ai/text-to-speech",
            headers={
                "api-subscription-key": SARVAM_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "inputs": [text],
                "target_language_code": lang_code,
                "speaker": "anushka",
                "model": "bulbul:v2",
                "pace": 1.0,
                "loudness": 1.5,
                "enable_preprocessing": True
            }
        )
        response.raise_for_status()
        data = response.json()
        audio_b64 = data["audios"][0]
        return base64.b64decode(audio_b64)