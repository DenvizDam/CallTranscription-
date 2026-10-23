# PROMPT – CREATE EXCEL STATISTICAL REPORT (TABLE & MATRIX ONLY)

Hãy đóng vai một chuyên gia Data Analyst, Business Analyst và Excel Reporting Designer.

Sử dụng dataset hiện có trong workbook Excel để **tạo một worksheet mới có tên "Statistical Report"**, xây dựng báo cáo thống kê chuyên nghiệp, chính xác, dễ hiểu và hữu ích cho business.

Báo cáo phải được thiết kế hoàn chỉnh ngay trong Excel, có bố cục khoa học, cân đối, gọn gàng, dễ đọc và hỗ trợ tương tác.

**CÁC YÊU CẦU BẮT BUỘC:**
- Tạo worksheet mới tên "Statistical Report".
- Chỉ sử dụng Table và Matrix, tuyệt đối không tạo Chart hoặc biểu đồ.
- Không chỉnh sửa, xóa hoặc ghi đè dữ liệu ở bất kỳ worksheet nguồn nào.
- Phân bổ tất cả các bảng trong một khu vực thống nhất, không rải rác.
- Tối ưu chiều ngang báo cáo để hạn chế tối đa cuộn ngang.
- Mỗi Table và Matrix phải có Title và Subtitle rõ ràng bằng tiếng Việt.

## 1. Điều kiện lọc bắt buộc

Trước khi thực hiện bất kỳ phép thống kê nào, lọc toàn bộ dataset theo điều kiện:

**Label = "good"**

- Chỉ sử dụng những dòng có Label chính xác bằng "good".
- Loại khỏi phạm vi thống kê tất cả các dòng có Label khác "good" hoặc Blank.
- Toàn bộ Count, Percentage, Table, Matrix và Business Insights phải dựa trên tập dữ liệu đã lọc.
- Không chỉnh sửa dữ liệu nguồn.
- Cột Label chỉ dùng làm điều kiện lọc, không đưa vào bảng phân tích.

## 2. Phạm vi các cột cần thống kê

Dataset gốc có nhiều cột, tuy nhiên chỉ sử dụng 5 cột sau để phân tích:

1. GT Detail
2. Root Cause
3. False Entities
4. Detail False Entities
5. Check

Không sử dụng những cột khác để tính toán, phân loại hoặc đưa ra kết luận.

Giữ nguyên tên trường để dễ đối chiếu với dữ liệu nguồn.

## 3. Cấu trúc phân tích

Phân tích bốn cột chính theo mức độ chi tiết tăng dần:

**GT Detail → Root Cause → False Entities → Detail False Entities**

- GT Detail: Cấp độ tổng quan nhất.
- Root Cause: Cấp độ phân tích nguyên nhân.
- False Entities: Cấp độ phân loại Entity sai.
- Detail False Entities: Cấp độ mô tả lỗi chi tiết nhất.

Cột Check được sử dụng như một chiều phân tích bổ sung, không thuộc cấu trúc phân cấp chính.

Không tự giả định quan hệ cha–con tuyệt đối nếu dữ liệu thực tế không chứng minh điều đó.

## 4. Quy tắc xử lý Blank

**Không tính Blank vào bất kỳ phép thống kê liên quan nào.**

- Khi thống kê từng cột, chỉ loại Blank tại cột đó.
- Khi thống kê kết hợp nhiều cột, chỉ tính các dòng có dữ liệu hợp lệ ở tất cả các cột tham gia.
- Không xóa toàn bộ bản ghi chỉ vì một cột bị Blank.
- Không tính Blank vào mẫu số khi tính Percentage (%).
- Không thay Blank bằng giá trị khác.
- Xem ô trống, NULL, NaN và chuỗi chỉ chứa khoảng trắng là Blank.
- Không chỉnh sửa dữ liệu nguồn.

## 5. Tạo worksheet báo cáo mới

**BẮT BUỘC tạo một worksheet mới có tên "Statistical Report".**

- Toàn bộ Table, Matrix, KPI và kết quả phân tích phải được đặt trên worksheet này.
- Không tạo thêm các sheet phụ không cần thiết.
- Không chỉnh sửa worksheet nguồn.
- Không sao chép toàn bộ dataset gốc sang sheet báo cáo nếu không cần thiết.
- Ưu tiên sử dụng Excel Table, PivotTable hoặc công thức để tham chiếu trực tiếp dữ liệu nguồn.
- Báo cáo phải có khả năng cập nhật khi dữ liệu nguồn thay đổi nếu công cụ Excel hỗ trợ.
- Nếu tên sheet đã tồn tại, không ghi đè; hãy thông báo thay vì tự ý xóa hoặc thay thế.

## 6. Nội dung báo cáo và tiêu đề từng phần

Tổ chức báo cáo thành 5 Section theo trình tự từ tổng quan đến chi tiết.

### SECTION 01 – TỔNG QUAN DỮ LIỆU HỢP LỆ

**Title: "01. Tổng quan dữ liệu sau khi lọc Label = good"**

**Subtitle:** "Thống kê số lượng bản ghi hợp lệ và mức độ đầy đủ dữ liệu của các trường phân tích."

Tạo bảng tổng quan gồm:
- Tổng số bản ghi có Label = "good".
- Số bản ghi hợp lệ của từng cột.
- Số lượng nhóm giá trị khác nhau của từng cột.
- Tỷ lệ dữ liệu hợp lệ trên tổng số bản ghi có Label = "good".

Bảng tổng quan cần được bố trí ngay đầu sheet, ngắn gọn và dễ đọc.

### SECTION 02 – THỐNG KÊ PHÂN BỐ TỪNG NHÓM

Tạo 5 bảng thống kê riêng biệt.

**Table 2.1 – "Phân bố các nhóm GT Detail"**

Subtitle: "Số lượng và tỷ trọng của từng nhóm GT Detail trong dữ liệu hợp lệ."

**Table 2.2 – "Phân bố các nguyên nhân lỗi (Root Cause)"**

Subtitle: "Tần suất xuất hiện của từng nguyên nhân lỗi."

**Table 2.3 – "Phân bố các loại Entity bị sai (False Entities)"**

Subtitle: "Những loại Entity thường xuất hiện lỗi."

**Table 2.4 – "Phân bố các lỗi Entity chi tiết (Detail False Entities)"**

Subtitle: "Các dạng lỗi Entity cụ thể trong dữ liệu."

**Table 2.5 – "Phân bố kết quả kiểm tra (Check)"**

Subtitle: "Số lượng và tỷ trọng của từng giá trị trong cột Check."

Mỗi bảng gồm:
- Category
- Count
- Percentage (%)
- Rank

Yêu cầu:
- Sắp xếp Count giảm dần.
- Không hiển thị Blank.
- Có dòng Total.
- Tổng Count bằng tổng số bản ghi hợp lệ của cột.
- Tổng Percentage bằng 100%, ngoại trừ sai lệch nhỏ do làm tròn.

### SECTION 03 – MATRIX PHÂN TÍCH MỐI LIÊN HỆ

Tạo 6 Matrix:

**Matrix 3.1 – "Phân bố nguyên nhân lỗi theo từng nhóm GT Detail"**
- Rows: GT Detail
- Columns: Root Cause
- Values: Count

**Matrix 3.2 – "Phân bố các loại Entity sai theo nguyên nhân lỗi"**
- Rows: Root Cause
- Columns: False Entities
- Values: Count

**Matrix 3.3 – "Phân bố lỗi Entity chi tiết theo từng loại Entity sai"**
- Rows: False Entities
- Columns: Detail False Entities
- Values: Count

**Matrix 3.4 – "Phân bố kết quả Check theo nguyên nhân lỗi"**
- Rows: Root Cause
- Columns: Check
- Values: Count

**Matrix 3.5 – "Phân bố kết quả Check theo loại Entity sai"**
- Rows: False Entities
- Columns: Check
- Values: Count

**Matrix 3.6 – "Phân bố kết quả Check theo lỗi Entity chi tiết"**
- Rows: Detail False Entities
- Columns: Check
- Values: Count

Yêu cầu:
- Chỉ tính dữ liệu hợp lệ ở những cột đang tham gia Matrix.
- Loại Blank tại các cột đó.
- Có Row Total, Column Total và Grand Total.
- Sắp xếp theo tổng Count giảm dần nếu phù hợp.
- Có Title và Subtitle riêng.
- Sử dụng Conditional Formatting nhẹ để làm nổi bật các giá trị cao.
- Nếu Matrix quá rộng, có thể dùng bảng tổng hợp dạng dài với Filter và Sort để thay thế, nhưng phải giữ nguyên ý nghĩa và đầy đủ dữ liệu thống kê.

### SECTION 04 – THỐNG KÊ PHÂN CẤP CHI TIẾT

**Title: "04. Phân tích lỗi từ tổng quan đến chi tiết"**

**Subtitle:** "Thống kê các tổ hợp lỗi theo chuỗi GT Detail → Root Cause → False Entities → Detail False Entities."

Tạo bảng gồm:
- GT Detail
- Root Cause
- False Entities
- Detail False Entities
- Count
- Percentage (%)

Quy tắc:
- Mỗi dòng là một tổ hợp giá trị xuất hiện trong dataset.
- Gộp các tổ hợp giống nhau.
- Chỉ tính dòng có đủ dữ liệu hợp lệ của cả bốn cột.
- Sắp xếp Count giảm dần.
- Percentage tính trên tổng số bản ghi hợp lệ có đủ cả bốn cột.
- Có Grand Total.
- Cho phép Filter và Sort.

### SECTION 05 – NHÓM LỖI XUẤT HIỆN NHIỀU NHẤT

**Title: "05. Top 10 tổ hợp lỗi xuất hiện nhiều nhất"**

**Subtitle:** "Những tổ hợp lỗi có tần suất cao nhất trong dữ liệu phân cấp chi tiết."

Tạo bảng gồm:
- Rank
- GT Detail
- Root Cause
- False Entities
- Detail False Entities
- Count
- Percentage (%)

Yêu cầu:
- Chọn Top 10 dựa trên Count giảm dần.
- Percentage sử dụng mẫu số từ Section 04.
- Không tính Blank.
- Có thể bổ sung nhận xét ngắn dựa trên số liệu.
- Không tự đánh giá mức độ nghiêm trọng chỉ dựa trên tần suất.

## 7. Yêu cầu bố cục và phân bổ trên worksheet

**ĐÂY LÀ YÊU CẦU ƯU TIÊN CAO.**

Toàn bộ báo cáo phải được phân bổ khoa học, tập trung, cân đối và vừa với không gian hiển thị của Excel.

### 7.1. Tối ưu không gian

- Không bố trí các Table và Matrix rải rác.
- Không để những vùng trống quá lớn.
- Không tạo quá nhiều cột hoặc hàng trống.
- Ưu tiên chiều dọc thay vì trải rộng chiều ngang.
- Hạn chế tối đa việc cuộn ngang.
- Tự điều chỉnh Column Width và Row Height.
- Sử dụng Wrap Text nếu nội dung dài.
- Không để chữ bị cắt, tràn hoặc chồng lấn.
- Không thu nhỏ font quá mức chỉ để ép nội dung vào một màn hình.
- Ưu tiên mức Zoom khoảng 80–90% nếu phù hợp.

### 7.2. Nguyên tắc bố trí bảng

- Bảng nhỏ được đặt cạnh nhau khi vừa chiều ngang.
- Bảng lớn nên được bố trí riêng.
- Matrix nhiều cột phải được tối ưu để dễ đọc.
- Những bảng liên quan nên đặt gần nhau.
- Khoảng cách giữa các bảng khoảng 1–2 hàng hoặc cột trống khi phù hợp.
- Tiêu đề phải nằm ngay phía trên bảng.
- Không để bảng chồng lấn.
- Không đặt bảng ở những cột quá xa khu vực báo cáo chính.

### 7.3. Thứ tự trình bày

1. Tổng quan dữ liệu.
2. Phân bố từng nhóm.
3. Matrix phân tích.
4. Phân tích phân cấp chi tiết.
5. Top 10 tổ hợp lỗi.

Bố trí tất cả theo luồng đọc từ trên xuống dưới.

Người đọc nên chủ yếu chỉ cần cuộn xuống để theo dõi báo cáo.

### 7.4. Tối ưu hiển thị

- Ưu tiên chiều ngang gọn và phù hợp màn hình máy tính thông thường.
- Không cố gắng đưa toàn bộ báo cáo vào một màn hình.
- Cho phép chiều dài worksheet linh hoạt.
- Sử dụng Grouping nếu phù hợp để thu gọn những khu vực dài.
- Đảm bảo các bảng luôn giữ được khả năng đọc và tương tác.

## 8. Khả năng tương tác

- Bật Filter và Sort cho các bảng chi tiết.
- Cho phép sắp xếp theo Count, Percentage và Category.
- Ưu tiên Excel Table hoặc PivotTable khi phù hợp.
- Hỗ trợ Expand/Collapse nếu có cấu trúc phân cấp.
- Có thể dùng Slicer nếu hỗ trợ và không làm rối bố cục.
- Freeze Panes tại vị trí hợp lý.
- Có thể tạo liên kết điều hướng đến từng Section.
- Không dùng Merged Cells trong vùng dữ liệu cần Filter hoặc Sort.
- Không tạo những chức năng lọc gây xung đột giữa các bảng.
- Nếu dùng Slicer, đảm bảo kết nối với đúng bảng cần lọc.

## 9. Yêu cầu thiết kế và tiêu đề

Mỗi Table và Matrix bắt buộc có:
- Title: Tên bảng rõ ràng, mô tả đúng nội dung.
- Subtitle: Một câu ngắn giải thích ý nghĩa của bảng và phạm vi thống kê.

Thiết kế:
- Tiêu đề Section màu xanh navy hoặc xanh dương đậm.
- Header bảng màu xanh nhạt hoặc xám nhạt.
- Nền bảng màu trắng hoặc rất nhạt.
- Sử dụng font dễ đọc, đồng bộ.
- Có đường viền mảnh.
- Header in đậm.
- Total và Grand Total nổi bật.
- Count là số nguyên.
- Percentage có 2 chữ số thập phân.
- Căn trái văn bản.
- Căn phải số liệu.
- Conditional Formatting nhẹ nếu phù hợp.
- Không sử dụng Chart.

## 10. Kiểm tra chất lượng

Sau khi tạo xong worksheet, bắt buộc kiểm tra:

**Về dữ liệu:**
- Tất cả kết quả chỉ dựa trên Label = "good".
- Không tính Blank.
- Count và Percentage chính xác.
- Tổng Count từng bảng khớp với dữ liệu hợp lệ.
- Grand Total Matrix khớp với số dòng hợp lệ đồng thời của các cột tham gia.
- Không sử dụng cột ngoài phạm vi.
- Không thay đổi dữ liệu nguồn.

**Về bố cục:**
- Không có bảng chồng lấn.
- Không có chữ bị cắt.
- Không có bảng rải rác.
- Không có khoảng trắng lớn không cần thiết.
- Hạn chế tối đa cuộn ngang.
- Title và Subtitle rõ ràng.
- Bố cục đồng bộ và có tính thẩm mỹ.

**Về tương tác:**
- Filter và Sort hoạt động đúng.
- PivotTable hoặc Table hoạt động chính xác.
- Không có công thức bị lỗi.
- Không có Chart.

## 11. Mục tiêu cuối cùng

Hãy thực sự tạo một worksheet mới có tên **"Statistical Report"** ngay trong workbook hiện tại.

Kết quả cần đáp ứng:

1. Báo cáo thống kê đầy đủ bằng Table và Matrix.
2. Chỉ dựa trên 5 cột phân tích và điều kiện Label = "good".
3. Loại bỏ Blank đúng cách trong từng phép tính.
4. Có Title và Subtitle rõ ràng cho từng bảng.
5. Bố cục cân đối, tập trung, không rải rác và hạn chế cuộn ngang.
6. Có khả năng Filter, Sort và tương tác.
7. Số liệu chính xác và dễ kiểm tra.
8. Không thay đổi dữ liệu gốc.

**ƯU TIÊN CAO NHẤT: Tính chính xác của số liệu, bố cục gọn gàng và vừa với khu vực hiển thị, tiêu đề dễ hiểu, khả năng tương tác và giá trị thực tế cho business.**

Không chỉ tạo các bảng thống kê đơn thuần. Hãy tổ chức chúng thành một báo cáo Excel thống nhất, logic, chuyên nghiệp và dễ sử dụng.
