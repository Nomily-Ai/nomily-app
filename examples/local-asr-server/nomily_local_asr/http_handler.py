"""HTTP handler for batch file transcription."""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from server.asr import transcribe_file

_language = "zh"
_model_size = "medium"


class TranscribeHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/v1/transcribe":
            self.send_error(404)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self.send_error(400, "No audio data")
            return

        file_data = self.rfile.read(content_length)
        print(f"\n[transcribe] Received {content_length} bytes")
        t0 = time.monotonic()

        segments = transcribe_file(file_data, language=_language, model_size=_model_size)

        elapsed = time.monotonic() - t0
        total_text = " ".join(s["text"] for s in segments)
        print(f"[transcribe] {len(segments)} segments, {elapsed:.1f}s")
        if total_text:
            print(f"  >> {total_text[:200]}")

        result = {"segments": segments, "text": total_text}
        body = json.dumps(result, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def run_http_server(host: str = "0.0.0.0", port: int = 12301,
                    language: str = "zh", model_size: str = "medium"):
    global _language, _model_size
    _language = language
    _model_size = model_size
    server = HTTPServer((host, port), TranscribeHandler)
    print(f"HTTP transcribe server on http://{host}:{port}/v1/transcribe")
    server.serve_forever()
