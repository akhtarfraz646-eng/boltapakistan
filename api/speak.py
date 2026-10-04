from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import edge_tts
import uuid
import os

app = FastAPI()

@app.post("/")
async def speak(request: Request):
    data = await request.json()
    text = data.get("text", "")
    filename = f"/tmp/{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(text, "ur-PK-AsadAPMultilingual")
    await communicate.save(filename)
    return FileResponse(filename, media_type="audio/mpeg")
