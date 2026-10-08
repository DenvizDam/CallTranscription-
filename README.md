
import subprocess
from pathlib import Path

import numpy as np
import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq


# ============================================================
# CONFIG
# ============================================================

MODEL_PATH = "/home/dtphat/projects/PhoWhisper-base"

# Muon dung checkpoint chinh thuc:
# MODEL_PATH = "vinai/PhoWhisper-base"

SAMPLE_RATE = 16000

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 60)
print("Loading PhoWhisper...")
print("Model:", MODEL_PATH)
print("Device:", DEVICE)
print("Dtype:", DTYPE)
print("=" * 60)

processor = AutoProcessor.from_pretrained(MODEL_PATH)

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    MODEL_PATH,
    torch_dtype=DTYPE,
)

model.to(DEVICE)
model.eval()

print("PhoWhisper loaded successfully.")
print("Expected sample rate:", processor.feature_extractor.sampling_rate)


# ============================================================
# AUDIO DECODING
# ============================================================

def load_audio(audio_path: str):
    """
    Decode audio using FFmpeg.

    Supports GSM, WAV, MP3, FLAC, etc.
    Resamples to 16 kHz mono PCM float32.
    """

    path = Path(audio_path)

    if not path.is_file():
        raise FileNotFoundError(f"Audio not found: {path}")

    command = [
        "ffmpeg",
        "-nostdin",
        "-v", "error",
        "-i", str(path),
        "-vn",
        "-ac", "1",
        "-ar", str(SAMPLE_RATE),
        "-f", "f32le",
        "pipe:1",
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "FFmpeg is not installed or not in PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        error_message = exc.stderr.decode(
            "utf-8", errors="replace"
        )
        raise RuntimeError(
            f"FFmpeg decode failed: {error_message}"
        ) from exc

    audio = np.frombuffer(
        result.stdout,
        dtype=np.float32
    ).copy()

    if audio.size == 0:
        raise ValueError("Decoded audio is empty.")

    if not np.isfinite(audio).all():
        raise ValueError("Audio contains NaN or Infinity.")

    duration = len(audio) / SAMPLE_RATE

    return audio, duration


# ============================================================
# LONG-FORM TRANSCRIPTION
# ============================================================

@torch.inference_mode()
def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe Vietnamese audio, including long calls.

    Uses Whisper sequential long-form generation,
    NOT pipeline chunk_length_s.
    """

    audio, duration = load_audio(audio_path)

    print(f"Audio: {Path(audio_path).name}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Samples: {len(audio)}")
    print(f"Sample rate: {SAMPLE_RATE}")

    # IMPORTANT:
    # truncation=False preserves the full recording.
    # padding="longest" avoids unnecessary 30s padding.
    inputs = processor(
        audio,
        sampling_rate=SAMPLE_RATE,
        return_tensors="pt",
        truncation=False,
        padding="longest",
        return_attention_mask=True,
    )

    input_features = inputs.input_features.to(
        device=DEVICE,
        dtype=DTYPE,
    )

    attention_mask = inputs.attention_mask.to(DEVICE)

    # Whisper uses timestamps to move through long audio.
    # No manual 30-second splitting is performed here.
    generated_ids = model.generate(
        input_features=input_features,
        attention_mask=attention_mask,
        language="vi",
        task="transcribe",
        return_timestamps=True,
        do_sample=False,
    )

    transcript = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )[0]

    return transcript.strip()
