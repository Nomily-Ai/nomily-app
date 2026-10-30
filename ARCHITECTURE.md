# Nomily AI architecture and integration boundary

Nomily AI is a set of native mobile clients plus user-configured AI providers.
This repository is the public entry point; it is not a shared Nomily cloud or a
complete self-hosted deployment.

```text
Vobot V05E (BLE) ─┐
Apple Watch ─────┼─> Nomily AI on iPhone ─> ASR provider or local ASR ─> transcript
Imported audio ──┘                                  │
                                                     └─> LLM provider or Ollama ─> summary

Android ─> Nomily AI Android client ─> configured ASR / LLM providers
```

## Public repositories

| Repository | Responsibility |
| --- | --- |
| `nomily-app` | Project entry, public documentation, device matrix, reference assets, and local ASR reference service. |
| [`nomily-ios`](https://github.com/Nomily-Ai/nomily-ios) | iPhone and Apple Watch client, Vobot V05E BLE workflow, local library, and Watch transfer. |
| [`nomily-android`](https://github.com/Nomily-Ai/nomily-android) | Android client and its native audio, ASR, LLM, crypto, and protocol modules. |

## Recording inputs

- **Vobot V05E**: verified BLE recording workflow in the native clients.
- **Apple Watch**: records in the watchOS companion and transfers to paired
  iPhone.
- **Plaud Note Pro, soundcore Work (D3200) / Anker AI Recorder Bean, DingTalk
  A1, and TicNote**: exported-audio import on iPhone; this is not direct BLE
  pairing.

The detailed status and future-device boundary live in the
[device compatibility matrix](media/devices/README.md).

## Provider and cost boundary

Nomily AI does not charge a subscription fee. Third-party ASR and LLM costs are
paid separately under the selected provider's pricing. Users choose and
configure their own provider account, endpoint, model, and API key.

- Azure Speech or a user-operated compatible local ASR endpoint receives audio
  only when selected for transcription.
- A selected LLM provider receives the transcript text required for summaries,
  titles, translations, or other requested generation.
- Local ASR and Ollama are optional integrations. They do not make the entire
  Nomily product self-hosted or fully offline.

## Local ASR reference contract

The reference service is in
[`examples/local-asr-server`](examples/local-asr-server/). It documents the
mobile-client contract:

| Function | Endpoint |
| --- | --- |
| Live audio | WebSocket `ws://<LAN-IP>:12300/v1/listen` |
| Complete recording | HTTP `POST http://<LAN-IP>:12301/v1/transcribe` |

Run it only on a trusted LAN. Do not expose its ports or an Ollama endpoint to
the public internet without an authentication and network-security design.

## Where to make changes

- Documentation, device claims, diagrams, and the reference service: this
  repository.
- iPhone, Apple Watch, BLE transfer, or iOS import behavior: `nomily-ios`.
- Android behavior: `nomily-android`.
- Public setup guide and fixed-data demo: [geekis.com](https://geekis.com).

Before changing a device claim or protocol detail, follow the verification
steps in [`AGENTS.md`](AGENTS.md).
