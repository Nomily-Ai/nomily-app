# Nomily App

> Your recordings. Your keys. Your AI.

Nomily is companion software for supported AI recording devices. This repository
is the public project entry point: use it to understand the project boundary,
choose a mobile client, and find the applicable licence. The runnable clients
live in their own repositories.

## Start here

| If you want to… | Start with | What you need |
|---|---|---|
| Build the iPhone or Apple Watch client | [nomily-ios](https://github.com/Nomily-Ai/nomily-ios) | macOS, Xcode 15+, a physical iPhone; Apple Watch is optional |
| Build the Android client | [nomily-android](https://github.com/Nomily-Ai/nomily-android) | JDK 21, Android Studio or Gradle, a physical Android phone |
| Understand the project and licence | **nomily-app** | This repository |

Each client has its own build and run guide. They share product concepts, but
they are separate native applications rather than two steps of one installation.

## Status and scope

The client source repositories are public for inspection and local builds.
Release readiness, store availability, supported device combinations, and
firmware compatibility are tracked separately and must not be inferred from a
source commit alone.

This account covers the companion software and its documented workflows. It
does **not** publish production service credentials, user recordings, device
identifiers, firmware release packages, hardware specifications, or commercial
product commitments.

## Repository map

| Repository | Role |
|---|---|
| [nomily-ios](https://github.com/Nomily-Ai/nomily-ios) | Native SwiftUI client for iOS and Apple Watch |
| [nomily-android](https://github.com/Nomily-Ai/nomily-android) | Native Kotlin / Jetpack Compose client for Android |
| **nomily-app** | Project map, project-wide licence, and reusable brand-preview assets |

## App preview

| Recordings | Transcription providers | LLM providers for summaries |
|---|---|---|
| <img src="media/app-recordings.png" alt="Nomily recordings library" width="200"> | <img src="media/app-asr-providers.png" alt="Nomily transcription provider settings" width="200"> | <img src="media/app-llm-providers.png" alt="Nomily LLM provider and model selection" width="200"> |

Screens use synthetic or non-sensitive preview data. Review
[`media/README.md`](media/README.md) before reusing product imagery or brand
assets.

## Privacy and responsible reporting

- API keys are supplied by the user and must never be committed.
- Keep recordings, transcripts, device identifiers, logs, generated
  configuration files, and access credentials out of issues and pull requests.
- For a reproducible bug, open an issue in the affected client repository and
  include the client version, device/OS version, and redacted steps to reproduce.

## Licence

The source is available under the [Nomily Small Team License 1.0.0](LICENSE).
It permits personal use and company use by teams of up to 10 people; larger
teams need a separate paid licence. Contact <nomily@geekis.com> for commercial
licensing. This is a source-available licence, not an OSI-approved open-source
licence.

Brand assets under [`media/`](media/) are excluded from that licence; see
[`media/README.md`](media/README.md).
