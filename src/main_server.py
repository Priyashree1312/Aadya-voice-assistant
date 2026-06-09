from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from livekit import api
import os

app = FastAPI()

@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/token")
async def get_token():
    token = api.AccessToken(
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET")
    ).with_grants(api.VideoGrants(
        room_join=True,
        room="aadya-screening",
    )).with_identity("user").with_name("Candidate")
    return JSONResponse({"token": token.to_jwt(), "url": os.getenv("LIVEKIT_URL")})