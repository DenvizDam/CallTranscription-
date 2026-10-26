STT	Sub-task	Nội dung thực hiện	Deliverable
1	Analyze False Entity Errors	Phân tích các lỗi S2T theo từng False Entity (Amount, Name, Phone Number, Agent Code, Proposal Number, Term...)	Danh sách lỗi và mức độ ưu tiên
2	Identify Prompt Gaps	Xác định điểm thiếu trong prompt hiện tại khiến model nhận dạng sai hoặc không nhất quán	Danh sách vấn đề cần cải thiện
3	Enhance Amount Prompt	Cải thiện nhận dạng số tiền, đơn vị tiền tệ, cách đọc số	Prompt cập nhật cho Amount
4	Enhance Name Prompt	Cải thiện nhận dạng họ tên, tên riêng và tên khách hàng	Prompt cập nhật cho Name
5	Enhance Code & Number Prompt	Cải thiện Agent Code, Proposal Number, Phone Number và chuỗi ký tự chữ–số	Prompt cập nhật cho Code & Number
6	Enhance Domain Terminology Prompt	Bổ sung thuật ngữ bảo hiểm, tên sản phẩm và từ chuyên ngành	Prompt cập nhật cho Term
7	Integrate Prompt Improvements	Tích hợp các thay đổi thành prompt thống nhất, tránh xung đột quy tắc	Unified S2T Prompt
8	Test & Compare Results	Chạy lại các audio lỗi với prompt cũ và mới, so sánh transcript với Ground Truth	Kết quả Before vs After
9	Evaluate Regression & Finalize	Kiểm tra cải thiện ở nhóm lỗi mục tiêu và đảm bảo không làm tăng lỗi ở nhóm khác	Final Prompt & Evaluation Report
