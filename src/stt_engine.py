import os
import httpx
import base64
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

LANGUAGE_CODE_MAP = {
    "en": "en-IN",
    "hi": "hi-IN",
    "or": "od-IN"
}

async def transcribe_audio(audio_bytes: bytes, language: str = "en") -> str:
    lang_code = LANGUAGE_CODE_MAP.get(language, "en-IN")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.sarvam.ai/speech-to-text",
            headers={
                "api-subscription-key": SARVAM_API_KEY,
            },
            files={
                "file": ("audio.wav", audio_bytes, "audio/wav")
            },
            data={
                "language_code": lang_code,
                "model": "saarika:v2",
                "with_timestamps": False
            }
        )
        response.raise_for_status()
        data = response.json()
        return data.get("transcript", "")