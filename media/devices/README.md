# Device compatibility matrix

Nomily evaluates each recording source separately. A device is not supported
merely because it records audio, exposes Bluetooth, or has an export function.

| Input source | Public status | Client | Notes |
| --- | --- | --- | --- |
| V05E recorder | Implemented | iOS and Android | BLE recording workflow; real compatibility depends on the tested device and firmware. [View on Amazon](https://www.amazon.com/dp/B0HHGWYS6J) |
| TicNote NE-79 | Physical-device validation in progress | iOS | Recorder-protocol work is under validation. It is not publicly supported until recording, transfer, and transcription complete on physical hardware. |
| Apple Watch microphone | Implemented | iOS / watchOS | Records on Watch and transfers to the paired iPhone client. |
| Audio imported on iPhone | Implemented | iOS | Import, library, transcription, and summary workflow. |
| Other recorder models | Not committed | — | Requires model-specific protocol, transfer, and firmware validation. |
| Android Watch companion | Not published | — | Do not infer Wear OS support from the Android client. |

## Adding a future device

Before a new device is marked as supported, record its exact model and
firmware, pairing state, transfer path, audio format, encryption behavior, and
the smallest successful import or transfer test. Public documentation should
state whether support is implemented, verified on physical hardware, planned,
or not committed.

Do not include serial numbers, Bluetooth MAC addresses, peripheral UUIDs,
recordings, transcripts, credentials, or vendor-confidential materials.
