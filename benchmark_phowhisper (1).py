"""Fair A/B: fallback_no_context with and without VAD, same 80 audio/TXT pairs."""
import argparse
import csv
import re
import time
import unicodedata
from pathlib import Path

from jiwer import wer, cer
from phowhisper import transcribe_audio

ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "datasets/benchmark/audio"
GT_DIR = ROOT / "datasets/benchmark/ground_truth"
RESULT_DIR = ROOT / "results"
EXTENSIONS = {".wav", ".gsm", ".mp3", ".flac", ".m4a"}
MODES = {"no_vad": False, "with_vad": True}
FIELDS = [
    "mode", "audio", "ground_truth_file", "ground_truth", "prediction",
    "normalized_ground_truth", "normalized_prediction", "wer", "cer",
    "duration_sec", "asr_input_sec", "speech_kept_sec", "speech_kept_ratio",
    "vad_segments", "processing_time_sec", "rtf", "status", "error"
]


def normalize_text(value):
    value = unicodedata.normalize("NFC", str(value)).lower()
    value = re.sub(r"[^\w\s]", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def load_pairs():
    if not AUDIO_DIR.is_dir() or not GT_DIR.is_dir():
        raise FileNotFoundError(f"Expected {AUDIO_DIR} and {GT_DIR}")
    audios = sorted(p for p in AUDIO_DIR.iterdir()
                    if p.is_file() and p.suffix.lower() in EXTENSIONS)
    texts = {p.stem: p for p in GT_DIR.glob("*.txt")}
    if len({p.stem for p in audios}) != len(audios):
        raise ValueError("Duplicate audio stems across extensions")
    missing = [p.name for p in audios if p.stem not in texts]
    extra = sorted(set(texts) - {p.stem for p in audios})
    if not audios or missing or extra:
        raise ValueError(f"Audio/TXT mismatch: missing={missing}, extra={extra}")
    print(f"Paired {len(audios)} audio + TXT files")
    return [(p, texts[p.stem]) for p in audios]


def summarize(rows, mode):
    valid = [r for r in rows if r["status"] == "OK"]
    output = dict(mode=mode, files=len(rows), success=len(valid),
                  failed=len(rows)-len(valid), avg_wer="", avg_cer="",
                  corpus_wer="", corpus_cer="", overall_rtf="",
                  mean_speech_kept_ratio="")
    if valid:
        output["avg_wer"] = sum(r["wer"] for r in valid) / len(valid)
        output["avg_cer"] = sum(r["cer"] for r in valid) / len(valid)
        # Keep file boundaries when computing corpus metrics.
        output["corpus_wer"] = wer([r["normalized_ground_truth"] for r in valid],
                                   [r["normalized_prediction"] for r in valid])
        output["corpus_cer"] = cer([r["normalized_ground_truth"] for r in valid],
                                   [r["normalized_prediction"] for r in valid])
        total_duration = sum(r["duration_sec"] for r in valid)
        output["overall_rtf"] = sum(r["processing_time_sec"] for r in valid) / total_duration
        output["mean_speech_kept_ratio"] = sum(r["speech_kept_ratio"] for r in valid) / len(valid)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=3, help="0=all audio files")
    parser.add_argument("--modes", nargs="+", choices=MODES,
                        default=["no_vad", "with_vad"])
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("--limit must be >= 0")
    pairs = load_pairs()
    if args.limit:
        pairs = pairs[:args.limit]
    RESULT_DIR.mkdir(exist_ok=True, parents=True)
    summaries = []

    for mode in args.modes:
        rows = []
        output_file = RESULT_DIR / f"benchmark_{mode}.csv"
        print(f"\n=== {mode.upper()} | {len(pairs)} calls ===")
        with output_file.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for idx, (audio_path, txt_path) in enumerate(pairs, 1):
                row = dict.fromkeys(FIELDS, "")
                row.update(mode=mode, audio=audio_path.name,
                           ground_truth_file=txt_path.name)
                try:
                    gt = txt_path.read_text(encoding="utf-8-sig").strip()
                    ref = normalize_text(gt)
                    if not ref:
                        raise ValueError("Empty normalized ground truth")
                    row.update(ground_truth=gt, normalized_ground_truth=ref)
                    start = time.perf_counter()
                    prediction, info = transcribe_audio(str(audio_path), MODES[mode])
                    elapsed = time.perf_counter() - start
                    pred = normalize_text(prediction)
                    row.update(prediction=prediction, normalized_prediction=pred,
                               wer=wer(ref, pred), cer=cer(ref, pred),
                               processing_time_sec=elapsed, status="OK", **info)
                    row["rtf"] = elapsed / info["duration_sec"]
                    print(f"[{idx}/{len(pairs)}] {audio_path.name} "
                          f"WER={row['wer']:.1%} CER={row['cer']:.1%} "
                          f"speech={row['speech_kept_ratio']:.1%} RTF={row['rtf']:.3f}")
                    print("GT  :", gt[:140])
                    print("PRED:", prediction[:140])
                except Exception as exc:
                    row.update(status="ERROR", error=f"{type(exc).__name__}: {exc}")
                    print(f"[{idx}/{len(pairs)}] ERROR: {audio_path.name}: {row['error']}")
                rows.append(row)
                writer.writerow(row)
                f.flush()
        summaries.append(summarize(rows, mode))
        print(f"Saved: {output_file}")

    compare = RESULT_DIR / "vad_comparison.csv"
    with compare.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)
    print(f"\nSaved comparison: {compare}")
    for s in summaries:
        print(s)
    if any(s["failed"] for s in summaries):
        print("WARNING: Errors occurred. Compare only matching successful files.")
    print("Review recordings with a low speech-kept ratio to ensure VAD did not remove speech.")


if __name__ == "__main__":
    main()
