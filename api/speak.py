from http.server import BaseHTTPRequestHandler
import json, asyncio
import edge_tts

VOICES = {
    "Asad": "ur-PK-AsadAPMultilingual",
    "Uzma": "ur-PK-UzmaNeural"
}

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length))
            text = data.get('text','').strip()
            voice_key = data.get('voice','Asad')
            voice_id = VOICES.get(voice_key, VOICES["Asad"])

            if not text:
                self.send_response(400); self.end_headers(); return

            async def get_voice():
                comm = edge_tts.Communicate(text, voice_id)
                audio = b""
                async for chunk in comm.stream():
                    if chunk["type"] == "audio":
                        audio += chunk["data"]
                return audio

            audio_bytes = asyncio.run(get_voice())

            self.send_response(200)
            self.send_header('Content-Type', 'audio/mpeg')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(audio_bytes)
        except Exception as e:
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(str(e).encode())
