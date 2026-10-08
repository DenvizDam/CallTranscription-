"""Benchmark matching audio + TXT ground truth files, with A/B decoding configs."""
import argparse
import csv
import re
import time
import unicodedata
from pathlib import Path

from jiwer import cer, wer
from phowhisper import DECODING_CONFIGS, transcribe_audio

ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "datasets/benchmark/audio"
GT_DIR = ROOT / "datasets/benchmark/ground_truth"
RESULT_DIR = ROOT / "results"
EXTENSIONS = {".wav", ".gsm", ".mp3", ".flac", ".m4a"}
FIELDS = ["config", "audio", "ground_truth_file", "ground_truth", "prediction",
          "normalized_ground_truth", "normalized_prediction", "wer", "cer",
          "duration_sec", "processing_time_sec", "rtf", "status", "error"]


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text).lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def load_pairs():
    if not AUDIO_DIR.is_dir() or not GT_DIR.is_dir():
        raise FileNotFoundError(f"Expected {AUDIO_DIR} and {GT_DIR}")
    audios = sorted(p for p in AUDIO_DIR.iterdir()
                    if p.is_file() and p.suffix.lower() in EXTENSIONS)
    texts = {p.stem: p for p in GT_DIR.glob("*.txt")}
    if len({p.stem for p in audios}) != len(audios):
        raise ValueError("Multiple audio extensions share the same filename stem")
    missing = [p.name for p in audios if p.stem not in texts]
    extra = sorted(set(texts) - {p.stem for p in audios})
    print(f"Audios: {len(audios)} | TXT: {len(texts)}")
    if missing or extra or not audios:
        raise ValueError(f"Dataset pairing invalid: missing={missing}, extra={extra}")
    return [(p, texts[p.stem]) for p in audios]


def summarize(rows, config):
    valid = [r for r in rows if r["status"] == "OK"]
    result = {"config": config, "files": len(rows), "success": len(valid),
              "failed": len(rows) - len(valid), "avg_wer": "", "avg_cer": "",
              "corpus_wer": "", "corpus_cer": "", "overall_rtf": ""}
    if valid:
        result["avg_wer"] = sum(r["wer"] for r in valid) / len(valid)
        result["avg_cer"] = sum(r["cer"] for r in valid) / len(valid)
        # Preserve recording boundaries when computing corpus metrics.
        result["corpus_wer"] = wer([r["normalized_ground_truth"] for r in valid],
                                   [r["normalized_prediction"] for r in valid])
        result["corpus_cer"] = cer([r["normalized_ground_truth"] for r in valid],
                                   [r["normalized_prediction"] for r in valid])
        total_dur = sum(r["duration_sec"] for r in valid)
        result["overall_rtf"] = sum(r["processing_time_sec"] for r in valid) / total_dur
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--configs", nargs="+", choices=list(DECODING_CONFIGS),
                        default=["baseline", "fallback_no_context", "fallback_with_context"])
    parser.add_argument("--limit", type=int, default=3,
                        help="Number of audio files. 0 = all 80.")
    args = parser.parse_args()
    pairs = load_pairs()
    if args.limit < 0:
        parser.error("--limit must be >= 0")
    if args.limit:
        pairs = pairs[:args.limit]
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    summaries = []

    for config in args.configs:
        output = RESULT_DIR / f"benchmark_{config}.csv"
        rows = []
        print(f"\n=== CONFIG: {config} | {len(pairs)} calls ===")
        with output.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for i, (audio, gt) in enumerate(pairs, 1):
                row = dict.fromkeys(FIELDS, "")
                row.update(config=config, audio=audio.name, ground_truth_file=gt.name)
                try:
                    ref_raw = gt.read_text(encoding="utf-8-sig").strip()
                    ref = normalize_text(ref_raw)
                    if not ref:
                        raise ValueError("Ground truth is empty after normalization")
                    row.update(ground_truth=ref_raw, normalized_ground_truth=ref)
                    start = time.perf_counter()
                    pred_raw, duration = transcribe_audio(str(audio), config)
                    elapsed = time.perf_counter() - start
                    pred = normalize_text(pred_raw)
                    row.update(prediction=pred_raw, normalized_prediction=pred,
                               wer=wer(ref, pred), cer=cer(ref, pred),
                               duration_sec=duration, processing_time_sec=elapsed,
                               rtf=elapsed/duration, status="OK")
                    print(f"[{i}/{len(pairs)}] {audio.name} "
                          f"WER={row['wer']:.1%} CER={row['cer']:.1%} "
                          f"RTF={row['rtf']:.2f}")
                    print("GT  :", ref_raw[:180])
                    print("PRED:", pred_raw[:180])
                except Exception as e:
                    row.update(status="ERROR", error=f"{type(e).__name__}: {e}")
                    print(f"[{i}/{len(pairs)}] ERROR {audio.name}: {row['error']}")
                rows.append(row)
                writer.writerow(row)
                f.flush()
        result = summarize(rows, config)
        summaries.append(result)
        print("SUMMARY:", result)
        print("Saved:", output)

    summary_file = RESULT_DIR / "decoding_comparison.csv"
    with summary_file.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)
    print("\nCOMPARISON:", summary_file)
    if any(s["failed"] for s in summaries):
        print("WARNING: Some calls failed. Compare configs only on a shared successful set.")
    print("Remember: use a separate validation set for selecting decoding settings; keep final test set untouched.")


if __name__ == "__main__":
    main()
