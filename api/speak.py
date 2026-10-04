from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import edge_tts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VOICES = {
    "Asad": "ur-PK-AsadNeural",
    "Uzma": "ur-PK-UzmaNeural"
}

@app.post("/api/speak")
async def generate_speech(request: Request):
    try:
        data = await request.json()
        text = data.get('text', '').strip()
        voice_key = data.get('voice', 'Asad')
        voice_id = VOICES.get(voice_key, VOICES["Asad"])

        if not text:
            return Response(content="No text provided", status_code=400)

        # Audio ko memory mein generate karo (Vercel par file save nahi kar sakte)
        communicate = edge_tts.Communicate(text, voice_id)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]

        return Response(content=audio_data, media_type="audio/mpeg")
        
    except Exception as e:
        return Response(content=f"Error: {str(e)}", status_code=500)
