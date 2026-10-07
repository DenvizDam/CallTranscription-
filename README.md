# CallTranscription
This repo for work



01–03: bài toán và phạm vi.
04–09: thuật ngữ, yêu cầu và triển khai.
10–13: landscape và điểm đáng chú ý từng nhóm.
14–16: lý do cần thận trọng, chi phí và dữ liệu.
17–18: shortlist và điều cần chốt.
19–25: phụ lục tra cứu.
==> Overview of slides 






Ưu tiên	Cần kiểm tra	Tại sao
🔴 1	Ground truth có đúng audio không	Lệch transcript/file → WER gần 100%
🔴 2	Decode GSM có đúng không	File nghe được nhưng waveform decode có thể sai
🔴 3	Prediction từng file	Xem model thật sự đang nghe thành gì
🔴 4	Silence/noise	Whisper rất dễ hallucinate khi ít speech
🟠 5	Channel stereo	Agent/customer có thể đang bị trộn
🟠 6	Chunking	30s chunk có thể chứa phần lớn silence
🟠 7	Language/task	Phải là Vietnamese + transcribe
🟡 8	PhoWhisper-base domain mismatch	Call-center GSM có thể khác mạnh training data


Điều mình muốn bạn làm ngay là lấy 3–5 file thôi, chưa chạy benchmark toàn bộ.
