from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import edge_tts, uuid, os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def make_ssml(text, voice, emo):
    t = text.strip()
    if emo == "gussa": t = f"Aray! {t}! Samjho! {t}!"
    elif emo == "pyar": t = f"Haye... {t}... dil se {t}..."
    elif emo == "pareshani": t = f"Uff Allah... {t}... samajh nahi aa raha... {t}..."
    elif emo == "dar": t = f"Aa... {t}... dar lag raha hai... {t}..."
    elif emo == "khushi": t = f"Wah! {t}! Zabardast! {t}!"
    elif emo == "hansi": t = f"Hahaha! {t}! Bohat funny! {t}!"
    elif emo == "rona": t = f"Aah... {t}... {t}... kismat..."
    elif emo == "udas": t = f"Aah... {t}... dil udaas hai..."
    elif emo == "adab": t = f"Janab, arz hai ke {t}. Mehrbani."
    elif emo == "sargoshi": t = f"Shhh... {t}... dheere... {t}"
    elif emo == "dosti": t = f"Oye yaar! {t}! Chal {t}!"
    
    rate = {"gussa":"+30%","pyar":"-15%","pareshani":"+10%","dar":"-5%","khushi":"+20%","hansi":"+15%","rona":"-35%","udas":"-30%","adab":"-20%","sargoshi":"-10%","dosti":"+10%"}.get(emo,"-5%")
    pitch = {"gussa":"+20Hz","pyar":"-10Hz","pareshani":"+15Hz","dar":"+20Hz","khushi":"+20Hz","hansi":"+15Hz","rona":"-20Hz","udas":"-18Hz","adab":"+2Hz","sargoshi":"-15Hz"}.get(emo,"+0Hz")
    vol = "x-soft" if emo in ["sargoshi","dar","rona","udas","pyar"] else "medium"
    return f'<speak><voice name="{voice}"><prosody rate="{rate}" pitch="{pitch}" volume="{vol}">{t}</prosody></voice></speak>'

@app.get("/")
async def home(): return FileResponse("index.html")

@app.get("/logo.png")
async def logo(): return FileResponse("logo.png")

@app.post("/generate")
async def generate(data: dict):
    text, voice, emo = data.get("text",""), data.get("voice","ur-PK-AsadNeural"), data.get("emotion","normal")
    fname = f"{uuid.uuid4()}.mp3"
    ssml = make_ssml(text, voice, emo)
    await edge_tts.Communicate(ssml, voice).save(fname)
    base = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/") or "http://127.0.0.1:8000"
    return {"file_url": f"{base}/play/{fname}"}

@app.get("/play/{filename}")
async def play_file(filename: str): return FileResponse(filename, media_type="audio/mpeg")