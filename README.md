zipformer:
  checkpoint: "/home/dtphat/projects/Zipformer/sherpa-onnx-zipformer-vi-30M-int8-2026-02-09"

  encoder: "/home/dtphat/projects/Zipformer/sherpa-onnx-zipformer-vi-30M-int8-2026-02-09/encoder.int8.onnx"
  decoder: "/home/dtphat/projects/Zipformer/sherpa-onnx-zipformer-vi-30M-int8-2026-02-09/decoder.onnx"
  joiner: "/home/dtphat/projects/Zipformer/sherpa-onnx-zipformer-vi-30M-int8-2026-02-09/joiner.int8.onnx"
  tokens: "/home/dtphat/projects/Zipformer/sherpa-onnx-zipformer-vi-30M-int8-2026-02-09/tokens.txt"

  mode: "no_vad"
  sample_rate: 16000
  num_threads: 4
  provider: "cuda"
