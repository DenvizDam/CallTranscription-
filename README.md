import re
import time
import unicodedata
from pathlib import Path

import pandas as pd
from jiwer import wer, cer

from phowhisper import transcribe_audio


# ============================================================
# CONFIG
# ============================================================

AUDIO_DIR = Path("data/audio")
GROUND_TRUTH_DIR = Path("data/ground_truth")

OUTPUT_FILE = "benchmark_results.csv"

AUDIO_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".flac",
    ".m4a",
    ".gsm",
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text: str) -> str:

    if text is None:
        return ""

    text = str(text)

    # Chuẩn hóa Unicode tiếng Việt
    text = unicodedata.normalize(
        "NFC",
        text
    )

    # Lowercase
    text = text.lower()

    # Bỏ punctuation
    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
        flags=re.UNICODE,
    )

    # Nhiều khoảng trắng -> 1 khoảng trắng
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CHECK FOLDERS
# ============================================================

if not AUDIO_DIR.exists():
    raise FileNotFoundError(
        f"Audio folder not found: {AUDIO_DIR}"
    )

if not GROUND_TRUTH_DIR.exists():
    raise FileNotFoundError(
        f"Ground truth folder not found: {GROUND_TRUTH_DIR}"
    )


# ============================================================
# FIND AUDIO FILES
# ============================================================

audio_files = sorted(
    [
        file
        for file in AUDIO_DIR.iterdir()
        if file.is_file()
        and file.suffix.lower() in AUDIO_EXTENSIONS
    ]
)


print()
print("=" * 80)
print("PHOWHISPER BENCHMARK")
print("=" * 80)

print("Audio folder       :", AUDIO_DIR)
print("Ground truth folder:", GROUND_TRUTH_DIR)
print("Total audio files  :", len(audio_files))

print("=" * 80)


if len(audio_files) == 0:
    raise RuntimeError(
        "No audio files found."
    )


# ============================================================
# RESULTS
# ============================================================

results = []


# ============================================================
# BENCHMARK LOOP
# ============================================================

for index, audio_path in enumerate(audio_files):

    audio_id = audio_path.stem

    ground_truth_path = (
        GROUND_TRUTH_DIR
        / f"{audio_id}.txt"
    )


    print()
    print("=" * 80)

    print(
        f"[{index + 1}/{len(audio_files)}]"
    )

    print(
        f"Audio       : {audio_path.name}"
    )

    print(
        f"Ground truth: {ground_truth_path.name}"
    )


    # --------------------------------------------------------
    # CHECK GROUND TRUTH
    # --------------------------------------------------------

    if not ground_truth_path.exists():

        print(
            "ERROR: Ground truth not found!"
        )

        results.append(
            {
                "audio":
                    audio_path.name,

                "ground_truth_file":
                    ground_truth_path.name,

                "ground_truth":
                    "",

                "prediction":
                    "",

                "normalized_ground_truth":
                    "",

                "normalized_prediction":
                    "",

                "wer":
                    None,

                "cer":
                    None,

                "processing_time":
                    None,

                "status":
                    "GROUND_TRUTH_NOT_FOUND",
            }
        )

        continue


    # --------------------------------------------------------
    # READ GROUND TRUTH
    # --------------------------------------------------------

    try:

        ground_truth = ground_truth_path.read_text(
            encoding="utf-8"
        ).strip()

    except UnicodeDecodeError:

        ground_truth = ground_truth_path.read_text(
            encoding="utf-8-sig"
        ).strip()


    # --------------------------------------------------------
    # TRANSCRIBE
    # --------------------------------------------------------

    try:

        start_time = time.time()

        prediction = transcribe_audio(
            str(audio_path)
        )

        processing_time = (
            time.time()
            - start_time
        )


        # ----------------------------------------------------
        # NORMALIZE
        # ----------------------------------------------------

        ref_normalized = normalize_text(
            ground_truth
        )

        pred_normalized = normalize_text(
            prediction
        )


        # ----------------------------------------------------
        # WER / CER
        # ----------------------------------------------------

        if ref_normalized:

            sample_wer = wer(
                ref_normalized,
                pred_normalized
            )

            sample_cer = cer(
                ref_normalized,
                pred_normalized
            )

        else:

            sample_wer = None
            sample_cer = None


        # ----------------------------------------------------
        # PRINT RESULT
        # ----------------------------------------------------

        print()
        print("GROUND TRUTH:")
        print(ground_truth)

        print()
        print("PREDICTION:")
        print(prediction)

        print()
        print("NORMALIZED GT:")
        print(ref_normalized)

        print()
        print("NORMALIZED PRED:")
        print(pred_normalized)

        print()


        if sample_wer is not None:

            print(
                f"WER : "
                f"{sample_wer * 100:.2f}%"
            )

            print(
                f"CER : "
                f"{sample_cer * 100:.2f}%"
            )


        print(
            f"Time: "
            f"{processing_time:.2f}s"
        )


        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        results.append(
            {
                "audio":
                    audio_path.name,

                "ground_truth_file":
                    ground_truth_path.name,

                "ground_truth":
                    ground_truth,

                "prediction":
                    prediction,

                "normalized_ground_truth":
                    ref_normalized,

                "normalized_prediction":
                    pred_normalized,

                "wer":
                    sample_wer,

                "cer":
                    sample_cer,

                "processing_time":
                    processing_time,

                "status":
                    "OK",
            }
        )


    except Exception as e:

        print()
        print(
            f"ERROR: {e}"
        )

        results.append(
            {
                "audio":
                    audio_path.name,

                "ground_truth_file":
                    ground_truth_path.name,

                "ground_truth":
                    ground_truth,

                "prediction":
                    "",

                "normalized_ground_truth":
                    "",

                "normalized_prediction":
                    "",

                "wer":
                    None,

                "cer":
                    None,

                "processing_time":
                    None,

                "status":
                    f"ERROR: {e}",
            }
        )


# ============================================================
# SAVE CSV
# ============================================================

results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# SUMMARY
# ============================================================

valid_results = results_df[
    results_df["status"] == "OK"
].copy()


print()
print()
print("=" * 80)
print("BENCHMARK SUMMARY")
print("=" * 80)

print(
    f"Total audio : "
    f"{len(audio_files)}"
)

print(
    f"Successful  : "
    f"{len(valid_results)}"
)

print(
    f"Failed      : "
    f"{len(audio_files) - len(valid_results)}"
)


if len(valid_results) > 0:

    # --------------------------------------------------------
    # MEAN PER-FILE WER / CER
    # --------------------------------------------------------

    average_wer = (
        valid_results["wer"]
        .mean()
    )

    average_cer = (
        valid_results["cer"]
        .mean()
    )

    average_time = (
        valid_results[
            "processing_time"
        ]
        .mean()
    )


    print()
    print(
        f"Average WER : "
        f"{average_wer * 100:.2f}%"
    )

    print(
        f"Average CER : "
        f"{average_cer * 100:.2f}%"
    )

    print(
        f"Average time: "
        f"{average_time:.2f}s"
    )


    # --------------------------------------------------------
    # CORPUS WER / CER
    # --------------------------------------------------------

    all_references = " ".join(
        valid_results[
            "normalized_ground_truth"
        ].tolist()
    )

    all_predictions = " ".join(
        valid_results[
            "normalized_prediction"
        ].tolist()
    )


    corpus_wer = wer(
        all_references,
        all_predictions
    )

    corpus_cer = cer(
        all_references,
        all_predictions
    )


    print()
    print(
        f"Corpus WER  : "
        f"{corpus_wer * 100:.2f}%"
    )

    print(
        f"Corpus CER  : "
        f"{corpus_cer * 100:.2f}%"
    )


print()
print(
    f"Results saved to: "
    f"{OUTPUT_FILE}"
)

print("=" * 80)
