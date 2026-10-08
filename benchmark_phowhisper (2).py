"""Run V4 controlled comparisons over matching audio/TXT pairs."""
import argparse
import csv
import re
import time
import unicodedata
from pathlib import Path
from jiwer import wer, cer

ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / 'datasets/benchmark/audio'
GT_DIR = ROOT / 'datasets/benchmark/ground_truth'
OUT = ROOT / 'results_v4'
EXT = {'.wav', '.gsm', '.mp3', '.m4a', '.flac'}
FIELDS = ['mode', 'audio', 'ground_truth_file', 'ground_truth', 'prediction',
          'normalized_ground_truth', 'normalized_prediction', 'wer', 'cer',
          'duration_sec', 'asr_input_sec', 'speech_kept_sec', 'speech_kept_ratio',
          'vad_segments', 'groups', 'processing_time_sec', 'rtf', 'status', 'error']


def normalize(text):
    text = unicodedata.normalize('NFC', text).lower()
    text = re.sub(r'[^\w\s]', ' ', text, flags=re.UNICODE)
    return re.sub(r'\s+', ' ', text).strip()


def pairs():
    if not AUDIO_DIR.is_dir() or not GT_DIR.is_dir():
        raise FileNotFoundError(f'Expected folders: {AUDIO_DIR} / {GT_DIR}')
    audios = sorted(p for p in AUDIO_DIR.iterdir()
                    if p.is_file() and p.suffix.lower() in EXT)
    gts = {p.stem: p for p in GT_DIR.glob('*.txt')}
    if not audios or len({p.stem for p in audios}) != len(audios):
        raise ValueError('No audio or duplicate audio filenames across extensions')
    missing = [a.name for a in audios if a.stem not in gts]
    extra = sorted(set(gts) - {a.stem for a in audios})
    if missing or extra:
        raise ValueError(f'Missing TXT: {missing}; unmatched TXT: {extra}')
    return [(a, gts[a.stem]) for a in audios]


def metrics(rows, mode):
    good = [r for r in rows if r['status'] == 'OK']
    result = dict(mode=mode, total=len(rows), success=len(good),
                  failed=len(rows) - len(good))
    if good:
        result.update(avg_wer=sum(r['wer'] for r in good)/len(good),
                      avg_cer=sum(r['cer'] for r in good)/len(good),
                      corpus_wer=wer([r['normalized_ground_truth'] for r in good],
                                     [r['normalized_prediction'] for r in good]),
                      corpus_cer=cer([r['normalized_ground_truth'] for r in good],
                                     [r['normalized_prediction'] for r in good]),
                      rtf=sum(r['processing_time_sec'] for r in good) /
                          sum(r['duration_sec'] for r in good))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=3, help='0 means all files')
    parser.add_argument('--modes', nargs='+', choices=['no_vad', 'vad_concat', 'vad_segments'],
                        default=['vad_concat', 'vad_segments'])
    parser.add_argument('--segment-seconds', type=float, default=25)
    args = parser.parse_args()
    if args.limit < 0 or not 3 <= args.segment_seconds <= 30:
        parser.error('--limit >=0 and --segment-seconds between 3 and 30 required')
    items = pairs()
    if args.limit:
        items = items[:args.limit]
    OUT.mkdir(exist_ok=True)
    from phowhisper import transcribe_audio
    summaries = []
    for mode in args.modes:
        rows = []
        output = OUT / f'{mode}_{int(args.segment_seconds)}s.csv'
        with output.open('w', encoding='utf-8-sig', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            for index, (audio, gt_path) in enumerate(items, 1):
                row = dict.fromkeys(FIELDS, '')
                row.update(mode=mode, audio=audio.name,
                           ground_truth_file=gt_path.name)
                try:
                    ground_truth = gt_path.read_text(encoding='utf-8-sig').strip()
                    ref = normalize(ground_truth)
                    if not ref:
                        raise ValueError('Empty ground truth')
                    start = time.perf_counter()
                    prediction, info = transcribe_audio(str(audio), mode, args.segment_seconds)
                    elapsed = time.perf_counter() - start
                    hyp = normalize(prediction)
                    row.update(ground_truth=ground_truth, prediction=prediction,
                               normalized_ground_truth=ref, normalized_prediction=hyp,
                               wer=wer(ref, hyp), cer=cer(ref, hyp), **info,
                               processing_time_sec=elapsed,
                               rtf=elapsed/info['duration_sec'], status='OK')
                    print(f'{mode} [{index}/{len(items)}] {audio.name}: '
                          f'WER={row["wer"]:.2%} CER={row["cer"]:.2%} '
                          f'groups={info["groups"]} kept={info["speech_kept_ratio"]:.1%}')
                except Exception as exc:
                    row.update(status='ERROR', error=f'{type(exc).__name__}: {exc}')
                    print(f'{mode} [{index}/{len(items)}] ERROR {audio.name}: {row["error"]}')
                rows.append(row)
                writer.writerow(row)
                file.flush()
        summaries.append(metrics(rows, mode))
        print('Saved', output)
    summary = OUT / 'comparison.csv'
    with summary.open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)
    for s in summaries:
        print(s)
    print('Comparison:', summary)
    print('NOTE: Review low VAD-kept ratios to check for lost speech.')
    print('NOTE: Short-segment decode uses short-form; fallback thresholds only apply to long-form.')


if __name__ == '__main__':
    main()
