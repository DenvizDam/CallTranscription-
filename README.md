# PROMPT – EXCEL STATISTICAL REPORT & ROOT CAUSE ANALYSIS

Hãy đóng vai một chuyên gia Data Analyst và Business Analyst, sử dụng dataset hiện có trong Excel để xây dựng báo cáo thống kê chuyên nghiệp, chính xác, trực quan, dễ hiểu và tập trung vào giá trị business.

## 1. Điều kiện lọc dữ liệu bắt buộc

Trước khi thực hiện bất kỳ phép thống kê nào, phải lọc toàn bộ dataset theo điều kiện:

**Label = "good"**

Quy tắc:
- Chỉ những dòng có Label chính xác bằng "good" mới được tham gia phân tích.
- Loại bỏ khỏi phạm vi thống kê tất cả các dòng có Label khác "good" hoặc bị Blank.
- Toàn bộ KPI, bảng thống kê, biểu đồ và kết luận phải dựa trên tập dữ liệu đã lọc.
- Không chỉnh sửa hoặc xóa dữ liệu gốc.

## 2. Phạm vi các cột cần phân tích

Dataset gốc có nhiều cột, tuy nhiên báo cáo chỉ được phép sử dụng 5 cột:

1. GT Detail
2. Root Cause
3. False Entities
4. Detail False Entities
5. Check

Cột Label chỉ sử dụng để lọc dữ liệu, không đưa vào nội dung thống kê.

Không sử dụng những cột khác để tính toán, phân loại hoặc đưa ra kết luận.

## 3. Cấu trúc phân tích

Bốn cột chính được trình bày theo mức độ chi tiết tăng dần:

**GT Detail → Root Cause → False Entities → Detail False Entities**

Trong đó:
- GT Detail: Cấp độ tổng quan nhất.
- Root Cause: Cấp độ phân tích nguyên nhân.
- False Entities: Cấp độ phân loại entity sai.
- Detail False Entities: Cấp độ mô tả lỗi cụ thể nhất.

Cột Check được sử dụng làm chiều phân tích bổ sung để đối chiếu với các nhóm lỗi.

Không tự giả định quan hệ phân cấp tuyệt đối giữa các giá trị nếu dữ liệu không hỗ trợ.

## 4. Quy tắc xử lý Blank

**Bắt buộc không tính Blank vào bất kỳ phép thống kê liên quan nào.**

- Khi thống kê riêng từng cột, chỉ tính các dòng có giá trị hợp lệ tại cột đó.
- Khi thống kê kết hợp nhiều cột, chỉ tính những dòng có dữ liệu hợp lệ ở tất cả các cột đang tham gia phân tích.
- Không xóa toàn bộ dòng chỉ vì một cột có giá trị Blank.
- Không tính Blank vào mẫu số khi tính Percentage (%).
- Không tự thay thế Blank bằng giá trị khác.
- Xem ô trống, NULL, NaN và chuỗi chỉ chứa khoảng trắng là Blank.
- Giữ nguyên dữ liệu trong worksheet gốc.

## 5. Yêu cầu tạo báo cáo trong Excel

**BẮT BUỘC tạo một worksheet mới có tên "Statistical Report" để chứa toàn bộ báo cáo.**

### A. Summary Statistics

Tạo phần tổng quan bao gồm:
- Tổng số dòng thỏa mãn Label = "good".
- Tổng số dòng hợp lệ của từng cột phân tích.
- Số lượng nhóm phân loại khác nhau của từng cột.
- Tổng quan phân bố các nhóm lỗi.
- Top 5 nhóm xuất hiện nhiều nhất.

### B. Individual Column Statistics

Tạo bảng thống kê riêng cho từng cột:
- GT Detail.
- Root Cause.
- False Entities.
- Detail False Entities.
- Check.

Mỗi bảng phải bao gồm:

| Category | Count | Percentage (%) | Rank |
|---|---|---|---|

Yêu cầu:
- Count: Số lần xuất hiện của từng giá trị.
- Percentage: Count / Tổng số dòng hợp lệ của cột tương ứng.
- Rank: Thứ hạng dựa trên Count giảm dần.
- Loại bỏ Blank hoàn toàn khỏi từng bảng thống kê.
- Sắp xếp theo Count từ cao xuống thấp.

### C. Cross-Analysis

Tạo các bảng thống kê kết hợp:

1. GT Detail × Root Cause.
2. Root Cause × False Entities.
3. False Entities × Detail False Entities.
4. GT Detail × Root Cause × False Entities × Detail False Entities.
5. Check × Root Cause.
6. Check × False Entities.
7. Check × Detail False Entities.

Với mỗi bảng:
- Hiển thị số lượng bản ghi.
- Tính tỷ trọng (%) trên tổng số bản ghi hợp lệ của phép phân tích đó.
- Tính tỷ trọng trong nhóm cha khi phù hợp.
- Loại bỏ các dòng có Blank ở bất kỳ cột nào tham gia phép thống kê.
- Sắp xếp theo tần suất giảm dần.

### D. Visualization

Tạo các biểu đồ trực tiếp trong worksheet "Statistical Report":

- Bar Chart: Top Root Cause.
- Bar Chart: Top False Entities.
- Bar Chart: Top Detail False Entities.
- Biểu đồ phân bố GT Detail.
- Biểu đồ phân bố Check.
- Treemap hoặc biểu đồ phù hợp để thể hiện cấu trúc phân cấp nếu được Excel hỗ trợ.

Ưu tiên sử dụng PivotTable, PivotChart và Slicer nếu môi trường Excel hỗ trợ.

### E. Business Insights

Dựa trên kết quả thống kê, đưa ra các nhận định:

- Root Cause nào xuất hiện nhiều nhất?
- Loại False Entities nào thường xảy ra lỗi nhất?
- Detail False Entities nào xuất hiện nhiều nhất?
- Những nhóm GT Detail nào tập trung nhiều lỗi?
- Mối liên hệ đáng chú ý giữa Root Cause và False Entities là gì?
- Kết quả Check phân bố như thế nào giữa các nhóm?
- Những nhóm lỗi nào cần được ưu tiên kiểm tra hoặc cải thiện?

Mỗi nhận định phải có số liệu cụ thể làm căn cứ.

Không tự suy diễn nguyên nhân hoặc mức độ nghiêm trọng chỉ dựa trên tần suất.

## 6. Yêu cầu trình bày

Thiết kế worksheet "Statistical Report" theo phong cách báo cáo business chuyên nghiệp:

- Bố cục rõ ràng, từ tổng quan đến chi tiết.
- Tiêu đề và các phần được phân chia hợp lý.
- KPI được trình bày nổi bật.
- Bảng thống kê dễ đọc, dễ so sánh.
- Sử dụng màu sắc đồng bộ, chuyên nghiệp.
- Định dạng Count là số nguyên.
- Định dạng Percentage với 2 chữ số thập phân.
- Sắp xếp các nhóm theo Count giảm dần.
- Có thể sử dụng Conditional Formatting để làm nổi bật những nhóm có tần suất cao.
- Không tạo dashboard HTML hoặc file ngoài Excel.
- Ưu tiên công thức và bảng thống kê có thể cập nhật khi dữ liệu thay đổi.

## 7. Kiểm tra tính chính xác

Sau khi hoàn thành, kiểm tra lại:

- Tất cả kết quả chỉ sử dụng các dòng có Label = "good".
- Không có giá trị Blank được tính vào các bảng thống kê.
- Tổng Count của bảng thống kê riêng từng cột bằng số dòng hợp lệ của cột tương ứng.
- Tổng tỷ trọng các nhóm hợp lệ của từng bảng bằng 100%, ngoại trừ sai lệch do làm tròn.
- Không sử dụng dữ liệu từ những cột ngoài phạm vi quy định.
- Không tạo dữ liệu giả hoặc kết quả không có căn cứ.
- Các biểu đồ phải khớp với bảng thống kê.

## 8. Quy định bắt buộc về worksheet

**Toàn bộ báo cáo phải được tạo trên một worksheet mới có tên "Statistical Report".**

- Không chỉnh sửa worksheet gốc.
- Không xóa bất kỳ dữ liệu gốc nào.
- Không ghi đè công thức hoặc giá trị trong các sheet hiện
