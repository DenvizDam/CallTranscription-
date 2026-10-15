Hiện tại:
- Ground Truth: Mã số nhân viên đúng.
- AI Transcript: Mã số nhân viên bị nhận diện sai.
- Extracted Entity agentcode: Sai theo transcript.
Tôi đề xuất bạn debug theo phương pháp Backward Tracing, bắt đầu từ nơi phát hiện lỗi rồi truy ngược về bước phát sinh lỗi đầu tiên.
1. Khoanh vùng lỗi trong pipeline
Audio gốc + Ground Truth

Preprocessing / VAD
Audio có bị mất hoặc cắt sai dãy số không?

SpeechToTextProcessor
Ưu tiên kiểm tra
Transcript thô đã sai mã số chưa?

NERProcessor / NerPipeline
Có làm biến đổi hoặc trích xuất sai mã số không?

Entity: agentcode sai


2. Bây giờ bạn chỉ cần đặt 3 breakpoint
BP	Vị trí	Cần kiểm tra
BP1	SpeechToTextProcessor – ngay sau inference	Transcript thô từ model
BP2	NERProcessor – sau normalization	Mã số nhân viên có bị biến đổi không
BP3	NerPipeline – sau khi extract entities	Giá trị agentcode mà NER trả về
Cách chạy
1. Mở ba function trên và đặt breakpoint tại các vị trí tương ứng.
2. Chạy worker bằng F5 hoặc attach debugger vào worker đang chạy.
3. Gửi request chứa audio bị lỗi.
4. Khi dừng ở BP1, xem raw transcript. So sánh dãy số với ground truth.
5. Nhấn F5 để đến BP2, kiểm tra transcript sau normalization.
6. Nhấn F5 để đến BP3, kiểm tra entity agentcode.
3. Cách xác định nguyên nhân
Kết quả debug	Hướng điều tra
Raw transcript đã sai	S2T, audio preprocessing hoặc VAD
Raw transcript đúng, normalized transcript sai	Logic normalization
Transcript sau normalization đúng, agentcode sai	NER, parsing hoặc entity mapping
Cả ba đúng nhưng JSON cuối sai	Post-processing hoặc export
Nếu BP1 đã sai, chưa cần sửa NER ngay. Vì agentcode sai có thể chỉ là lỗi kéo theo (downstream error).
4. Sau khi xác nhận lỗi do S2T
Với mã số nhân viên, bạn cần đặc biệt chú ý:
- Model nhận nhầm chữ số có cách phát âm gần giống nhau.
- Model tự bỏ hoặc thêm chữ số.
- Model gộp dãy số thành một số khác.
- VAD cắt mất chữ số ở đầu hoặc cuối.
- Prompt hoặc decoding khiến model tự diễn giải thay vì chép chính xác dãy số.
Mã số nhân viên là identifier, không phải số lượng. Vì vậy, cần giữ nguyên từng chữ số, đúng thứ tự và cả số 0 ở đầu nếu có.
Một cải tiến lâu dài có thể là kiểm tra agentcode theo độ dài và định dạng hợp lệ, nhưng không được tự ý sửa thành một mã nhân viên khác chỉ vì mã đó có trong danh sách.

5. Việc tôi muốn bạn làm ngay
Bắt đầu với BP1 tại SpeechToTextProcessor trước. Đây là điểm có giá trị nhất ở case hiện tại.
Bạn hãy gửi tôi hai thứ:
1. Ground Truth và AI Transcript của đoạn mã số nhân viên (có thể thay các số thật bằng dãy số giả nhưng giữ nguyên kiểu sai).
2. Ảnh code trong SpeechToTextProcessor, đặc biệt đoạn gọi model và nhận transcript.
Tôi sẽ chỉ bạn chính xác dòng nào cần đặt breakpoint, biến nào cần xem và cách tiếp tục debug để xác định root cause.
