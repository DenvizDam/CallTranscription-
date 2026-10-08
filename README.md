



from transformers import pipeline

from app.utils.logger import logger


# ============================================================
# MODEL CONFIG
# ============================================================

MODEL_PATH = "/home/dtphat/projects/PhoWhisper-base"

# Nếu muốn test trực tiếp checkpoint chính thức từ Hugging Face:
# MODEL_PATH = "vinai/PhoWhisper-base"


# ============================================================
# LOAD MODEL
# ============================================================

logger.info("Loading PhoWhisper Model...")

asr_model = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_PATH,

    # Whisper/PhoWhisper được thiết kế với window 30 giây
    chunk_length_s=30,

    # Overlap giữa các chunk để tránh mất chữ ở điểm cắt
    stride_length_s=5,
)

logger.info("PhoWhisper Loaded")

# Debug thông tin model
try:
    logger.info(
        f"Model name/path: {asr_model.model.config._name_or_path}"
    )

    logger.info(
        f"Feature extractor sampling rate: "
        f"{asr_model.feature_extractor.sampling_rate}"
    )

except Exception as e:
    logger.warning(
        f"Could not print model information: {e}"
    )


# ============================================================
# TRANSCRIBE FUNCTION
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

            # Có thể giữ True nếu sau này cần timestamp
            return_timestamps=True,

            generate_kwargs={
                "language": "vi",
                "task": "transcribe",
            },
        )

        transcript = result["text"].strip()

        logger.info("Transcription Complete")

        logger.info(
            f"Transcript: {transcript}"
        )

        return transcript

    except Exception as e:

        logger.exception(
            f"Transcription failed for {audio_path}: {e}"
        )

        raise
