"""ASR engines: real-time streaming (faster-whisper) and batch file transcription."""

import struct
import subprocess
import numpy as np

# OGG Opus wrapping is self-contained so the reference service has no client-code dependency.

OPUS_FRAME_SIZE = 40
OPUS_SAMPLE_RATE = 48000
OPUS_CHANNELS = 1
OPUS_PRESKIP = 312


def _ogg_crc(data: bytes) -> int:
    crc = 0
    for b in data:
        crc ^= b << 24
        for _ in range(8):
            if crc & 0x80000000:
                crc = ((crc << 1) ^ 0x04C11DB7) & 0xFFFFFFFF
            else:
                crc = (crc << 1) & 0xFFFFFFFF
    return crc


def _make_ogg_page(serial, page_seq, granule, segments, bos=False, eos=False):
    flag = 0
    if bos: flag |= 0x02
    if eos: flag |= 0x04
    body = b"".join(segments)
    seg_table = bytes(len(s) for s in segments)
    header = struct.pack(
        "<4sBBqIIIB", b"OggS", 0, flag, granule,
        serial, page_seq, 0, len(segments),
    )
    page = header + seg_table + body
    crc = _ogg_crc(page)
    page = page[:22] + struct.pack("<I", crc) + page[26:]
    return page


def raw_opus_to_ogg_bytes(raw: bytes) -> bytes:
    """Wrap raw concatenated 40-byte OPUS frames into OGG Opus container."""
    num_frames = len(raw) // OPUS_FRAME_SIZE
    if num_frames == 0:
        return b""
    serial = 0x444E4F54
    pages = []
    page_seq = 0

    opus_head = struct.pack(
        "<8sBBHIhB", b"OpusHead", 1, OPUS_CHANNELS,
        OPUS_PRESKIP, OPUS_SAMPLE_RATE, 0, 0,
    )
    pages.append(_make_ogg_page(serial, page_seq, 0, [opus_head], bos=True))
    page_seq += 1

    vendor = b"nomily"
    opus_tags = b"OpusTags" + struct.pack("<I", len(vendor)) + vendor + struct.pack("<I", 0)
    pages.append(_make_ogg_page(serial, page_seq, 0, [opus_tags]))
    page_seq += 1

    granule = OPUS_PRESKIP
    for i in range(0, num_frames, 50):
        batch = []
        for j in range(i, min(i + 50, num_frames)):
            batch.append(raw[j * OPUS_FRAME_SIZE : (j + 1) * OPUS_FRAME_SIZE])
            granule += 960
        is_last = (i + 50 >= num_frames)
        pages.append(_make_ogg_page(serial, page_seq, granule, batch, eos=is_last))
        page_seq += 1

    return b"".join(pages)


def decode_opus_to_pcm(raw_opus: bytes, sample_rate: int) -> np.ndarray | None:
    """Decode raw OPUS frames to 16-bit PCM via ffmpeg."""
    ogg_data = raw_opus_to_ogg_bytes(raw_opus)
    if not ogg_data:
        return None
    try:
        proc = subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error",
                "-i", "pipe:0",
                "-f", "s16le", "-acodec", "pcm_s16le",
                "-ar", str(sample_rate), "-ac", "1",
                "pipe:1",
            ],
            input=ogg_data, capture_output=True, timeout=10,
        )
        if proc.returncode != 0:
            print(f"  ffmpeg decode error: {proc.stderr.decode()[-200:]}")
            return None
        return np.frombuffer(proc.stdout, dtype=np.int16)
    except Exception as e:
        print(f"  Decode error: {e}")
        return None


def decode_file_to_pcm(file_data: bytes, sample_rate: int) -> np.ndarray | None:
    """Decode an audio file (OGG Opus, WAV, etc.) to 16-bit PCM via ffmpeg."""
    try:
        proc = subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error",
                "-i", "pipe:0",
                "-f", "s16le", "-acodec", "pcm_s16le",
                "-ar", str(sample_rate), "-ac", "1",
                "pipe:1",
            ],
            input=file_data, capture_output=True, timeout=60,
        )
        if proc.returncode != 0:
            print(f"  ffmpeg decode error: {proc.stderr.decode()[-200:]}")
            return None
        return np.frombuffer(proc.stdout, dtype=np.int16)
    except Exception as e:
        print(f"  Decode error: {e}")
        return None


# ── Streaming ASR (real-time WebSocket) ──

class WhisperASR:
    """Real-time ASR using faster-whisper with time-based segmentation."""

    SAMPLE_RATE = 12000

    def __init__(self, model_size: str = "medium", language: str = "zh", device: str = "auto"):
        from faster_whisper import WhisperModel
        print(f"Loading Whisper model '{model_size}' (language={language})...")
        self.model = WhisperModel(model_size, device=device, compute_type="auto")
        self.language = language
        print("Model loaded.")
        self._buffer = bytearray()
        self._time_offset = 0.0
        self._prev_text = ""

    def feed(self, opus_frame: bytes):
        self._buffer.extend(opus_frame)

    def buffered_duration(self) -> float:
        return len(self._buffer) / OPUS_FRAME_SIZE * 0.020

    def transcribe(self, is_final: bool = False) -> list[dict]:
        if not self._buffer:
            return []

        pcm = decode_opus_to_pcm(bytes(self._buffer), self.SAMPLE_RATE)
        if pcm is None or len(pcm) == 0:
            self._buffer.clear()
            return []

        duration = len(pcm) / self.SAMPLE_RATE
        audio_f32 = pcm.astype(np.float32) / 32768.0

        segments, _ = self.model.transcribe(
            audio_f32,
            language=self.language if self.language != "auto" else None,
            vad_filter=True,
            beam_size=5,
            initial_prompt=self._prev_text or None,
        )

        results = []
        texts = []
        for seg in segments:
            text = seg.text.strip()
            if text:
                texts.append(text)
                results.append({
                    "type": "transcript",
                    "text": text,
                    "start": round(self._time_offset + seg.start, 3),
                    "duration": round(seg.end - seg.start, 3),
                    "is_final": is_final,
                })

        if texts:
            self._prev_text = "".join(texts)[-200:]

        self._time_offset += duration
        self._buffer.clear()
        return results

    def reset(self):
        self._buffer.clear()
        self._time_offset = 0.0
        self._prev_text = ""


# ── Batch ASR (complete file transcription) ──

_whisper_model = None


def _get_whisper_model(model_size: str = "medium", device: str = "auto"):
    """Lazy-load and cache the Whisper model for batch transcription."""
    global _whisper_model
    if _whisper_model is None:
        from faster_whisper import WhisperModel
        print(f"Loading Whisper model '{model_size}' for batch transcription...")
        _whisper_model = WhisperModel(model_size, device=device, compute_type="auto")
        print("Model loaded.")
    return _whisper_model


def transcribe_file(file_data: bytes, language: str = "zh",
                    model_size: str = "medium") -> list[dict]:
    """Transcribe a complete audio file. Returns list of segments with timestamps."""
    pcm = decode_file_to_pcm(file_data, sample_rate=16000)
    if pcm is None or len(pcm) == 0:
        return []

    audio_f32 = pcm.astype(np.float32) / 32768.0
    model = _get_whisper_model(model_size)

    segments, info = model.transcribe(
        audio_f32,
        language=language if language != "auto" else None,
        vad_filter=True,
        beam_size=5,
        word_timestamps=True,
    )

    results = []
    for seg in segments:
        text = seg.text.strip()
        if text:
            results.append({
                "text": text,
                "start": round(seg.start, 3),
                "end": round(seg.end, 3),
                "duration": round(seg.end - seg.start, 3),
            })

    return results
