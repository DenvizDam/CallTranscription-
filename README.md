Xây dựng hệ thống Root Cause Analysis nhằm phân loại nguyên nhân lỗi giữa hai giai đoạn Speech-to-Text (S2T) và Named Entity Recognition (NER).



Thiết kế logic phân loại thành 5 nhóm: S2T, NER, Both Phase, No Error, Need Review.



Phát triển pipeline Python kết hợp LLM Qwen3-Omni để phân tích và xác định nguyên nhân lỗi.



Xây dựng cơ chế đối chiếu Entities Extracted với Transcript (AI) theo giá trị, ngữ nghĩa và ngữ cảnh.



Xử lý các cách biểu diễn số tiền khác nhau trong transcript, đồng thời kiểm tra nghiêm ngặt định dạng và giá trị entity mà không tự ý chỉnh sửa.



Tích hợp Python Rule Engine và LLM để giảm tình trạng phân loại nhầm lỗi S2T thành Both Phase.



Bổ sung thông tin giải thích nguyên nhân, phương pháp phân loại và các trường hỗ trợ debug.



Đảm bảo giữ nguyên toàn bộ dữ liệu gốc, chỉ phân tích những bản ghi có Label = good.



Hoàn thiện full source code V5, README, cấu hình Conda và hướng dẫn triển khai trên server Ubuntu.



Hoàn thành 12/12 unit tests trên dữ liệu mẫu; chuẩn bị kiểm thử với dữ liệu thực tế.
