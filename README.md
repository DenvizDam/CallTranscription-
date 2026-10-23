

Amount
Tối ưu S2T Prompt nhằm tăng độ chính xác khi nhận dạng số tiền, nhấn mạnh việc giữ nguyên giá trị, phân biệt đơn vị nghìn/triệu/tỷ và hạn chế tự suy đoán. Kiểm chứng hiệu quả bằng A/B Test trên audio thực tế.


code 
Tối ưu S2T Prompt để bảo toàn từng ký tự mã; kiểm tra Preprocess/VAD tại đoạn đọc mã và bổ sung bộ test nhận dạng mã chữ-số

name
Tối ưu S2T Prompt nhận dạng tên riêng tiếng Việt, hạn chế tự suy đoán họ tên; kiểm tra audio theo giọng vùng miền và bổ sung bộ kiểm thử tên khách hàng.

1. Bảng tổng hợp Root Cause & Solution
Loại thông tin	Những lỗi S2T thường gặp	Hướng giải pháp ưu tiên
NAME	Sai dấu, nhầm họ tên, thiếu hoặc dư thành phần tên	Tối ưu prompt nhận dạng tên riêng tiếng Việt; kiểm tra audio và phát âm vùng miền
PHRASE / WORD	Nhận dạng sai từ, cụm từ chuyên ngành, thiếu hoặc thêm từ	Bổ sung thuật ngữ bảo hiểm trong prompt; giảm suy đoán theo ngữ cảnh
PHONENUMBER	Sai số, thiếu/dư số, mất số 0 đầu	Nhận dạng từng chữ số, giữ nguyên thứ tự và số 0 đầu
PROPOSALNUMBER	Sai mã hồ sơ, nhầm chữ số hoặc chữ cái, thiếu ký tự	Hướng dẫn nhận dạng mã theo từng ký tự, không tự sửa theo mẫu
TERM	Sai thời hạn, nhầm năm/tháng hoặc nhầm số	Kiểm tra đồng thời giá trị số và đơn vị thời gian
2. Prompt cải thiện theo từng loại
A. NAME – Tên khách hàng / nhân viên
Ví dụ:
- Ground Truth: Nguyễn Thị Minh Anh
- Transcript AI: Nguyễn Thị Mỹ Anh
Hướng cải thiện: Giúp S2T nhận dạng chính xác tên riêng, không tự thay bằng tên phổ biến hơn.

Khi nhận dạng họ tên người Việt Nam:

- Bảo toàn đầy đủ họ, tên đệm và tên chính.
- Ưu tiên âm thanh thực tế, không suy đoán tên dựa trên mức độ phổ biến.
- Chú ý các âm và dấu thanh dễ nhầm trong tên riêng.
- Không tự thêm hoặc bỏ thành phần họ tên.
- Nếu người nói đánh vần hoặc nhắc lại tên,
  sử dụng thông tin đó để nhận dạng chính xác hơn.
- Không tự thay tên bằng tên khác chỉ vì
  phù hợp hơn với ngữ cảnh.



Solution để ghi vào RCA:
Tối ưu S2T Prompt nhận dạng tên riêng tiếng Việt, hạn chế tự suy đoán họ tên; kiểm tra audio theo giọng vùng miền và bổ sung bộ kiểm thử tên khách hàng.

B. PHRASE / WORD – Từ và cụm từ
Ví dụ:
- Ground Truth: "Phí bảo hiểm định kỳ"
- Transcript AI: "Phí bảo hiểm điện tử"
Hướng cải thiện: Tăng khả năng nhận dạng các thuật ngữ đặc thù trong ngành bảo hiểm.

Khi chuyển giọng nói thành văn bản:

- Nhận dạng chính xác các từ và cụm từ chuyên ngành bảo hiểm.
- Chú ý những cụm từ như:
  phí bảo hiểm, thời hạn đóng phí,
  số tiền bảo hiểm, hợp đồng bảo hiểm,
  quyền lợi bảo hiểm, hồ sơ yêu cầu bảo hiểm.
- Không tự thay thế cụm từ nghe được bằng
  thuật ngữ khác chỉ vì phổ biến hơn.
- Không tự bổ sung từ hoặc hoàn thiện câu
  nếu nội dung không xuất hiện trong audio.
- Giữ nguyên ý nghĩa và nội dung lời nói.



Solution để ghi vào RCA:
Bổ sung và chuẩn hóa bộ thuật ngữ bảo hiểm trong S2T Prompt; kiểm thử các cặp từ dễ nhầm, hạn chế hiện tượng thay thế, thêm hoặc bỏ từ.

C. PHONENUMBER – Số điện thoại
Ví dụ:
- Ground Truth: 0901234567
- Transcript AI: 0911234567
Hướng cải thiện: Đảm bảo từng chữ số được nhận dạng chính xác.

Khi audio chứa số điện thoại:

- Nhận dạng chính xác từng chữ số từ 0 đến 9.
- Giữ nguyên thứ tự và số lượng chữ số.
- Bắt buộc giữ các số 0 ở đầu.
- Không tự thêm, bỏ hoặc thay thế chữ số.
- Không tự sửa số điện thoại dựa trên đầu số nhà mạng.
- Khi người nói đọc theo từng nhóm,
  phải bảo toàn đầy đủ các nhóm số.
- Chỉ ghép thành một dãy số khi có đủ
  căn cứ từ nội dung audio.



Solution để ghi vào RCA:
Tối ưu prompt nhận dạng chuỗi số liên tiếp, bảo toàn số 0 đầu và thứ tự chữ số; kiểm tra VAD tại các khoảng ngắt khi đọc số điện thoại và bổ sung kiểm tra độ dài đầu ra.

D. PROPOSALNUMBER – Mã hồ sơ yêu cầu bảo hiểm
Ví dụ:
- Ground Truth: 0012345678
- Transcript AI: 012345678
Hướng cải thiện: Tập trung vào khả năng nhận dạng chính xác chuỗi mã định danh dài.

Khi nhận dạng mã hồ sơ yêu cầu bảo hiểm:

- Nhận dạng theo từng ký tự thực sự nghe được.
- Giữ chính xác thứ tự và số lượng ký tự.
- Không bỏ các số 0 đứng đầu mã.
- Không tự thêm hoặc loại bỏ ký tự.
- Không tự suy đoán mã theo cấu trúc thường gặp.
- Phân biệt các chữ số hoặc chữ cái
  có cách phát âm gần giống.
- Nếu mã được đọc thành nhiều nhóm,
  phải giữ đầy đủ các nhóm ký tự.



Solution để ghi vào RCA:
Tối ưu S2T Prompt nhận dạng chuỗi mã hồ sơ, tập trung bảo toàn từng ký tự và số 0 đầu; kiểm tra VAD khi mã được đọc ngắt quãng và xây dựng bộ test mã dài.

E. TERM – Thời hạn bảo hiểm / thời hạn đóng phí
Ví dụ:
- Ground Truth: 15 năm
- Transcript AI: 50 năm
Hoặc:
- Ground Truth: 12 tháng
- Transcript AI: 12 năm
Hướng cải thiện: Nhận dạng chính xác cả giá trị số và đơn vị thời gian.

Khi nhận dạng thông tin thời hạn:

- Nhận dạng chính xác giá trị số được nói.
- Phân biệt các đơn vị ngày, tháng và năm.
- Không tự chuyển đổi đơn vị thời gian.
- Không tự suy đoán thời hạn dựa trên
  sản phẩm hoặc quy tắc bảo hiểm.
- Phân biệt thời hạn bảo hiểm và
  thời hạn đóng phí khi nghe được trong audio.
- Không tự thay giá trị bằng một thời hạn
  được cho là hợp lý hơn.



Solution để ghi vào RCA:
Tối ưu S2T Prompt nhận dạng số và đơn vị thời gian; kiểm thử các trường hợp nhầm năm/tháng, nhầm giá trị thời hạn và kiểm tra chất lượng audio tại đoạn chứa thông tin thời hạn.


3. Bảng chuẩn hóa để đưa vào hệ thống RCA
Đây là bảng tôi đề xuất bạn sử dụng khi điền các cột GT Detail, Group Cause, False Entities, Detail False Entities, Rootcause và Solution.
GT Detail	Group Cause	False Entities	Detail False Entities	Rootcause	Solution
S2T	NAME RECOGNITION ERROR	NAME	VALUE	Nhận dạng sai họ hoặc tên	Tối ưu prompt tên riêng, đánh giá giọng vùng miền
S2T	WORD RECOGNITION ERROR	PHRASE/WORD	VALUE	Nhận dạng sai thuật ngữ bảo hiểm	Bổ sung thuật ngữ và test case chuyên ngành
S2T	NUMBER RECOGNITION ERROR	PHONENUMBER	VALUE	Sai hoặc thiếu chữ số điện thoại	Tối ưu nhận dạng từng số, bảo toàn số 0 đầu
S2T	CODE RECOGNITION ERROR	PROPOSALNUMBER	VALUE	Nhận dạng sai ký tự trong mã hồ sơ	Tối ưu prompt mã định danh, kiểm tra VAD
S2T	TERM RECOGNITION ERROR	TERM	VALUE	Nhầm giá trị hoặc đơn vị thời hạn	Tối ưu nhận dạng số và đơn vị thời gian
4. Nên ưu tiên giải pháp nào?
Tôi đề xuất sử dụng cùng một quy trình cho tất cả các loại lỗi:
1. Kiểm tra audio gốc và đoạn sau VAD để xác định có bị mất âm hay không.
2. Tối ưu S2T Prompt theo từng loại thông tin, không thêm tất cả hướng dẫn quá dài vào một prompt ngay từ đầu.
3. A/B Test prompt mới với prompt hiện tại trên cùng các audio lỗi.
4. Đánh giá lại theo từng loại: NAME, PHRASE/WORD, PHONENUMBER, PROPOSALNUMBER và TERM.
5. Nếu prompt không cải thiện, tiếp tục xem xét khả năng của model, phân đoạn audio và fine-tuning.
Một lưu ý: Prompt không đảm bảo sửa được lỗi nghe nhầm từ audio. Với tên riêng, mã và số điện thoại, chất lượng tín hiệu, việc phân đoạn và năng lực mô hình thường quan trọng không kém prompt.
Theo tôi, bạn nên xây dựng một S2T Prompt tổng thể có các quy tắc nhận dạng thông tin quan trọng, sau đó A/B Test từng nhóm hướng dẫn. Như vậy dễ đo được thay đổi nào thực sự có tác dụng và tránh prompt trở nên quá dài, gây ảnh hưởng đến các nội dung khác.
