import asyncio
import io
import os
import sys
import wave

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from livekit.agents import tts
from livekit.agents.types import APIConnectOptions
from livekit import rtc
from sarvam_tts import synthesize
from language_detector import LanguageDetector


class SarvamTTS(tts.TTS):
    def __init__(self, language_detector: LanguageDetector):
        super().__init__(
            capabilities=tts.TTSCapabilities(streaming=False),
            sample_rate=22050,
            num_channels=1
        )
        self._lang_detector = language_detector

    def synthesize(self, text: str, **kwargs) -> "SarvamChunkedStream":
        return SarvamChunkedStream(
            tts=self,
            input_text=text,
            conn_options=APIConnectOptions(),
            language_detector=self._lang_detector
        )


class SarvamChunkedStream(tts.ChunkedStream):
    def __init__(
        self,
        *,
        tts: SarvamTTS,
        input_text: str,
        conn_options: APIConnectOptions,
        language_detector: LanguageDetector
    ):
        super().__init__(tts=tts, input_text=input_text, conn_options=conn_options)
        self._lang_detector = language_detector

    async def _run(self) -> None:
        lang = self._lang_detector.current_lang
        print(f"[Sarvam] language: {lang}, text: {self._input_text[:50]}")
        try:
            audio_bytes = await synthesize(self._input_text, lang)
            print(f"[Sarvam] got audio: {len(audio_bytes)} bytes")
            frame = self._wav_to_frame(audio_bytes)
            print(f"[Sarvam] frame ready: {frame.sample_rate}Hz")
            self._event_ch.send_nowait(
                tts.SynthesizedAudio(
                    request_id=self._request_id,
                    frame=frame
                )
            )
            print(f"[Sarvam] sent to LiveKit!")
        except Exception as e:
            print(f"[Sarvam] ERROR: {e}")
            import traceback
            traceback.print_exc()

    def _wav_to_frame(self, wav_bytes: bytes) -> rtc.AudioFrame:
        with wave.open(io.BytesIO(wav_bytes)) as wf:
            sample_rate = wf.getframerate()
            num_channels = wf.getnchannels()
            raw_data = wf.readframes(wf.getnframes())

        return rtc.AudioFrame(
            data=raw_data,
            sample_rate=sample_rate,
            num_channels=num_channels,
            samples_per_channel=len(raw_data) // (2 * num_channels)
        )