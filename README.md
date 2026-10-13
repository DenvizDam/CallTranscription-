CallCSPro/
│
├── models/
│   ├── phowhisper.py        # PhoWhisper
│   ├── qwen3_asr.py         # Qwen3-ASR
│   ├── zipformer.py         # Zipformer
│   ├── fastconformer.py     # FastConformer
│   └── whisper_large.py    # Whisper Large
│
├── configs/
│   └── models.yaml          # Cấu hình từng model
│
├── preprocessing/
│   ├── audio_loader.py
│   ├── vad.py
│   └── segmentation.py
│
├── evaluation/
│   ├── normalization.py
│   └── metrics.py
│
├── benchmark.py             # Chạy benchmark chung
│
├── datasets/
│   └── benchmark/
│       ├── audio/           # 80 audio
│       └── ground_truth/    # 80 TXT
│
└── results/
    ├── phowhisper/
    ├── qwen3_asr/
    └── zipformer/
