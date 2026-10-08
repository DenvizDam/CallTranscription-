
import csv
import re
import time
import unicodedata
from pathlib import Path

from jiwer import wer, cer

from phowhisper import transcribe_audio


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

AUDIO_DIR = BASE_DIR / "datasets/benchmark/audio"
GT_DIR = BASE_DIR / "datasets/benchmark/ground_truth"
OUTPUT_DIR = BASE_DIR / "results"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RESULT_CSV = OUTPUT_DIR / "benchmark_results.csv"
SUMMARY_FILE = OUTPUT_DIR / "summary.txt"

AUDIO_EXTENSIONS = {
    ".wav", ".gsm", ".mp3", ".flac", ".m4a"
}

# None = run all files
# Set to 3 for a quick debug run
MAX_FILES = None


# ============================================================
# NORMALIZE VIETNAMESE TEXT
# ============================================================

def normalize_text(text):
    text = unicodedata.normalize("NFC", str(text))
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ============================================================
# READ GROUND TRUTH
# ============================================================

def read_ground_truth(path):
    # utf-8-sig also handles UTF-8 BOM
    return path.read_text(encoding="utf-8-sig").strip()


# ============================================================
# DISCOVER AND VALIDATE DATASET
# ============================================================

if not AUDIO_DIR.is_dir():
    raise FileNotFoundError(AUDIO_DIR)

if not GT_DIR.is_dir():
    raise FileNotFoundError(GT_DIR)

audio_files = sorted(
    p for p in AUDIO_DIR.iterdir()
    if p.is_file()
    and p.suffix.lower() in AUDIO_EXTENSIONS
)

gt_files = sorted(GT_DIR.glob("*.txt"))

audio_stems = [p.stem for p in audio_files]
gt_stems = {p.stem for p in gt_files}

if len(set(audio_stems)) != len(audio_stems):
    raise ValueError(
        "Multiple audio files share the same base filename."
    )

missing_gt = [
    p.name for p in audio_files
    if p.stem not in gt_stems
]

extra_gt = sorted(
    gt_stems - set(audio_stems)
)

print("=" * 70)
print("PHOWHISPER LONG-FORM BENCHMARK")
print("=" * 70)

print("Audio files:", len(audio_files))
print("GT files   :", len(gt_files))
print("Missing GT :", missing_gt)
print("Extra GT   :", extra_gt)

if missing_gt or extra_gt:
    raise ValueError(
        "Dataset pairing mismatch. "
        "Fix missing/extra ground truth files first."
    )

if not audio_files:
    raise ValueError("No audio files found.")

if MAX_FILES is not None:
    audio_files = audio_files[:MAX_FILES]

print("Files to benchmark:", len(audio_files))


# ============================================================
# RESULT COLUMNS
# ============================================================

columns = [
    "audio",
    "ground_truth_file",
    "ground_truth",
    "prediction",
    "normalized_ground_truth",
    "normalized_prediction",
    "wer",
    "cer",
    "duration_sec",
    "processing_time_sec",
    "rtf",
    "status",
    "error"
]

results = []


# ============================================================
# BENCHMARK LOOP
# ============================================================

with RESULT_CSV.open(
    "w",
    encoding="utf-8-sig",
    newline=""
) as csv_file:

    writer = csv.DictWriter(
        csv_file,
        fieldnames=columns
    )

    writer.writeheader()

    for index, audio_path in enumerate(audio_files, start=1):

        gt_path = GT_DIR / f"{audio_path.stem}.txt"

        print("\n" + "=" * 70)
        print(f"[{index}/{len(audio_files)}]")
        print("Audio:", audio_path.name)
        print("GT   :", gt_path.name)

        row = {
            col: "" for col in columns
        }

        row["audio"] = audio_path.name
        row["ground_truth_file"] = gt_path.name

        try:
            ground_truth = read_ground_truth(gt_path)
            ref = normalize_text(ground_truth)

            if not ref:
                raise ValueError("Empty normalized ground truth")

            row["ground_truth"] = ground_truth
            row["normalized_ground_truth"] = ref

            # Read duration with ffprobe.
            # This is metadata only; transcribe_audio
            # does the actual decoding.
            import subprocess

            probe = subprocess.run(
                [
                    "ffprobe",
                    "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    str(audio_path)
                ],
                capture_output=True,
                text=True,
                check=True
            )

            duration = float(probe.stdout.strip())

            start = time.perf_counter()

            prediction = transcribe_audio(
                str(audio_path)
            )

            processing_time = (
                time.perf_counter() - start
            )

            pred = normalize_text(prediction)

            sample_wer = wer(ref, pred)
            sample_cer = cer(ref, pred)

            rtf = (
                processing_time / duration
                if duration > 0 else None
            )

            row.update({
                "prediction": prediction,
                "normalized_prediction": pred,
                "wer": sample_wer,
                "cer": sample_cer,
                "duration_sec": duration,
                "processing_time_sec": processing_time,
                "rtf": rtf,
                "status": "OK"
            })

            print("\nREFERENCE:")
            print(ground_truth[:500])

            print("\nPREDICTION:")
            print(prediction[:500])

            print(f"\nWER: {sample_wer * 100:.2f}%")
            print(f"CER: {sample_cer * 100:.2f}%")
            print(f"Time: {processing_time:.2f}s")
            print(f"RTF: {rtf:.3f}" if rtf is not None else "RTF: N/A")

        except Exception as e:
            row["status"] = "ERROR"
            row["error"] = str(e)

            print("ERROR:", e)

        results.append(row)

        # Save immediately after each file
        writer.writerow(row)
        csv_file.flush()


# ============================================================
# AGGREGATE METRICS
# ============================================================

valid = [
    r for r in results
    if r["status"] == "OK"
]

failed = len(results) - len(valid)

summary = [
    "PHOWHISPER LONG-FORM BENCHMARK",
    f"Total files: {len(results)}",
    f"Successful: {len(valid)}",
    f"Failed: {failed}",
]

if valid:
    refs = [
        r["normalized_ground_truth"]
        for r in valid
    ]

    preds = [
        r["normalized_prediction"]
        for r in valid
    ]

    avg_wer = sum(
        r["wer"] for r in valid
    ) / len(valid)

    avg_cer = sum(
        r["cer"] for r in valid
    ) / len(valid)

    # Corpus metrics across aligned files
    corpus_wer = wer(refs, preds)
    corpus_cer = cer(refs, preds)

    total_audio_sec = sum(
        r["duration_sec"] for r in valid
    )

    total_processing_sec = sum(
        r["processing_time_sec"] for r in valid
    )

    overall_rtf = (
        total_processing_sec / total_audio_sec
        if total_audio_sec > 0 else 0
    )

    summary += [
        f"Average WER: {avg_wer * 100:.2f}%",
        f"Average CER: {avg_cer * 100:.2f}%",
        f"Corpus WER: {corpus_wer * 100:.2f}%",
        f"Corpus CER: {corpus_cer * 100:.2f}%",
        f"Overall RTF: {overall_rtf:.3f}",
    ]

else:
    summary.append("No successful benchmark samples.")

summary_text = "\n".join(summary)

print("\n" + "=" * 70)
print(summary_text)
print("=" * 70)

SUMMARY_FILE.write_text(
    summary_text,
    encoding="utf-8"
)

print("\nSaved:", RESULT_CSV)
print("Saved:", SUMMARY_FILE)
