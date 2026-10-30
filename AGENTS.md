# Nomily AI entry-repository guide

## Scope

This repository is the public project entry point: documentation, compatibility
boundaries, reference assets, and the local ASR reference service. It is not an
installable mobile client and it does not contain a shared Nomily cloud service.

## Repository map

- iPhone and Apple Watch client: [`Nomily-Ai/nomily-ios`](https://github.com/Nomily-Ai/nomily-ios)
- Android client: [`Nomily-Ai/nomily-android`](https://github.com/Nomily-Ai/nomily-android)
- Local transcription reference service: [`examples/local-asr-server/`](examples/local-asr-server/)
- Device compatibility matrix: [`media/devices/README.md`](media/devices/README.md)
- Public project guide and fixed-data demo: [geekis.com](https://geekis.com)

## Change boundaries

- Keep device claims precise. `Vobot V05E` is the BLE recorder workflow; named
  third-party recorders are supported through exported-audio import unless a
  direct integration is explicitly documented and verified.
- Do not claim that the complete product is self-hosted or fully offline. Local
  ASR and Ollama are user-operated provider integrations.
- Never add API keys, recordings, transcripts, device identifiers, logs, or
  private endpoint addresses to the repository.

## Verification

For documentation, device-matrix, or protocol changes, run:

```sh
git diff --check
xmllint --noout media/diagrams/*.svg
python -m compileall -q examples/local-asr-server/nomily_local_asr
```

For changes to the local ASR service, also follow its
[reference-service README](examples/local-asr-server/README.md) and keep the
documented ports and request contract aligned with the mobile clients.
