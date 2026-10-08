"""PhoWhisper long-form baseline vs Silero VAD + identical decoding."""
import subprocess
from pathlib import Path

import numpy as np
import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

MODEL_PATH = "/home/dtphat/projects/PhoWhisper-base"
SAMPLE_RATE = 16000
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Exact settings from the previous successful V2 fallback_no_context.
DECODING = {
    "condition_on_prev_tokens": False,
    "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
    "compression_ratio_threshold": 1.35,
    "logprob_threshold": -1.0,
    "no_speech_threshold": 0.6,
}

# Conservative settings to avoid cutting short responses ('da', 'vang').
VAD_PARAMS = {
    "threshold": 0.40,
    "sampling_rate": SAMPLE_RATE,
    "min_speech_duration_ms": 150,
    "min_silence_duration_ms": 350,
    "speech_pad_ms": 250,
}
JOIN_SILENCE_MS = 200

print(f"Loading PhoWhisper: {MODEL_PATH} ({DEVICE})")
processor = AutoProcessor.from_pretrained(MODEL_PATH)
model = AutoModelForSpeechSeq2Seq.from_pretrained(MODEL_PATH).to(DEVICE).eval()
assert processor.feature_extractor.sampling_rate == SAMPLE_RATE
_vad_model = None


def load_audio(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
           "-ac", "1", "-ar", str(SAMPLE_RATE), "-f", "f32le",
           "-acodec", "pcm_f32le", "pipe:1"]
    result = subprocess.run(cmd, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors="replace"))
    audio = np.frombuffer(result.stdout, dtype="<f4").copy()
    if not audio.size or not np.isfinite(audio).all():
        raise ValueError(f"Empty/invalid audio: {path}")
    return audio


def _get_vad_model():
    global _vad_model
    if _vad_model is None:
        from silero_vad import load_silero_vad
        _vad_model = load_silero_vad()
    return _vad_model


def apply_vad(audio):
    """Keep padded VAD speech, preserve order, insert a little silence between regions.

    This changes timeline, so resulting timestamps must NOT be treated as original call times.
    """
    from silero_vad import get_speech_timestamps

    timestamps = get_speech_timestamps(
        torch.from_numpy(audio), _get_vad_model(), **VAD_PARAMS
    )
    if not timestamps:
        raise ValueError("VAD found no speech; inspect this recording manually")

    # Padding may create overlapping segments. Merge to avoid duplicate speech.
    regions = []
    for item in timestamps:
        start, end = int(item["start"]), int(item["end"])
        if regions and start <= regions[-1][1]:
            regions[-1][1] = max(regions[-1][1], end)
        else:
            regions.append([start, end])

    join_silence = np.zeros(int(SAMPLE_RATE * JOIN_SILENCE_MS / 1000), dtype=np.float32)
    pieces = []
    kept_samples = 0
    for i, (start, end) in enumerate(regions):
        if i:
            pieces.append(join_silence)
        pieces.append(audio[start:end])
        kept_samples += end - start

    processed = np.concatenate(pieces)
    return processed, {
        "vad_segments": len(regions),
        "speech_kept_sec": kept_samples / SAMPLE_RATE,
        "speech_kept_ratio": kept_samples / len(audio),
    }


@torch.inference_mode()
def transcribe_audio(audio_path: str, use_vad: bool = False):
    """Returns (prediction, metrics). Same Whisper decoding for A/B groups."""
    audio = load_audio(audio_path)
    original_sec = len(audio) / SAMPLE_RATE
    info = {"duration_sec": original_sec, "vad_segments": 0,
            "speech_kept_sec": original_sec, "speech_kept_ratio": 1.0}
    if use_vad:
        audio, extra = apply_vad(audio)
        info.update(extra)
    info["asr_input_sec"] = len(audio) / SAMPLE_RATE

    inputs = processor(
        audio, sampling_rate=SAMPLE_RATE, return_tensors="pt",
        truncation=False, padding="longest", return_attention_mask=True
    )
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
    tokens = model.generate(
        **inputs, language="vi", task="transcribe",
        return_timestamps=True, **DECODING
    )
    prediction = processor.batch_decode(tokens, skip_special_tokens=True)[0].strip()
    return prediction, info
