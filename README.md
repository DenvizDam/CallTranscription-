from transformers import pipeline

from app.utils.logger import logger


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = "/home/dtphat/projects/PhoWhisper-base"

# Nếu muốn test trực tiếp model chính thức từ Hugging Face:
# MODEL_PATH = "vinai/PhoWhisper-base"


# ============================================================
# LOAD PHOWHISPER MODEL
# ============================================================

logger.info("Loading PhoWhisper Model...")

asr_model = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_PATH,
    chunk_length_s=30,
    stride_length_s=5,
)

logger.info("PhoWhisper Loaded")


# ============================================================
# TRANSCRIBE AUDIO
# ============================================================

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe Vietnamese audio using PhoWhisper.

    Args:
        audio_path (str):
            Path to audio file.

    Returns:
        str:
            Transcribed text.
    """

    logger.info(
        f"Transcribing: {audio_path}"
    )

    try:

        result = asr_model(
            audio_path,
            generate_kwargs={
                "language": "vi",
                "task": "transcribe",
            },
        )

        transcript = result["text"].strip()

        logger.info(
            "Transcription Complete"
        )

        logger.info(
            f"Transcript: {transcript}"
        )

        return transcript

    except Exception as e:

        logger.exception(
            f"Transcription failed for {audio_path}: {e}"
        )

        raise
