# Nomily local ASR reference service

This optional example runs a `faster-whisper` service that matches Nomily AI's
local ASR settings. It is intended for a trusted computer on the same private
network as the phone. It has no authentication or TLS, so do not expose it to
the public internet.

It provides both endpoints used by the native client:

- `ws://<computer-ip>:12300/v1/listen` for live OPUS streaming.
- `http://<computer-ip>:12301/v1/transcribe` for complete recording files.

## Requirements

- Python 3.10 or newer
- `ffmpeg` available on `PATH`
- A computer with enough memory for the model selected

On macOS, install ffmpeg with `brew install ffmpeg`. On Ubuntu/Debian, use
`sudo apt install ffmpeg python3-venv`.

## Start the service

From the repository root:

```bash
cd examples/local-asr-server
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r nomily_local_asr/requirements.txt
python -m nomily_local_asr --host 0.0.0.0 --port 12300 --http-port 12301 --model small --lang auto
```

The first launch downloads the selected Whisper model. `small` is a sensible
first test; choose a larger model only after confirming the computer has enough
memory and acceptable processing speed.

## Phone settings

Keep the phone and computer on the same Wi-Fi. Find the computer's LAN address:

```bash
# macOS
ipconfig getifaddr en0

# Linux
hostname -I
```

In Nomily AI, open **Settings -> ASR providers -> Local ASR Server**, then enter
the address only (for example `192.168.1.20`) as **Host** and `12300` as
**Port**. Do not enter `localhost`: on a phone it refers to the phone itself.
The client automatically uses port `12301` for file transcription.

For a local test on the computer, with the service running:

```bash
curl -X POST http://127.0.0.1:12301/v1/transcribe \
  --data-binary @recording.opus \
  -H 'Content-Type: application/octet-stream'
```

If the phone cannot connect, first check that both devices are on the same
network and that the computer firewall allows inbound TCP ports `12300` and
`12301` from the local network.
