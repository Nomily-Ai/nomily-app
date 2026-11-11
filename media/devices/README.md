# Device compatibility matrix

Nomily evaluates each recording source separately. A device is not supported
merely because it records audio, exposes Bluetooth, or has an export function.

| Input source | Public status | Client | Notes |
| --- | --- | --- | --- |
| Vobot V05E recorder | Implemented | iOS and Android | BLE recording workflow; real compatibility depends on the tested device and firmware. [View on Amazon](https://www.amazon.com/dp/B0HHGWYS6J?maas=maas_adg_7561A19815A1FBF370F5F7E1AAD78D3E_afap_abs&ref_=aa_maas&tag=maas) |
| Apple Watch microphone | Implemented | iOS / watchOS | Records on Watch and transfers to the paired iPhone client. |
| Audio files already on iPhone | Implemented | iOS | Import, library, transcription, and summary workflow. This is not a device-integration claim. |
| Other recorder models | No public compatibility claim | — | Requires legal, protocol, transfer, and firmware review before any public statement. |
| Android Watch companion | Not published | — | Do not infer Wear OS support from the Android client. |

## Adding a future device

Before a new device is marked as supported, record its exact model and
firmware, pairing state, transfer path, audio format, encryption behavior, and
the smallest successful import or transfer test. Public documentation should
state whether support is implemented, verified on physical hardware, planned,
or not committed.

Do not include serial numbers, Bluetooth MAC addresses, peripheral UUIDs,
recordings, transcripts, credentials, or vendor-confidential materials.
