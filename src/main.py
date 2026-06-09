import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents import Agent, AgentSession
from livekit.plugins import deepgram, google

from language_detector import LanguageDetector
from scope_validator import is_in_scope, get_redirect
from conversation_manager import ConversationManager
from sarvam_tts_plugin import SarvamTTS

def load_system_prompt() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "config", "prompts", "presale_system_prompt.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

class PresaleAgent(Agent):
    def __init__(self):
        super().__init__(instructions=load_system_prompt())
        self.lang_detector = LanguageDetector()
        self.conv_manager = ConversationManager(scenario="presale")

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    agent = PresaleAgent()

    session = AgentSession(
        stt=deepgram.STT(
            api_key=os.getenv("DEEPGRAM_API_KEY"),
            language="multi",
            model="nova-2",
        ),
        llm=google.LLM(
            api_key=os.getenv("GEMINI_API_KEY"),
            model="gemini-2.0-flash",
        ),
        tts=SarvamTTS(language_detector=agent.lang_detector),
    )

    @session.on("user_speech_committed")
    def on_user_speech(msg):
        lang = agent.lang_detector.detect_language(msg.content)
        agent.conv_manager.log_turn("user", msg.content, lang)
        if not is_in_scope(msg.content):
            redirect = get_redirect(lang)
            agent.conv_manager.log_turn("assistant", redirect, lang)

    @session.on("agent_speech_committed")
    def on_agent_speech(msg):
        agent.conv_manager.log_turn(
            "assistant", msg.content,
            agent.lang_detector.current_lang
        )

    @ctx.room.on("disconnected")
    def on_disconnect():
        agent.conv_manager.save()

    await session.start(room=ctx.room, agent=agent)

    await session.generate_reply(
        instructions="Greet the user warmly. Say: Hello! I am Aadya, your presales assistant. How can I help you today?"
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="Aadya",
        load_threshold=1.0,
        num_idle_processes=1,
    ))