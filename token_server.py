import os
import secrets
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uvicorn
from livekit.api import AccessToken, VideoGrants

load_dotenv()

app = FastAPI()

@app.get("/connect")
async def connect():
    room_name = f"voicebot-{secrets.token_hex(4)}"

    token = (
        AccessToken(
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET")
        )
        .with_identity("user")
        .with_grants(VideoGrants(room_join=True, room=room_name))
        .to_jwt()
    )

    livekit_url = os.getenv("LIVEKIT_URL", "").replace("wss://", "https://")
    playground_url = (
        f"https://agents-playground.livekit.io/#"
        f"user_token={token}"
        f"&livekit_url={os.getenv('LIVEKIT_URL')}"
        f"&agent_name=Aadya"
    )

    print(f"Room created: {room_name}")
    print(f"URL: {playground_url}")

    return JSONResponse({
        "room": room_name,
        "playground_url": playground_url
    })

@app.get("/")
async def root():
    return {"status": "Aadya token server running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)