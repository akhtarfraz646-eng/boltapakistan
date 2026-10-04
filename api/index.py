from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import edge_tts
import uuid
import os

app = FastAPI()

class TextInput(BaseModel):
    text: str

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/logo.png")
def logo():
    return FileResponse(os.path.join(BASE_DIR, "logo.png"))

@app.post("/speak")
async def speak(data: TextInput):
    filename = f"/tmp/{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(data.text, "ur-PK-AsadAPMultilingual")
    await communicate.save(filename)
    return FileResponse(filename, media_type="audio/mpeg")
