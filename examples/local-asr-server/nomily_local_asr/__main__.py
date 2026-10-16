import argparse
import asyncio
import threading

from server.ws_handler import run_server
from server.http_handler import run_http_server

parser = argparse.ArgumentParser(prog="server", description="ASR server")
parser.add_argument("--host", default="0.0.0.0")
parser.add_argument("--port", type=int, default=12300,
                    help="WebSocket streaming port (default: 12300)")
parser.add_argument("--http-port", type=int, default=12301,
                    help="HTTP transcribe port (default: 12301)")
parser.add_argument("--model", default="medium",
                    help="Whisper model size (default: medium)")
parser.add_argument("--lang", default="zh",
                    help="Language code or 'auto' (default: zh)")
args = parser.parse_args()

# Start HTTP transcribe server in a background thread
http_thread = threading.Thread(
    target=run_http_server,
    kwargs={"host": args.host, "port": args.http_port,
            "language": args.lang, "model_size": args.model},
    daemon=True,
)
http_thread.start()

# Run WebSocket streaming server in main thread
asr_kwargs = {"model_size": args.model, "language": args.lang}
asyncio.run(run_server(args.host, args.port, **asr_kwargs))
