# Nomily App

> Your recordings. Your keys. Your AI.

Companion software for supported Nomily AI recording devices. This repository is
the project entry point: it describes what Nomily AI is and points to the app
repositories.

> **Project status:** private preview and public-release candidate. This is a
> companion-software project, not a hardware catalogue, firmware release, or
> product specification.

Most AI recorders ask users to surrender two things at once: their conversations and their choice of intelligence. Nomily AI is our challenge to that default. It is being built around a simpler idea: the person who creates the recording should control where it goes, which AI processes it, and what they pay for.

We are taking the hacker's path: ship a useful tool, expose the seams, let technically curious users inspect it, and improve it through real-world feedback. This is a private preview, not yet a public release or a promise that every component will be opened unchanged.

## Repositories

| Repository | Purpose | You need |
|---|---|---|
| [nomily-ios](https://github.com/Nomily-Ai/nomily-ios) | Native SwiftUI app for iOS 16 and later, with an Apple Watch companion | macOS, Xcode 15+, a physical iPhone, XcodeGen |
| [nomily-android](https://github.com/Nomily-Ai/nomily-android) | Native Kotlin / Jetpack Compose app for Android 7 (API 24) and later | JDK 21, Android Studio (or Gradle), a physical Android phone |
| **nomily-app** | This repository: project overview, licence, and brand assets | — |

Each app repository carries its own build and run guide. Start there. The two
apps share device concepts, but they are independent installations, not steps of
one procedure.

This repository covers companion software and its supported workflows. It does
not establish hardware appearance, dimensions, device compatibility beyond
tested evidence, firmware availability, or commercial product terms.

## App preview

| Recordings | Transcription providers | LLM providers for summaries |
|---|---|---|
| <img src="media/app-recordings.png" alt="Nomily AI recordings library" width="200"> | <img src="media/app-asr-providers.png" alt="Nomily AI transcription provider settings" width="200"> | <img src="media/app-llm-providers.png" alt="Nomily AI LLM provider and model selection for summaries" width="200"> |

Screens use synthetic or non-sensitive preview data. See
[`media/README.md`](media/README.md) before reusing product imagery or brand
assets.

## Security and privacy

- API keys are supplied by the user and must never be committed.
- Device identifiers, recordings, transcripts, logs, and generated configuration
  files must remain untracked.

Third-party dependencies remain subject to their own licenses and terms.

## License

This project is licensed under the [Nomily Small Team License 1.0.0](LICENSE).

Personal use is free. Use for the benefit of a company is permitted while no more
than 10 individuals in that company use the software; beyond that, a paid licence
is required — write to <nomily@geekis.com>. The same 10-user rule applies to the
builds we distribute through app stores. Full terms are in [`LICENSE`](LICENSE),
and the app terms of use are at <https://geekis.com/terms.html>.

Brand assets under [`media/`](media/) are not covered by this license; see
[`media/README.md`](media/README.md).
