# CallTranscription
This repo for work



01–03: bài toán và phạm vi.
04–09: thuật ngữ, yêu cầu và triển khai.
10–13: landscape và điểm đáng chú ý từng nhóm.
14–16: lý do cần thận trọng, chi phí và dữ liệu.
17–18: shortlist và điều cần chốt.
19–25: phụ lục tra cứu.
==> Overview of slides 



Trong source code benchmark PhoWhisper của bạn, mình sẽ kiểm tra đúng 8 chỗ này. Với WER 0.9 / CER 0.8, chỉ cần một chỗ sai là kết quả có thể hỏng toàn bộ.
1. Load model và processor đúng checkpoint chưa
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seqmodel_id = "vinai/PhoWhisper-base"processor = AutoProcessor.from_pretrained(model_id)model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id)


Kiểm tra xem bạn có vô tình dùng processor của Whisper khác checkpoint không, ví dụ model PhoWhisper nhưng processor lại từ openai/whisper-base.
2. Sampling rate có thực sự là 16 kHz không
Tìm đoạn đọc audio:
audio, sr = librosa.load(path, sr=16000, mono=True)


hoặc nếu dùng soundfile:
audio, sr = sf.read(path)


thì phải có resample nếu sr != 16000.
Bạn nên thêm debug:
print("Sample rate:", sr)print("Shape:", audio.shape)print("Duration:", len(audio) / sr)


Nếu model nhận audio 8 kHz nhưng code khai báo:
sampling_rate=16000


thì đây là lỗi rất nghiêm trọng.
3. Input vào processor có truyền đúng sampling rate không
Phải dạng:
inputs = processor(    audio,    sampling_rate=16000,    return_tensors="pt")


Đừng có kiểu:
processor(audio, sampling_rate=sr)


nếu sr vẫn là 8000 mà bạn tưởng đã resample.
4. Generate có ép đúng language/task không
Với tiếng Việt, mình sẽ kiểm tra đoạn generate().
Ví dụ:
generated_ids = model.generate(    inputs.input_features,    language="vi",    task="transcribe")


hoặc tùy version Transformers:
forced_decoder_ids = processor.get_decoder_prompt_ids(    language="vi",    task="transcribe")


rồi:
generated_ids = model.generate(    inputs.input_features,    forced_decoder_ids=forced_decoder_ids)


Nếu code vô tình để translate thay vì transcribe, output có thể sai hoàn toàn mục tiêu benchmark.
5. Decode prediction có đúng không
Nên là:
prediction = processor.batch_decode(    generated_ids,    skip_special_tokens=True)[0]


Kiểm tra xem bạn có decode nhầm input_ids, labels, hoặc tensor khác không.
6. Reference và prediction có đúng cùng một audio không
Đây là chỗ mình đặc biệt muốn bạn kiểm tra.
Ví dụ:
for row in dataset:    audio_path = row["audio"]    reference = row["transcript"]


thêm:
print("FILE:", audio_path)print("REF :", reference)print("PRED:", prediction)print("-" * 50)


Lấy 5 file đầu rồi nghe thủ công audio.
Nếu:
audio_001.wav
REF: xin chào anh em gọi từ dai ichi life

nhưng audio thực tế nói nội dung khác, thì benchmark sai từ dataset mapping.
7. Normalization trước khi tính WER/CER
Tìm đoạn:
wer = metric.compute(    predictions=predictions,    references=references)


Đừng tính trực tiếp raw text nếu transcript có punctuation/casing khác nhau.
Nên normalize cả hai:
import reimport unicodedatadef normalize_vi(text):    text = unicodedata.normalize("NFC", text)    text = text.lower().strip()    text = re.sub(r"[^\w\s]", " ", text)    text = re.sub(r"\s+", " ", text)    return text.strip()


sau đó:
predictions_norm = [normalize_vi(x) for x in predictions]references_norm = [normalize_vi(x) for x in references]


rồi mới:
wer_score = wer_metric.compute(    predictions=predictions_norm,    references=references_norm)


CER cũng tương tự.
8. Chunking implementation
Nếu bạn dùng pipeline:
pipe = pipeline(    "automatic-speech-recognition",    model="vinai/PhoWhisper-base",    chunk_length_s=30)


thì khá an toàn.
Nhưng nếu bạn tự chunk:
chunk_size = 30 * 16000


hãy kiểm tra kỹ:
chunks = [    audio[i:i + chunk_size]    for i in range(0, len(audio), chunk_size)]


Vấn đề phổ biến là bạn chunk theo samples nhưng tưởng là milliseconds, ví dụ:
chunk_size = 30


thì bạn đang lấy 30 samples, không phải 30 giây.
Hoặc:
chunk_size = 30000


với NumPy audio 16 kHz thì thực ra chỉ:
30000 / 16000 = 1.875 giây

chứ không phải 30 giây.
Nếu là NumPy waveform thì:
chunk_samples = int(30 * sr)


mới đúng.
Mình khuyên bạn thêm hẳn một block debug vào source:
print("\n===== DEBUG =====")print("File:", audio_path)print("Sampling rate:", sr)print("Duration:", len(audio) / sr)print("Audio shape:", audio.shape)print("\nREFERENCE:")print(reference)print("\nPREDICTION:")print(prediction)print("\nNORMALIZED REF:")print(normalize_vi(reference))print("\nNORMALIZED PRED:")print(normalize_vi(prediction))print("=================\n")
