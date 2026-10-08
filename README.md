from transformers import pipeline


# ============================================================
# CONFIG
# ============================================================

MODEL_PATH = "/home/dtphat/projects/PhoWhisper-base"

# Nếu muốn test checkpoint chính thức:
# MODEL_PATH = "vinai/PhoWhisper-base"


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading PhoWhisper...")

asr_model = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_PATH,
    chunk_length_s=30,
    stride_length_s=5,
)

print("PhoWhisper loaded.")

try:
    print("Model:", asr_model.model.config._name_or_path)
    print(
        "Sampling rate:",
        asr_model.feature_extractor.sampling_rate
    )
except Exception:
    pass


# ============================================================
# TRANSCRIBE
# ============================================================

def transcribe_audio(audio_path: str) -> str:

    result = asr_model(
        audio_path,
        generate_kwargs={
            "language": "vi",
            "task": "transcribe",
        },
    )

    return result["text"].strip()
