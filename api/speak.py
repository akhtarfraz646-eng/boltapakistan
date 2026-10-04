from fastapi import FastAPI, Request
from fastapi.responses import Response
import edge_tts

app = FastAPI()

VOICES = {
    "Asad": "ur-PK-AsadAPMultilingual",
    "Uzma": "ur-PK-UzmaNeural"
}

@app.post("/")
async def handler(request: Request):
    try:
        data = await request.json()
        text = data.get("text","").strip()
        if not text:
            return Response("No text", status_code=400)
        voice_name = data.get("voice","Asad")
        voice_id = VOICES.get(voice_name, VOICES["Asad"])
        
        communicate = edge_tts.Communicate(text, voice_id)
        audio_bytes = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes += chunk["data"]
        
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        return Response(content=str(e), status_code=500)
