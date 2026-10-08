"""PhoWhisper V4: reproduce V3 and test timestamp-preserving VAD speech groups.
No fine-tuning. Requires ffmpeg + silero-vad + transformers.
"""
import subprocess
import os
import traceback
from pathlib import Path
import numpy as np
import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

MODEL_PATH = '/home/dtphat/projects/PhoWhisper-base'
SR = 16000
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
# Preserved from the previous V3 fallback_no_context evaluation.
DECODING = dict(condition_on_prev_tokens=False,
                temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
                compression_ratio_threshold=1.35,
                logprob_threshold=-1.0, no_speech_threshold=0.6)
VAD = dict(threshold=0.40, sampling_rate=SR,
           min_speech_duration_ms=150, min_silence_duration_ms=350,
           speech_pad_ms=250)
JOIN_SILENCE_MS = 200  # reproduce V3 concatenation

print(f'Loading {MODEL_PATH} on {DEVICE}')
processor = AutoProcessor.from_pretrained(MODEL_PATH)
model = AutoModelForSpeechSeq2Seq.from_pretrained(MODEL_PATH).to(DEVICE).eval()
assert processor.feature_extractor.sampling_rate == SR
_vad = None


def load_audio(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    p = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(path),
                        '-ac', '1', '-ar', str(SR), '-f', 'f32le',
                        '-acodec', 'pcm_f32le', 'pipe:1'], capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace'))
    audio = np.frombuffer(p.stdout, dtype='<f4').copy()
    if not len(audio) or not np.isfinite(audio).all():
        raise ValueError('Empty or invalid decoded audio')
    return audio


def vad_regions(audio):
    global _vad
    from silero_vad import load_silero_vad, get_speech_timestamps
    if _vad is None:
        # Silero TorchScript may be incompatible with some torch/Python builds.
        # VAD_BACKEND=onnx bypasses torch.jit.load (requires onnxruntime).
        backend = os.environ.get('VAD_BACKEND', 'torch').lower()
        if backend not in ('torch', 'onnx'):
            raise ValueError('VAD_BACKEND must be torch or onnx')
        print(f'[VAD] Loading Silero backend={backend}, torch={torch.__version__}')
        try:
            _vad = load_silero_vad(onnx=(backend == 'onnx'))
        except Exception:
            print('[VAD] Model loading failed:\n' + traceback.format_exc())
            raise
    try:
        stamps = get_speech_timestamps(torch.from_numpy(audio), _vad, **VAD)
    except Exception:
        print('[VAD] Speech detection failed:\n' + traceback.format_exc())
        raise
    if not isinstance(stamps, list):
        raise TypeError(f'Silero returned {type(stamps).__name__} instead of list')
    regions = []
    for s in stamps:
        if not isinstance(s, dict) or 'start' not in s or 'end' not in s:
            raise TypeError(f'Unexpected VAD timestamp: {s!r}')
        a, b = int(s['start']), int(s['end'])
        a, b = max(0, a), min(len(audio), b)
        if b <= a:
            continue
        if regions and a <= regions[-1][1]:
            regions[-1][1] = max(regions[-1][1], b)
        else:
            regions.append([a, b])
    return regions


def concatenate_regions(audio, regions):
    pause = np.zeros(int(SR * JOIN_SILENCE_MS / 1000), dtype=np.float32)
    pieces = []
    for i, (start, end) in enumerate(regions):
        if i:
            pieces.append(pause)
        pieces.append(audio[start:end])
    if not pieces:
        raise ValueError('VAD found no usable speech regions')
    return np.concatenate(pieces)


def group_regions(regions, max_seconds):
    """Group neighboring VAD regions on ORIGINAL timeline, <= max_seconds.
    A single region longer than max_seconds is split conservatively.
    """
    max_len = int(max_seconds * SR)
    groups = []
    for start, end in regions:
        while start < end:
            stop = min(end, start + max_len)
            if groups and stop - groups[-1][0] <= max_len:
                groups[-1][1] = stop
            else:
                groups.append([start, stop])
            start = stop
    return groups


@torch.inference_mode()
def recognize(audio, long_form=True):
    if len(audio) == 0:
        return ''
    features = processor(audio, sampling_rate=SR, return_tensors='pt',
                         truncation=False, padding='longest',
                         return_attention_mask=True)
    features = {k: v.to(DEVICE) for k, v in features.items()}
    # Native Whisper long-form (timestamps mandatory for >30s).
    # For <=30s groups, use short-form decoding; long-form fallback
    # thresholds are not applicable to such short groups.
    if long_form or len(audio) > 30 * SR:
        kwargs = dict(DECODING, return_timestamps=True)
    else:
        kwargs = dict(return_timestamps=False)
    ids = model.generate(**features, language='vi', task='transcribe', **kwargs)
    return processor.batch_decode(ids, skip_special_tokens=True)[0].strip()


def transcribe_audio(audio_path, mode='vad_concat', segment_seconds=25):
    audio = load_audio(audio_path)
    duration = len(audio) / SR
    info = dict(duration_sec=duration, vad_segments=0,
                speech_kept_sec=duration, speech_kept_ratio=1.0,
                asr_input_sec=duration, groups=1)
    if mode == 'no_vad':
        return recognize(audio), info
    if mode not in ('vad_concat', 'vad_segments'):
        raise ValueError(f'Unknown mode: {mode}')
    regions = vad_regions(audio)
    if not regions:
        raise ValueError('Silero VAD detected no speech; review manually')
    kept = sum(e - s for s, e in regions) / SR
    info.update(vad_segments=len(regions), speech_kept_sec=kept,
                speech_kept_ratio=kept / duration)
    if mode == 'vad_concat':
        joined = concatenate_regions(audio, regions)
        info['asr_input_sec'] = len(joined) / SR
        return recognize(joined), info

    # Unlike concatenation, do NOT remove silence inside a group.
    # It preserves natural pauses and avoids artificial speech joins.
    groups = group_regions(regions, segment_seconds)
    info['groups'] = len(groups)
    info['asr_input_sec'] = sum(e-s for s, e in groups) / SR
    chunks = []
    for start, end in groups:
        # Long-form fallback is inapplicable to <=30s segments.
        text = recognize(audio[start:end], long_form=False)
        if text:
            chunks.append(text)
    return ' '.join(chunks).strip(), info
