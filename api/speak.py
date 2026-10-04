from fastapi import FastAPI, Request
from fastapi.responses import Response
import edge_tts

app = FastAPI()

@app.post("/")
async def handler(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        if not text:
            return Response("No text", status_code=400)
        
        communicate = edge_tts.Communicate(text, "ur-PK-UzmaNeural")
        audio_bytes = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes += chunk["data"]
        
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        return Response(content=f"Error: {str(e)}", status_code=500)

# Vercel ke liye
app = app
