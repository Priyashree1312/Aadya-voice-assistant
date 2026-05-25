import json
import uuid
import os
from datetime import datetime


class ConversationManager:
    def __init__(self, scenario: str = "presale"):
        self.id = str(uuid.uuid4())
        self.scenario = scenario
        self.language = "en"
        self.history = []
        self.start_time = datetime.now().isoformat()
        self.lang_switches = 0
        self.turn_count = 0
        self.languages_used = set()

    def log_turn(self, role: str, content: str, lang: str, sentiment=None):
        self.history.append({
            "role": role,
            "content": content,
            "language": lang,
            "sentiment": sentiment,
            "timestamp": datetime.now().isoformat()
        })

        self.languages_used.add(lang)
        self.turn_count += 1

    def save(self):
        os.makedirs("logs", exist_ok=True)

        filepath = os.path.join("logs", f"{self.id}.json")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "conversation_id": self.id,
                "scenario": self.scenario,
                "start_time": self.start_time,
                "end_time": datetime.now().isoformat(),
                "lang_switches": self.lang_switches,
                "turn_count": self.turn_count,
                "history": self.history
            }, f, ensure_ascii=False, indent=2)

        print(f"Conversation saved: logs\\{self.id}.json")

    async def summarize(self, llm_client) -> str:
        if not self.history:
            return ""

        turns = "\n".join(
            f"{t['role'].upper()}: {t['content']}"
            for t in self.history
        )

        prompt = f"""Summarize this presale conversation in 3 bullet points:
- Main customer need
- Key product points discussed
- Next step agreed

Conversation:
{turns}
"""

        # Here you can call your LLM later
        # response = await llm_client.generate(prompt)

        summary_path = os.path.join(
            "logs",
            f"{self.id}.summary.txt"
        )

        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(f"Conversation ID: {self.id}\n")
            f.write(f"Scenario: {self.scenario}\n")
            f.write(f"Turns: {self.turn_count}\n")
            f.write(f"Languages: {', '.join(self.languages_used)}\n")
            f.write(f"Sentiment: {self._overall_sentiment()}\n")

        return summary_path

    def _overall_sentiment(self) -> str:
        sentiments = [
            t.get("sentiment")
            for t in self.history
            if t.get("sentiment")
        ]

        if not sentiments:
            return "neutral"

        pos = sentiments.count("positive")
        neg = sentiments.count("negative")

        if pos > neg:
            return "positive"
        elif neg > pos:
            return "negative"
        else:
            return "neutral"
        
        