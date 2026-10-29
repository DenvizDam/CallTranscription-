
S2T - fix dc lỗi nhận dạng sai giá trị số tiền  , c
NER - fix được lỗi trích xuất sai format của ammount và năm tháng 

Mục đích của bản Technical Specification (TS) này là giải thích, ghi nhận và kiểm soát toàn bộ những thay đổi kỹ thuật trong quá trình tối ưu hệ thống Speech-to-Text (S2T) và Named Entity Recognition (NER), để team Developer, AI/ML, QA và Technical Lead có thể hiểu, kiểm thử và triển khai một cách nhất quán.

Nói đơn giản, tài liệu này giúp trả lời 5 câu hỏi:
1. Tại sao cần thay đổi? Hệ thống hiện tại đang gặp những lỗi gì?
2. Chúng ta đã thay đổi những gì? Prompt, logic và cấu trúc code được cải tiến ra sao?
3. Thay đổi hoạt động như thế nào? Các bước xử lý và quy tắc mới là gì?
4. Làm sao biết thay đổi hiệu quả? Dùng test case và chỉ số nào để đánh giá?
5. Làm sao triển khai an toàn? Có ảnh hưởng hệ thống cũ không, và rollback như thế nào?
1. Giá trị thực tế của tài liệu
Đối tượng	Giá trị nhận được
Technical Lead	Hiểu phạm vi thay đổi, rủi ro và cơ sở để phê duyệt
AI/ML Team	Hiểu các quy tắc prompt, nguyên nhân lỗi và hướng tối ưu
Developer	Biết những file nào thay đổi, cách tích hợp và kiểm tra
QA / Tester	Biết cần kiểm thử những trường hợp nào và kết quả kỳ vọng
Business Team	Hiểu cải tiến có thể nâng cao chất lượng dữ liệu và giảm công việc kiểm tra thủ công như thế nào
DevOps	Có cơ sở lập kế hoạch triển khai và rollback

2. Ví dụ ngay từ công việc của bạn
Trước khi tối ưu, hệ thống có những lỗi:
Vấn đề	Trước tối ưu	Mục tiêu sau tối ưu
S2T sai số tiền	750 triệu → 350 triệu	Nhận đúng 750 triệu
S2T tự thêm đơn vị	10 triệu 400 đồng → 10 triệu 400 nghìn đồng	Không tự thêm “nghìn”
NER Detect Dư	Thủy Nguyễn Thị Thu Thủy	Nguyễn Thị Thu Thủy
NER Amount Format	"280 triệu"	"280000000"
NER Term Format	"20 năm"	"20"

Bản TS ghi rõ vấn đề, yêu cầu kỹ thuật, cách thực hiện và phương pháp kiểm thử cho từng trường hợp.

Lưu ý: Cột sau tối ưu là mục tiêu cần đạt, không phải tất cả các lỗi đã được xác nhận khắc phục thành công.
3. Technical Specification khác báo cáo kết quả như thế nào?
Đây là điểm quan trọng nhất.
Technical Specification	Evaluation / Test Report
Chúng ta cần thay đổi gì?	Sau khi thay đổi, kết quả ra sao?
Tại sao thay đổi?	Chất lượng cải thiện bao nhiêu?
Giải pháp được thiết kế thế nào?	Có phát sinh lỗi mới không?
Cần kiểm thử những gì?	Bao nhiêu test case Pass/Fail?
Cách triển khai và rollback?	Có đủ điều kiện để go-live không?

Technical Specification không phải tài liệu chứng minh model đã tốt hơn. Nó là tài liệu mô tả yêu cầu, thiết kế và điều kiện chấp nhận thay đổi.

Để hoàn chỉnh việc báo cáo với công ty, TS nên đi kèm kết quả benchmark và kiểm thử thực tế.
4. Tại sao công ty cần tài liệu này?
Ví dụ, sáu tháng sau có Developer mới tiếp nhận hệ thống NER và nhìn thấy đoạn code:
return enhance_prompt(text)



Nếu không có tài liệu, họ sẽ không biết tại sao có ner_v2_guards.py, những quy tắc nào được bổ sung, rủi ro của việc bỏ chúng đi, và phải kiểm thử lại những gì.

Nhờ Technical Specification, người tiếp nhận có thể hiểu lý do tồn tại của thay đổi mà không phải hỏi lại toàn bộ người thực hiện.

Tài liệu còn giúp team kiểm soát thay đổi: tránh sửa một lỗi nhỏ nhưng làm hỏng những trường hợp đã hoạt động đúng.
5. Kết luận
Đối với dự án bạn đang làm tại Dai-ichi Life, bản TS có ba giá trị lớn nhất:
- Technical: Ghi lại kiến trúc, logic tối ưu, các thay đổi trong source code và cách kiểm thử.
- Business: Liên kết các cải tiến kỹ thuật với chất lượng thông tin cuộc gọi, khả năng đánh giá và giảm rủi ro sai dữ liệu.
- Project Management: Hỗ trợ code review, UAT, phê duyệt triển khai, bảo trì và bàn giao hệ thống.
Điều tôi muốn nhấn mạnh: Bản Technical Specification hiện tại giải thích khá đầy đủ chúng ta đang cải tiến cái gì và bằng cách nào, nhưng phần cải tiến thực sự mang lại hiệu quả bao nhiêu vẫn cần được bổ sung bằng số liệu Before vs After.

Khi có cả Technical Specification + Evaluation Results + Test Evidence, công ty sẽ có cơ sở vững chắc hơn để quyết định có nên đưa bản tối ưu vào production hay không.
