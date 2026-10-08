"""PhoWhisper long-form ASR with configurable decoding experiments."""
import subprocess
from pathlib import Path

import numpy as np
import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

MODEL_PATH = "/home/dtphat/projects/PhoWhisper-base"
SAMPLE_RATE = 16000
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Compare on exactly the same audio and ground truth; do not auto-select by test WER.
DECODING_CONFIGS = {
    "baseline": {
        "condition_on_prev_tokens": False,
        "temperature": 0.0,
    },
    "fallback_no_context": {
        "condition_on_prev_tokens": False,
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        "compression_ratio_threshold": 1.35,
        "logprob_threshold": -1.0,
        "no_speech_threshold": 0.6,
    },
    "fallback_with_context": {
        "condition_on_prev_tokens": True,
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        "compression_ratio_threshold": 1.35,
        "logprob_threshold": -1.0,
        "no_speech_threshold": 0.6,
    },
}

print(f"Loading model: {MODEL_PATH} | device={DEVICE}")
processor = AutoProcessor.from_pretrained(MODEL_PATH)
model = AutoModelForSpeechSeq2Seq.from_pretrained(MODEL_PATH).to(DEVICE).eval()
assert processor.feature_extractor.sampling_rate == SAMPLE_RATE
print("PhoWhisper loaded.")


def load_audio(audio_path: str):
    """Decode with FFmpeg and resample to true 16 kHz mono float32."""
    path = Path(audio_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
           "-ac", "1", "-ar", str(SAMPLE_RATE), "-f", "f32le",
           "-acodec", "pcm_f32le", "pipe:1"]
    result = subprocess.run(cmd, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode(errors="replace"))
    audio = np.frombuffer(result.stdout, dtype="<f4").copy()
    if audio.size == 0 or not np.isfinite(audio).all():
        raise ValueError(f"Empty or invalid audio: {path}")
    return audio, SAMPLE_RATE


@torch.inference_mode()
def transcribe_audio(audio_path: str, config_name: str = "fallback_no_context"):
    """Return (transcript, duration_seconds) using native Whisper long-form."""
    if config_name not in DECODING_CONFIGS:
        raise ValueError(f"Unknown config {config_name}. Options: {list(DECODING_CONFIGS)}")

    audio, sr = load_audio(audio_path)
    duration = len(audio) / sr
    inputs = processor(audio, sampling_rate=sr, return_tensors="pt",
                       truncation=False, padding="longest",
                       return_attention_mask=True)
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
    generated = model.generate(
        **inputs,
        language="vi",
        task="transcribe",
        return_timestamps=True,
        **DECODING_CONFIGS[config_name],
    )
    transcript = processor.batch_decode(generated, skip_special_tokens=True)[0]
    return transcript.strip(), duration
