# 🤖 Aadya — AI Presale Voicebot

A multilingual AI voicebot built with LiveKit, supporting **English, Hindi, and Odia** — the only voicebot in this project that speaks three Indian languages.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LiveKit](https://img.shields.io/badge/LiveKit-1.5.11-green)
![Sarvam AI](https://img.shields.io/badge/TTS-Sarvam_AI-orange)
![Groq](https://img.shields.io/badge/LLM-Groq-purple)

---

## ✨ What Makes Aadya Special

| Feature | Aadya | Typical Bot |
|---|---|---|
| Languages | English + Hindi + **Odia** | English + Hindi only |
| TTS | Sarvam AI (Indian accent) | ElevenLabs (Western) |
| LLM | Groq (free, fast) | OpenAI (paid) |
| Odia Support | ✅ Full support | ❌ Not supported |
| Sentiment Analysis | ✅ Per turn | Basic or none |
| Analytics | ✅ JSONL + JSON per call | Basic logging |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Voice Framework | LiveKit Agents 1.5.11 |
| Speech-to-Text | Deepgram nova-2 (multilingual) |
| LLM | Groq llama-3.3-70b-versatile |
| Text-to-Speech | Sarvam AI bulbul:v2 |
| Language Detection | 4-layer fallback system |
| Backend | Python 3.11 |

---

## 🚀 Quick Start

### 1. Clone and setup

```bash
git clone https://github.com/yourusername/voicebot-screening-project
cd voicebot-screening-project
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configure API keys

```bash
cp .env.example .env
```

Fill in your `.env`:

```
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=APIxxxxxxxxxx
LIVEKIT_API_SECRET=your_secret
DEEPGRAM_API_KEY=your_deepgram_key
GROQ_API_KEY=your_groq_key
SARVAM_API_KEY=your_sarvam_key
SARVAM_SPEAKER=anushka
```

### 3. Run the bot

**Option A — One command (recommended):**
```bash
python run_all.py
```

**Option B — Manual (3 terminals):**
```bash
# Terminal 1
python src/main.py start

# Terminal 2
python token_server.py

# Terminal 3
python connect.py
```

---

## 🎤 How to Test

Once connected, try these:

| Say this | Expected response |
|---|---|
| "Hello" | English greeting from Aadya |
| "Namaste, aap kaun hain?" | Hindi response |
| "Namaskar" | Odia response |
| "How much does it cost?" | Scope redirect (no pricing!) |
| "speak hindi" | Instantly switches to Hindi |

---

## 📁 Project Structure

```
voicebot-screening-project/
├── src/
│   ├── main.py                  # Entry point
│   ├── sarvam_tts_plugin.py     # Custom Sarvam TTS adapter
│   ├── sarvam_tts.py            # Sarvam API client
│   ├── language_detector.py     # 4-layer language detection
│   ├── scope_validator.py       # Scope boundary enforcement
│   ├── conversation_manager.py  # Logging + analytics + sentiment
│   ├── sentiment.py             # Sentiment analysis
│   └── language_detector.py    # Language switching
├── config/
│   ├── prompts/
│   │   └── presale_system_prompt.txt
│   └── scenarios/
│       └── presale_config.yaml
├── tests/
│   ├── test_scope_validation.py
│   └── test_language_switching.py
├── docs/
├── logs/                        # Auto-created at runtime
├── token_server.py              # FastAPI connection endpoint
├── connect.py                   # Auto-connect helper
├── run_all.py                   # One-click launcher
├── .env.example
├── Dockerfile
└── requirements.txt
```

---

## 🌐 Language Detection

Aadya uses a 4-layer fallback system:

1. **Explicit switch phrases** — "Hindi mein baat karo", "speak english"
2. **Devanagari Unicode** — Detects Hindi script (U+0900–U+097F)
3. **Keyword heuristics** — Scores Hindi/Odia keywords (threshold: 2 matches)
4. **langdetect library** — Statistical fallback

---

## 🔒 Scope Enforcement

Aadya **never** discusses:
- Pricing, costs, or discounts
- Contracts or payment terms
- Orders or purchases
- Competitor information

When asked, she politely redirects to the sales team.

---

## 🧪 Run Tests

```bash
pytest tests/ -v
```

---

## 📊 Performance Targets

| Metric | Target | Status |
|---|---|---|
| End-to-End Latency | < 2.5s | ✅ Pass |
| Language Detection | > 95% | ✅ Pass |
| Scope Compliance | 100% | ✅ Pass |
| English STT | > 92% | ✅ Pass |
| Hindi STT | > 85% | ✅ Pass |

---

## 🔑 API Keys Needed

| Service | Get it at |
|---|---|
| LiveKit | cloud.livekit.io |
| Deepgram | console.deepgram.com |
| Groq | console.groq.com |
| Sarvam AI | dashboard.sarvam.ai |

---

## 📄 Documentation

Full project documentation: [voicebot_documentation.pdf](./voicebot_documentation.pdf)

---

## 👩‍💻 Author

**Priyashree Panda** — May 2026