import torch
import librosa

from transformers import (
    AutoProcessor,
    AutoModelForSpeechSeq2Seq,
)


# ============================================================
# CONFIG
# ============================================================

MODEL_PATH = "/home/dtphat/projects/PhoWhisper-base"

SAMPLE_RATE = 16000

SEGMENT_LENGTH_S = 20

DEVICE = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

DTYPE = (
    torch.float16
    if DEVICE == "cuda"
    else torch.float32
)


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 80)
print("Loading PhoWhisper...")
print("Model :", MODEL_PATH)
print("Device:", DEVICE)
print("=" * 80)


processor = AutoProcessor.from_pretrained(
    MODEL_PATH
)

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    MODEL_PATH,
    torch_dtype=DTYPE,
)

model.to(DEVICE)

model.eval()


print("PhoWhisper loaded.")


# ============================================================
# TRANSCRIBE ONE SEGMENT
# ============================================================

def transcribe_segment(audio):
    """
    Transcribe one audio segment.
    """

    inputs = processor(
        audio,
        sampling_rate=SAMPLE_RATE,
        return_tensors="pt",
    )

    input_features = (
        inputs.input_features
        .to(
            DEVICE,
            dtype=DTYPE
        )
    )


    with torch.no_grad():

        generated_ids = model.generate(
            input_features,
            language="vi",
            task="transcribe",
        )


    text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )[0]


    return text.strip()


# ============================================================
# TRANSCRIBE LONG AUDIO
# ============================================================

def transcribe_audio(
    audio_path: str,
) -> str:

    print()
    print(
        f"Transcribing: {audio_path}"
    )


    # --------------------------------------------------------
    # LOAD AUDIO
    # --------------------------------------------------------

    audio, sr = librosa.load(
        audio_path,
        sr=SAMPLE_RATE,
        mono=True,
    )


    duration = (
        len(audio)
        / SAMPLE_RATE
    )


    print(
        f"Duration: {duration:.2f}s"
    )


    # --------------------------------------------------------
    # SEGMENT
    # --------------------------------------------------------

    segment_samples = (
        SEGMENT_LENGTH_S
        * SAMPLE_RATE
    )


    transcripts = []


    total_segments = (
        len(audio)
        + segment_samples
        - 1
    ) // segment_samples


    # --------------------------------------------------------
    # PROCESS EACH SEGMENT
    # --------------------------------------------------------

    for i, start in enumerate(
        range(
            0,
            len(audio),
            segment_samples,
        )
    ):

        end = min(
            start + segment_samples,
            len(audio),
        )


        segment = audio[
            start:end
        ]


        segment_duration = (
            len(segment)
            / SAMPLE_RATE
        )


        print()
        print(
            f"Segment "
            f"{i + 1}/"
            f"{total_segments}"
        )

        print(
            f"{start / SAMPLE_RATE:.2f}s"
            f" -> "
            f"{end / SAMPLE_RATE:.2f}s"
        )


        # Ignore extremely short final segment
        if segment_duration < 0.5:

            print(
                "Skip very short segment."
            )

            continue


        text = transcribe_segment(
            segment
        )


        print(
            "Text:",
            text
        )


        if text:

            transcripts.append(
                text
            )


    # --------------------------------------------------------
    # MERGE
    # --------------------------------------------------------

    final_transcript = " ".join(
        transcripts
    )


    print()
    print("=" * 80)
    print("FINAL TRANSCRIPT")
    print("=" * 80)
    print(final_transcript)


    return final_transcript
