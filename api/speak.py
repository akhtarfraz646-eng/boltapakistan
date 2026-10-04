from http.server import BaseHTTPRequestHandler
import json
import asyncio
import edge_tts

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
            body = self.rfile.read(length)
            data = json.loads(body)
            
            text = data.get('text','').strip()
            voice_name = data.get('voice','Asad')

            if not text:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No text')
                return

            voices = {
                "Asad": "ur-PK-AsadAPMultilingual",
                "Uzma": "ur-PK-UzmaNeural"
            }
            voice_id = voices.get(voice_name, voices["Asad"])

            async def get_audio():
                com = edge_tts.Communicate(text, voice_id)
                audio_data = b""
                async for chunk in com.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data

            audio_bytes = asyncio.run(get_audio())

            self.send_response(200)
            self.send_header('Content-type', 'audio/mpeg')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(audio_bytes)

        except Exception as e:
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(str(e).encode())
