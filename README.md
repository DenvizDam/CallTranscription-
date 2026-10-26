# FULL PROMPT – EXCEL HIERARCHICAL ERROR ANALYSIS & TREE DIAGRAM

## 1. VAI TRÒ VÀ MỤC TIÊU

Hãy đóng vai chuyên gia Data Analyst, Business Analyst và Excel Automation Developer.

Sử dụng dataset hiện có trong workbook Excel đang mở để xây dựng một báo cáo phân tích lỗi Speech-to-Text (S2T) và Named Entity Recognition (NER).

**MỤC TIÊU CHÍNH:**

Tạo một sheet thống kê mới, tính toán toàn bộ số liệu từ cấp tổng quan rộng nhất đến cấp chi tiết nhất, sau đó tự động vẽ một Tree Diagram thể hiện đầy đủ các nhánh phân cấp.

Cấu trúc phân tích:

TOTAL RECORDS
→ GT DETAIL
→ GROUP CAUSE
→ FALSE ENTITY
→ DETAIL FALSE ENTITY
→ ROOT CAUSE
→ SOLUTION

Kết quả phải giúp trả lời:

1. Tổng cộng có bao nhiêu record lỗi?
2. S2T và NER có bao nhiêu lỗi?
3. Mỗi Group Cause chiếm bao nhiêu lỗi?
4. Trong từng Group Cause, False Entity nào xuất hiện nhiều nhất?
5. Mỗi False Entity sai Value, Format hoặc giá trị khác bao nhiêu lần?
6. Root Cause cụ thể của từng nhóm lỗi là gì?
7. Các Root Cause dẫn đến những Solution nào?
8. Mỗi nhánh chiếm bao nhiêu phần trăm cấp cha và tổng dataset?
9. Nhánh nào có số lượng lỗi lớn nhất?

**YÊU CẦU QUAN TRỌNG:**

- Chỉ tạo 1 sheet thống kê mới.
- Không tạo workbook mới.
- Không thay đổi dữ liệu gốc.
- Không tạo dữ liệu giả hoặc mô phỏng.
- Không giới hạn các giá trị theo danh sách cố định.
- Không bỏ sót bất kỳ nhánh thực tế nào.
- Sử dụng Tree Diagram bằng Excel Shapes và Connectors.
- Không tạo Sunburst Chart, Treemap hoặc Dashboard HTML.

---

## 2. ĐIỀU KIỆN LỌC DỮ LIỆU

Trước khi thực hiện bất kỳ phép thống kê nào, bắt buộc lọc dataset theo:

**Label = "good"**

Quy tắc:

1. Chỉ lấy những dòng có Label chính xác bằng `"good"`.
2. Phân biệt chữ hoa, chữ thường và khoảng trắng.
3. Loại khỏi tập thống kê mọi dòng có Label khác `"good"` hoặc Blank.
4. Không xóa các dòng bị loại trong dữ liệu nguồn.
5. Không chỉnh sửa giá trị Label.
6. Không tự xóa duplicate.
7. Toàn bộ Count và Percentage phải được tính trên tập dữ liệu sau khi lọc.
8. Nếu một dòng biểu diễn một error record thì mỗi dòng đó được đếm một lần ở mỗi cấp phân loại tương ứng.

Nếu có Case ID hoặc Call ID, không tự động sử dụng DISTINCT COUNT để thay thế số dòng lỗi.

Có thể bổ sung Distinct Case Count như một chỉ số riêng nếu dữ liệu hỗ trợ.

---

## 3. XÁC ĐỊNH CÁC CỘT PHÂN TÍCH

Tìm trong dataset nguồn các cột sau:

1. Label
2. GT Detail
3. Group Cause
4. False Entity
5. Detail False Entity
6. Root Cause
7. Solution hoặc Giải pháp

Phải sử dụng đúng dữ liệu thực tế của từng cột.

Nếu tên cột có sự khác biệt nhỏ, chỉ tự động mapping khi xác định được chính xác cột tương ứng.

Không tự suy diễn mapping khi có nhiều cột cùng khả năng phù hợp.

Nếu không tồn tại cột Solution hoặc Giải pháp:

- Thống kê đến Root Cause.
- Tree Diagram kết thúc ở Root Cause.
- Ghi rõ rằng dataset chưa có cột Solution.
- Không tự tạo hoặc điền giải pháp dựa trên giả định.

---

## 4. CẤU TRÚC PHÂN CẤP CHI TIẾT

Thực hiện thống kê theo đúng thứ tự.

### LEVEL 0 – TOTAL RECORDS

Tổng số dòng sau khi filter Label = "good".

Đây là node gốc của Tree Diagram.

### LEVEL 1 – GT DETAIL

Các giá trị đã biết:

- S2T
- NER

Nếu xuất hiện các giá trị khác, vẫn phải thống kê đầy đủ.

### LEVEL 2 – GROUP CAUSE

Phân loại theo GT Detail + Group Cause.

Các quan hệ đã biết:

NER:
- Business Rule Error
- NER Error

S2T:
- Extra Speech
- Missing / Extra Speech
- Number And Entity Error
- Recognition Error

Nếu dataset có thêm giá trị hoặc tổ hợp khác, phải đưa vào thống kê.

Không tự loại bỏ giá trị chưa có trong danh sách.

### LEVEL 3 – FALSE ENTITY

Phân loại theo:

GT Detail + Group Cause + False Entity

Các giá trị đã biết:

- Address
- Amount
- Amount-Term
- Confirm Sec
- Name

Danh sách này không cố định.

Tự động phát hiện và thống kê các giá trị khác nếu có.

Không giả định một False Entity chỉ thuộc một Group Cause.

Ví dụ:

Nếu Amount xuất hiện ở hai Group Cause khác nhau, phải tạo hai node Amount riêng thuộc đúng nhánh cha.

### LEVEL 4 – DETAIL FALSE ENTITY

Phân loại theo:

GT Detail + Group Cause + False Entity + Detail False Entity

Các giá trị đã biết:

- Value
- Format

Nếu xuất hiện giá trị khác, vẫn phải thống kê.

### LEVEL 5 – ROOT CAUSE

Phân loại theo:

GT Detail + Group Cause + False Entity + Detail False Entity + Root Cause

Các quan hệ đã biết:

NER + Business Rule Error:
- Inconsistency Model

NER + NER Error:
- Detect Dư
- Inconsistency Model

S2T + các Group Cause:
- Prompt Not Detail Enough
- Inconsistency Model

Các giá trị Root Cause mới vẫn phải được thống kê đầy đủ.

Không gộp Inconsistency Model của S2T với Inconsistency Model của NER.

Không tự loại bỏ tổ hợp khác mapping đã biết; chỉ đánh dấu để kiểm tra.

### LEVEL 6 – SOLUTION

Phân loại theo:

GT Detail + Group Cause + False Entity + Detail False Entity + Root Cause + Solution

Các quan hệ giải pháp tham khảo:

- S2T + Inconsistency Model → Review Environment.
- S2T + Prompt Not Detail Enough → Enhance Prompt theo False Entity.
- NER + Inconsistency Model → Enhance Logging / Trace.
- NER + Detect Dư → Review Detection Logic.

Lưu ý:

Đây là mapping tham khảo để kiểm tra chất lượng dữ liệu, không phải dữ liệu được phép tự động điền.

Phải thống kê mọi Solution thực tế trong Excel, kể cả khi khác danh sách trên.

---

## 5. QUY TẮC TỰ ĐỘNG NHẬN DIỆN GIÁ TRỊ MỚI

**ĐÂY LÀ YÊU CẦU BẮT BUỘC.**

Không hard-code danh sách giá trị của bất kỳ cột phân loại nào.

Với mỗi cột phải:

1. Quét toàn bộ dữ liệu sau khi lọc Label.
2. Lấy tất cả giá trị DISTINCT thực tế.
3. Không giới hạn Top 5, Top 10 hoặc Top 100.
4. Không bỏ qua các giá trị hiếm gặp.
5. Không tự chuẩn hóa hoặc sửa chính tả.
6. Không tự gộp những giá trị có tên gần giống nhau.
7. Giữ riêng Blank / Null.
8. Không làm mất quan hệ với cấp cha.
9. Không tự tạo tổ hợp không tồn tại.
10. Tự động bổ sung giá trị mới khi thống kê được cập nhật.

Phải phân biệt giữa:

- Giá trị Blank / Null thực tế trong dataset.
- Ô trống do một Level chưa áp dụng.

Dùng nhãn hiển thị `(Blank)` cho giá trị thiếu, nhưng vẫn giữ khả năng phân biệt với giá trị văn bản thực sự là `(Blank)`.

---

## 6. CÁCH TÍNH SỐ LIỆU

Mỗi node trong Tree Diagram phải có các chỉ số:

### 6.1. COUNT

Số record thuộc node đang xét.

Count được tính theo tổ hợp toàn bộ các cấp cha và cấp hiện tại.

### 6.2. PARENT COUNT

Số record thuộc node cha trực tiếp.

### 6.3. % OF PARENT

Công thức:

% of Parent = Count / Parent Count × 100

### 6.4. % OF TOTAL

Công thức:

% of Total = Count / Total Records × 100

### 6.5. RANK

Xếp hạng các node con theo Count giảm dần trong cùng một node cha.

Các node có Count lớn nhất được ưu tiên hiển thị trước.

### VÍ DỤ CÁCH TÍNH

Ví dụ mô phỏng:

TOTAL = 1.000

S2T = 700

Recognition Error = 280

Amount = 100

Value = 80

Prompt Not Detail Enough = 60

Enhance Amount Prompt = 60

Khi đó:

- S2T = 70% tổng.
- Recognition Error = 40% S2T.
- Amount = 35,71% Recognition Error.
- Value = 80% Amount.
- Prompt Not Detail Enough = 75% Value.
- Enhance Amount Prompt = 100% Root Cause tương ứng.

Chỉ sử dụng ví dụ này để hiểu phương pháp tính.

Tuyệt đối không đưa số liệu mô phỏng vào kết quả thực tế.

Lưu ý: Không cộng Count của tất cả Level với nhau, vì cùng một record được thống kê tại nhiều cấp.

---

## 7. CHỈ TẠO MỘT SHEET MỚI

Tạo đúng một sheet mới trong workbook Excel hiện tại.

Tên sheet:

**Hierarchical_Statistics**

Không tạo workbook mới.

Không tạo thêm sheet khác.

Không xóa, chỉnh sửa hoặc ghi đè sheet nguồn.

Nếu sheet `Hierarchical_Statistics` đã tồn tại, tạo sheet với hậu tố mới phù hợp.

Bố trí trong sheet gồm bốn khu vực:

**AREA A – OVERALL SUMMARY**

Tổng quan số liệu.

**AREA B – FULL HIERARCHICAL STATISTICS TABLE**

Bảng thống kê đầy đủ từ Level 0 đến Level 6.

**AREA C – TREE DIAGRAM**

Sơ đồ cây phân cấp được vẽ từ bảng thống kê.

**AREA D – DATA VALIDATION**

Bảng đối chiếu tính chính xác của số liệu.

Chỉ tạo bốn khu vực trong cùng một sheet.

Phải bố trí vị trí phù hợp để dữ liệu và các đối tượng Excel không chồng lấn, kể cả khi số dòng tăng sau Refresh.

---

## 8. AREA A – OVERALL SUMMARY

Tạo bảng tổng quan với các chỉ số:

| Metric | Count |
|---|---:|
| Total Source Records | |
| Total Valid Records (Label = good) | |
| Excluded Records | |
| GT Detail Distinct Count | |
| Group Cause Distinct Count | |
| False Entity Distinct Count | |
| Detail False Entity Distinct Count | |
| Root Cause Distinct Count | |
| Solution Distinct Count | |

Bổ sung các bảng tổng hợp nhỏ để hiển thị:

- Count theo GT Detail.
- Count theo Group Cause.
- Count theo False Entity.
- Count theo Root Cause.

Các bảng tổng hợp được phép nằm trong cùng AREA A nếu không gây chồng lấn.

Không tạo chart.

---

## 9. AREA B – FULL HIERARCHICAL STATISTICS TABLE

Tạo một Excel Table chứa các cột:

| Column | Description |
|---|---|
| Level | Cấp phân loại 0–6 |
| Node ID | Mã node duy nhất |
| Parent ID | Mã node cha |
| GT Detail | GT Detail |
| Group Cause | Group Cause |
| False Entity | False Entity |
| Detail False Entity | Detail False Entity |
| Root Cause | Root Cause |
| Solution | Giải pháp thực tế |
| Count | Số record |
| Parent Count | Số record của node cha |
| % of Parent | Tỷ lệ trong node cha |
| % of Total | Tỷ lệ trong toàn bộ dữ liệu |
| Rank in Parent | Thứ hạng trong cùng node cha |
| Hierarchy Path | Đường dẫn phân cấp |

### Yêu cầu cấu trúc

Mỗi dòng đại diện cho một node.

Ví dụ:

Level 0: TOTAL.

Level 1: S2T, NER và các giá trị GT Detail khác nếu có.

Level 2: Tất cả Group Cause dưới từng GT Detail.

Level 3: Tất cả False Entity dưới từng Group Cause.

Level 4: Tất cả Detail False Entity dưới từng False Entity.

Level 5: Tất cả Root Cause dưới từng Detail False Entity.

Level 6: Tất cả Solution dưới từng Root Cause.

### Node ID và Parent ID

Phải đảm bảo:

- Node ID duy nhất cho mỗi node.
- Parent ID tham chiếu đúng node cha.
- Node cùng tên nhưng khác nhánh cha phải có Node ID riêng.
- Node ID được tạo một cách nhất quán.
- Không dùng riêng tên giá trị làm Node ID.
- Hierarchy Path giữ đầy đủ thứ tự và giá trị các cấp.
- Nếu giá trị chứa ký tự phân cách đặc biệt thì Hierarchy Path vẫn phải phân biệt chính xác các tổ hợp.

### Sắp xếp

Sắp xếp theo cấu trúc cây:

- Node cha xuất hiện trước node con.
- Các node con cùng cấp được sắp xếp theo Count giảm dần.
- Nếu Count bằng nhau, dùng thứ tự tên nhất quán.

Không sort toàn bảng chỉ theo Count vì sẽ làm mất thứ tự phân cấp.

### Filter

Bật Excel Table Filter cho toàn bộ các cột.

Cho phép kiểm tra dữ liệu theo:

- Level
- GT Detail
- Group Cause
- False Entity
- Detail False Entity
- Root Cause
- Solution
- Count
- % of Parent
- % of Total

Không giới hạn số dòng trong báo cáo nếu Excel còn đủ khả năng lưu trữ.

---

## 10. AREA C – AUTOMATIC TREE DIAGRAM

**ĐÂY LÀ YÊU CẦU QUAN TRỌNG NHẤT CỦA BÁO CÁO.**

Sau khi hoàn thành bảng thống kê, hãy thực sự tự động vẽ một Tree Diagram ngay trong sheet `Hierarchical_Statistics`.

### 10.1. Loại diagram

Sử dụng:

**TREE DIAGRAM – HIERARCHICAL FLOWCHART**

Được xây dựng bằng:

- Excel Shapes.
- Excel Connectors.
- Text trong từng Shape.
- Các đối tượng có thể chỉnh sửa trực tiếp trong Excel.

Không sử dụng:

- Sunburst Chart.
- Treemap.
- Pie Chart.
- Bar Chart.
- Hình ảnh tĩnh.
- HTML Diagram.

### 10.2. Cấu trúc diagram

Vẽ theo thứ tự:

TOTAL RECORDS
↓
GT DETAIL
↓
GROUP CAUSE
↓
FALSE ENTITY
↓
DETAIL FALSE ENTITY
↓
ROOT CAUSE
↓
SOLUTION

Mỗi node phải nối đúng với node cha theo Parent ID đã tính.

### 10.3. Nội dung hiển thị trên từng node

Mỗi node cần hiển thị:

**Node Name**

Count: XXX

Parent: XX.XX%

Total: XX.XX%

Trong đó:

- Node Name là giá trị thực tế của cấp hiện tại.
- Count là số record của node.
- Parent là % of Parent.
- Total là % of Total.

Đối với TOTAL, chỉ cần hiển thị Count và 100% Total.

### 10.4. Vẽ đầy đủ tất cả các nhánh

Yêu cầu bắt buộc:

1. Vẽ toàn bộ GT Detail.
2. Vẽ toàn bộ Group Cause thuộc mỗi GT Detail.
3. Vẽ toàn bộ False Entity thuộc mỗi Group Cause.
4. Vẽ toàn bộ Detail False Entity thuộc từng False Entity.
5. Vẽ toàn bộ Root Cause thuộc từng Detail False Entity.
6. Vẽ toàn bộ Solution thuộc từng Root Cause.
7. Không giới hạn số nhánh theo danh sách giá trị đã biết.
8. Không tự bỏ các node có Count nhỏ.
9. Không gộp các node có cùng tên nhưng thuộc nhánh cha khác nhau.
10. Không tạo thêm node cho những tổ hợp không tồn tại trong dữ liệu.

Nếu Solution không tồn tại, diagram kết thúc ở Root Cause.

### 10.5. Quy tắc sắp xếp node

Trong từng node cha:

- Node con có Count lớn hơn được xếp trước.
- Node con có Count nhỏ hơn được xếp sau.
- Các node con phải được hiển thị liền kề trong cùng một nhánh.
- Không để các đường nối giữa những nhánh khác nhau gây hiểu nhầm.

### 10.6. Thiết kế diagram

Thiết kế đơn giản, tập trung vào số liệu.

Yêu cầu:

- Nền trắng.
- Chữ đen hoặc xám đậm.
- Hình chữ nhật đơn giản.
- Viền mảnh.
- Kích thước node đồng nhất theo từng cấp.
- Font dễ đọc.
- Đường kết nối rõ ràng.
- Không cần màu sắc trang trí.
- Không dùng icon không cần thiết.
- Không sử dụng hiệu ứng 3D.
- Không để chữ vượt ra ngoài Shape.
- Không để Shape hoặc Connector chồng lên nhau.

Có thể sử dụng màu rất nhẹ để phân biệt S2T và NER nếu thực sự cần thiết, nhưng không bắt buộc.

Ưu tiên thể hiện đầy đủ thông tin hơn tính thẩm mỹ.

### 10.7. Tự động bố trí diagram

Sử dụng thuật toán bố trí cây từ dữ liệu Node ID và Parent ID.

Ưu tiên vẽ từ trái sang phải:

- Level 0 nằm ngoài cùng bên trái.
- Level 1 nằm ở cột tiếp theo.
- Tiếp tục đến Level 6 bên phải.

Khoảng cách giữa các node phải được tính dựa trên số lượng node con và kích thước nhánh.

Mỗi nhánh cha phải có đủ không gian cho toàn bộ các nhánh con.

Không đặt các node theo tọa độ cố định nếu điều đó có thể dẫn đến chồng lấn khi số nhánh tăng.

Nếu diagram quá lớn:

- Cho phép mở rộng theo chiều ngang và chiều dọc của worksheet.
- Không tự cắt bỏ node.
- Không tự giới hạn Top N.
- Không ép tất cả node vào một khung nhỏ khiến chữ không đọc được.
- Nếu gặp giới hạn thực tế của Excel, phải báo cáo rõ số node chưa thể vẽ và lý do.

### 10.8. Đồng bộ diagram với số liệu

Diagram phải sử dụng trực tiếp dữ liệu từ Full Hierarchical Statistics Table.

Không nhập tay Count và Percentage vào sơ đồ.

Khi dữ liệu được thống kê lại, diagram phải có thể được tạo lại theo dữ liệu mới.

Node Name, Count, Parent Count và Percentage phải khớp chính xác với bảng thống kê.

Nếu làm mới diagram, phải xử lý các Shapes và Connectors cũ thuộc diagram trước đó để tránh nhân đôi, nhưng không xóa các đối tượng không liên quan.

---

## 11. PHƯƠNG PHÁP TỰ ĐỘNG HÓA TREE DIAGRAM

Ưu tiên sử dụng Excel VBA với:

- Shapes.AddShape
- Shapes.AddConnector
- TextFrame hoặc TextFrame2
- Các phương thức định vị và kết nối Shapes

Nếu môi trường có công cụ tự động hóa Excel khác hỗ trợ đầy đủ Shapes và Connectors, có thể sử dụng công cụ đó.

Quy trình:

1. Đọc dữ liệu nguồn.
2. Filter Label = "good".
3. Thống kê toàn bộ các tổ hợp.
4. Tạo Hierarchical Statistics Table.
5. Sinh Node ID và Parent ID.
6. Xác định số lượng node ở từng level.
7. Tính bố cục dựa trên kích thước các nhánh con.
8. Tạo Shape cho từng node.
9. Tạo Connector theo Parent ID.
10. Hiển thị Count và Percentage.
11. Kiểm tra các đường nối.
12. Đối chiếu diagram với bảng thống kê.

Nếu cần sử dụng VBA và workbook hiện tại là `.xlsx`, không được tự ý chuyển định dạng hoặc lưu thành file khác. Hãy sử dụng phương án tự động hóa bên ngoài workbook nếu được hỗ trợ, hoặc yêu cầu quyền sử dụng/lưu macro phù hợp.

Không tự ý thay đổi bảo mật hoặc bật macro.

Nếu môi trường hiện tại không thể thực thi VBA hoặc không hỗ trợ tạo Shapes tự động, phải nêu rõ giới hạn và vẫn hoàn thành bảng thống kê cùng sơ đồ phân cấp dạng văn bản trong sheet. Không được tuyên bố đã tạo Tree Diagram bằng Shapes nếu chưa thực sự tạo thành công.

---

## 12. AREA D – DATA VALIDATION

Tạo bảng kiểm tra chất lượng số liệu.

| Validation | Expected | Actual | Difference | Status |
|---|---:|---:|---:|---|

### CHECK 1 – TOTAL

Tổng Count Level 1 phải bằng Total Records.

### CHECK 2 – GROUP CAUSE

Tổng Count các Group Cause thuộc từng GT Detail phải bằng Count của GT Detail đó.

### CHECK 3 – FALSE ENTITY

Tổng Count False Entity của từng nhánh Group Cause phải bằng Count của Group Cause tương ứng.

### CHECK 4 – DETAIL FALSE ENTITY

Tổng Count Detail False Entity thuộc từng False Entity phải bằng Count của False Entity tương ứng.

### CHECK 5 – ROOT CAUSE

Tổng Count Root Cause thuộc mỗi nhánh Detail False Entity phải bằng Count của nhánh cha tương ứng.

### CHECK 6 – SOLUTION

Nếu có Solution, tổng Count Solution thuộc mỗi Root Cause phải bằng Count của Root Cause đó.

### CHECK 7 – NODE RELATIONSHIP

Kiểm tra:

- Mỗi node ngoài TOTAL có Parent ID hợp lệ.
- Không có node trùng Node ID.
- Không tồn tại node không có cha.
- Không tồn tại vòng lặp phân cấp.
- Level của node con phải lớn hơn Level của node cha đúng một cấp.

### CHECK 8 – DIAGRAM COMPLETENESS

Kiểm tra:

- Số node trong diagram bằng số node trong bảng thống kê.
- Số Connector bằng số node ngoài node TOTAL.
- Mỗi Connector nối đúng Parent ID.
- Không bỏ sót nhánh thực tế.

Nếu không thể vẽ đầy đủ, đánh dấu FAIL và ghi số lượng node bị thiếu.

### CHECK 9 – DATA QUALITY

Kiểm tra:

- Blank / Null.
- Giá trị DISTINCT mới.
- Giá trị khác mapping dự kiến.
- Giá trị có khoảng trắng bất thường.
- Tổ hợp phân loại không hợp lệ theo mapping đã biết.
- Các dòng có nhiều giá trị trong cùng một ô.

Không tự sửa dữ liệu gốc.

Mọi kiểm tra phải có trạng thái PASS / FAIL rõ ràng.

---

## 13. YÊU CẦU FILTER VÀ REFRESH

Bảng thống kê phải cho phép filter theo từng cấp phân loại.

Ví dụ:

- Filter GT Detail = S2T.
- Filter Group Cause = Number And Entity Error.
- Filter False Entity = Amount.
- Filter Detail False Entity = Value.
- Filter Root Cause = Prompt Not Detail Enough.

Khi đó, bảng phải hiển thị đúng các node và số liệu phù hợp.

Lưu ý:

Filter trong Excel Table không tự động làm thay đổi Tree Diagram trừ khi có logic đồng bộ riêng.

Yêu cầu tối thiểu là Tree Diagram phản ánh toàn bộ dataset đã lọc Label = "good".

Nếu môi trường hỗ trợ, bổ sung khả năng vẽ lại diagram cho một nhánh được lựa chọn mà không thay đổi Count và Percentage gốc.

Khi dữ liệu nguồn thay đổi, cần có quy trình Refresh:

1. Đọc lại dataset.
2. Lọc lại Label.
3. Tính lại bảng thống kê.
4. Cập nhật Node ID và Parent ID.
5. Vẽ lại Tree Diagram.
6. Chạy lại Data Validation.

Không được coi Refresh bảng là đã cập nhật diagram nếu Shapes chưa được làm mới.

---

## 14. BỐ CỤC VÀ ĐỊNH DẠNG SHEET

Tên sheet:

Hierarchical_Statistics

Bố trí đề xuất:

**AREA A – OVERALL SUMMARY:** Phía trên bên trái.

**AREA B – FULL HIERARCHICAL TABLE:** Phía dưới Summary, bắt đầu từ cột A.

**AREA C – TREE DIAGRAM:** Bên phải bảng thống kê, bắt đầu từ một vùng cột đủ xa để không chồng lên bảng.

**AREA D – DATA VALIDATION:** Trong khu vực riêng, không chồng lấn với bảng hoặc diagram.

Yêu cầu:

- Bật Filter ở bảng thống kê.
- Freeze Header phù hợp.
- Count hiển thị số nguyên.
- Percentage hiển thị 2 chữ số thập phân.
- AutoFit cột trong giới hạn dễ đọc.
- Không cắt bớt tên giá trị.
- Không để các Shape đè lên dữ liệu.
- Không dùng màu sắc quá nhiều.
- Không tạo thêm sheet.
- Không tạo workbook mới.

---

## 15. KẾT QUẢ CUỐI CÙNG

Sau khi hoàn thành, trong workbook hiện tại phải có một sheet `Hierarchical_Statistics` chứa:

**1. Overall Summary**

Số liệu tổng quan sau khi filter Label = "good".

**2. Full Hierarchical Statistics Table**

Toàn bộ số liệu phân cấp từ Total đến Solution.

**3. Complete Tree Diagram**

Sơ đồ cây với đầy đủ các node và đường nối, sử dụng Excel Shapes và Connectors.

**4. Data Validation**

Kết quả đối chiếu số liệu và kiểm tra độ đầy đủ của diagram.

### TIÊU CHUẨN HOÀN THÀNH

Báo cáo chỉ được coi là hoàn thành đầy đủ khi:

- Dữ liệu nguồn được giữ nguyên.
- Điều kiện Label = "good" được áp dụng chính xác.
- Tất cả giá trị DISTINCT đều được thống kê.
- Mọi tổ hợp thực tế đều có trong bảng.
- Count và Percentage chính xác.
- Parent ID và Node ID đúng.
- Diagram có đầy đủ node thực tế.
- Các Connector nối đúng quan hệ cha–con.
- Không có số liệu mô phỏng trong kết quả.
- Data Validation được thực hiện.
- Tất cả kết quả nằm trong một sheet mới.

**ƯU TIÊN CAO NHẤT:**

TÍNH CHÍNH XÁC → TÍNH ĐẦY ĐỦ → ĐÚNG QUAN HỆ PHÂN CẤP → KHẢ NĂNG KIỂM TRA → TÍNH DỄ ĐỌC.

Hãy thực sự tạo sheet thống kê và Tree Diagram bằng các công cụ Excel hiện có, không chỉ viết hướng dẫn hoặc mô tả các bước thực hiện.

Nếu có giới hạn kỹ thuật khiến một phần không thực hiện được, phải báo cáo rõ phần đã hoàn thành, phần chưa hoàn thành và nguyên nhân, không tự thay thế bằng kết quả giả.

**KẾT THÚC PROMPT.**
