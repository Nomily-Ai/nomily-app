# AI agent prompt: deploy Nomily AI local voice services

Copy the prompt below into an AI coding agent running **on the computer that
will host the services**. It is intended for a trusted computer and a phone on
the same private Wi-Fi network. The resulting ASR and Ollama services have no
authentication by default: never expose their ports to the public internet.

```text
Please turn this computer into a local voice-services host for the Nomily AI
recording app. Complete the deployment, verify it locally, and print the exact
values I need to enter in the app when you finish.

Safety and scope:
- Keep the services available only to this computer's private LAN. Do not open
  ports on the public internet, configure router port forwarding, or disable a
  firewall globally.
- Inspect the existing Nomily reference implementation in
  examples/local-asr-server before changing or replacing it. Preserve its
  client protocol unless a tested compatibility fix is required.
- Do not print secrets, API keys, Wi-Fi passwords, or private recordings.

Step 1 — install and start Ollama:
1. Install Ollama if it is not already installed.
2. Configure it to start automatically after login or boot, and bind it to the
   LAN with OLLAMA_HOST=0.0.0.0:11434.
3. Detect available system memory. Pull qwen2.5:3b on an 8 GB computer, or
   qwen2.5:7b when the computer has 16 GB RAM or more. If neither choice is
   practical, explain why and select the largest model that can run reliably.
4. Verify that Ollama answers locally and that it is reachable at port 11434
   from the private LAN.

Step 2 — install and run a persistent faster-whisper ASR service:
1. Install Python dependencies for faster-whisper, FastAPI, uvicorn, and
   websockets. Install ffmpeg when it is required by the operating system.
2. Use the Nomily local ASR reference service in
   examples/local-asr-server as the starting point, or create an equivalent
   compatible service when necessary. Run it continuously in the background:
   - macOS: launchd
   - Linux: systemd
   - Windows: Task Scheduler or an equivalent persistent service
3. Allow inbound connections only from the private LAN to TCP ports 12300 and
   12301. Do not create public firewall rules.
4. The service must support both Nomily endpoints:
   - HTTP batch transcription on port 12301: POST /v1/transcribe. The request
     body is raw audio bytes with Content-Type: application/octet-stream,
     usually an Ogg-Opus recording. Decode it with faster-whisper-compatible
     audio handling and return JSON in this shape:
     {"text":"full transcript","segments":[{"start":0.0,"end":1.2,"text":"segment text"}]}
   - WebSocket live transcription on port 12300: /v1/listen. The client sends
     fixed-size binary Opus frames without a container header. Assemble and
     decode them safely to PCM, feed them to VAD-assisted streaming
     transcription, and send JSON text frames as results:
     {"text":"recognized text","is_final":true}
     or
     {"text":"partial text","is_final":false}
     When the client sends the text frame {"type":"CloseStream"}, flush any
     buffered audio, send the final result, and close the connection.
5. Test the HTTP endpoint locally with a non-sensitive sample recording. Test
   the WebSocket endpoint or the Nomily app workflow before declaring success.

Step 3 — report the Nomily app settings:
1. Find this computer's private LAN IPv4 address (normally a 192.168.x.x or
   10.x.x.x address) using ifconfig, ipconfig, or the platform equivalent.
2. Print exactly these four lines, replacing the examples with real values:
   1. LAN IP: 192.168.x.x
   2. Nomily AI > Settings > Transcription > Local ASR Service > Host: 192.168.x.x
   3. Nomily AI > Settings > Transcription > Local ASR Service > Port: 12300
   4. Nomily AI > Settings > AI Services > Ollama > Endpoint: http://192.168.x.x:11434 | Model: qwen2.5:3b

Finish with this reminder: the phone and computer must be on the same Wi-Fi.
The Verify buttons on both the Local ASR Service and Ollama pages in Nomily AI
must pass before the deployment is considered complete.
```

## What the phone needs

Use the computer's LAN IP, never `localhost` or `127.0.0.1`; on a phone those
addresses refer to the phone itself. The Nomily ASR client uses port `12300` for
live audio and automatically uses `12301` for complete recording files.

For a manual setup without an agent, use the [local ASR reference
guide](README.md).
