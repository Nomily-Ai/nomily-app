"""WebSocket handler for real-time ASR streaming."""

import asyncio
import json
import time
from websockets.asyncio.server import serve, ServerConnection

from server.asr import WhisperASR

SEGMENT_DURATION = 5.0

# Set by run_server based on CLI args
_asr_kwargs = {}


async def _send_results(ws, results):
    for r in results:
        if r.get("text"):
            print(f"\n  >> {r['text']}", flush=True)
            await ws.send(json.dumps(r))


async def handle_client(ws: ServerConnection):
    """Handle a single WebSocket ASR client session."""
    addr = ws.remote_address
    print(f"\n[+] Client connected: {addr}")

    asr = WhisperASR(**_asr_kwargs)
    frames = 0
    segments = 0
    t0 = time.monotonic()

    try:
        async for message in ws:
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                    if data.get("type") == "CloseStream":
                        await _send_results(ws, asr.transcribe(is_final=True))
                        break
                except json.JSONDecodeError:
                    pass
                continue

            asr.feed(message)
            frames += 1
            elapsed = time.monotonic() - t0
            buffered = asr.buffered_duration()

            print(f"\r  [{elapsed:6.1f}s] frames={frames}  buf={buffered:.1f}s  segments={segments}", end="", flush=True)

            if buffered >= SEGMENT_DURATION:
                results = asr.transcribe(is_final=True)
                segments += 1
                await _send_results(ws, results)

        # Final flush
        if asr.buffered_duration() > 0.1:
            await _send_results(ws, asr.transcribe(is_final=True))

    except Exception as e:
        print(f"\n  Error: {e}")
    finally:
        elapsed = time.monotonic() - t0
        asr.reset()
        print(f"\n[-] Client disconnected: {addr}  ({frames} frames, {segments} segments, {elapsed:.0f}s)")


async def run_server(host: str = "0.0.0.0", port: int = 12300, **asr_kwargs):
    global _asr_kwargs
    _asr_kwargs = asr_kwargs
    print(f"WebSocket streaming on ws://{host}:{port}/v1/listen")
    print(f"  {asr_kwargs}")
    async with serve(handle_client, host, port) as server:
        await asyncio.get_running_loop().create_future()  # run forever
