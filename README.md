# FULL PROMPT – EXCEL HIERARCHICAL ERROR ANALYSIS & AUTOMATIC TREE DIAGRAM

## 1. VAI TRÒ VÀ MỤC TIÊU

Hãy đóng vai một chuyên gia Data Analyst, Business Analyst và Excel Automation Developer.

Sử dụng dữ liệu trong sheet **`DB Records`** của workbook Excel hiện tại để xây dựng báo cáo phân tích lỗi Speech-to-Text (S2T) và Named Entity Recognition (NER).

**MỤC TIÊU CHÍNH:**

Tạo duy nhất một sheet thống kê mới có tên:

`Hierarchical_Statistics`

Sheet này phải bao gồm:

1. Overall Summary – Tổng quan dữ liệu.
2. Full Hierarchical Statistics – Thống kê đầy đủ mọi cấp phân loại.
3. Automatic Tree Diagram – Sơ đồ cây thể hiện tất cả nhánh thực tế.
4. Data Validation – Kiểm tra độ chính xác và đầy đủ của số liệu.

Thống kê theo đúng cấu trúc:

**TOTAL RECORDS → GT DETAIL → GROUP CAUSE → FALSE ENTITY → DETAIL FALSE ENTITY → ROOT CAUSE → SOLUTION**

Mỗi cấp phải cung cấp:

- Count – Số lượng record.
- Parent Count – Tổng số record thuộc node cha.
- % of Parent – Tỷ lệ so với node cha.
- % of Total – Tỷ lệ so với tổng dữ liệu.
- Rank in Parent – Thứ hạng trong cùng node cha.
- Node ID và Parent ID – Quan hệ phân cấp.

**YÊU CẦU BẮT BUỘC:**

- Chỉ tạo một sheet mới trong workbook hiện tại.
- Không tạo workbook hoặc file Excel mới.
- Không sửa, xóa hoặc ghi đè dữ liệu nguồn.
- Không sử dụng dữ liệu mô phỏng.
- Không giới hạn các giá trị hoặc tổ hợp phân loại.
- Chỉ sử dụng dữ liệu thực tế.
- Vẽ Tree Diagram bằng Excel Shapes và Connectors.
- Không sử dụng Sunburst, Treemap hoặc các chart khác.

---

## 2. DATA SOURCE – SHEET NGUỒN

**SOURCE SHEET: `DB Records`**

Bắt buộc sử dụng sheet có tên chính xác:

`DB Records`

Quy định:

1. Chỉ sử dụng dữ liệu từ `DB Records`.
2. Không tự tìm hoặc sử dụng sheet khác làm nguồn.
3. Không chỉnh sửa bất kỳ ô nào trong sheet nguồn.
4. Không xóa, ghi đè, thay đổi cấu trúc hoặc format dữ liệu nguồn.
5. Không xóa duplicate nếu chưa có quy tắc xác định duplicate.
6. Mỗi dòng dữ liệu hợp lệ được tính là một record.
7. Chỉ sử dụng vùng dữ liệu thực tế có header hợp lệ; không tính các dòng trống hoặc dòng tổng hợp ngoài dataset.
8. Nếu không tìm thấy sheet `DB Records`, phải báo lỗi rõ ràng, không tự chọn sheet thay thế.

### ĐIỀU KIỆN LỌC BẮT BUỘC

Trước khi thống kê, lọc theo:

**Label = "good"**

Yêu cầu:

- Chỉ chọn giá trị chính xác bằng `"good"`.
- Phân biệt chữ hoa/chữ thường.
- Phân biệt khoảng trắng đầu/cuối.
- Không lấy `"Good"`, `"GOOD"`, `" good"` hoặc `"good "`.
- Không đưa các dòng Label khác `"good"` hoặc Blank vào thống kê.
- Không chỉnh sửa giá trị Label trong dữ liệu nguồn.
- Việc đếm phải áp dụng trên toàn bộ dataset nguồn thỏa điều kiện, không chỉ các dòng đang hiển thị do filter thủ công.

Tất cả Count và Percentage phải dựa trên tập dữ liệu sau khi lọc.

---

## 3. CÁC CỘT CẦN PHÂN TÍCH

Đọc các cột từ sheet `DB Records`:

1. `Label`
2. `GT Detail`
3. `Group Cause`
4. `False Entity`
5. `Detail False Entity`
6. `Root Cause`
7. `Solution` hoặc cột `Giải pháp` tương ứng.

Phải nhận diện đúng tên header thực tế.

Nếu tên cột Solution có khác biệt, chỉ mapping khi xác định được chính xác.

Nếu không tồn tại cột Solution:

- Không tự tạo giá trị Solution.
- Thống kê và vẽ Tree Diagram đến Root Cause.
- Ghi rõ Solution không tồn tại trong dữ liệu nguồn.
- Không làm gián đoạn việc thống kê các cấp còn lại.

Các cột phân loại không được tự sửa hoặc chuẩn hóa giá trị.

---

## 4. CẤU TRÚC HIERARCHY

### LEVEL 0 – TOTAL RECORDS

Đây là node gốc.

Count = Tổng số dòng có Label = "good".

### LEVEL 1 – GT DETAIL

Các giá trị đã biết:

- S2T
- NER

Nếu có giá trị mới, vẫn phải thống kê.

Mỗi giá trị GT Detail là một node con của TOTAL.

### LEVEL 2 – GROUP CAUSE

Phân loại theo:

GT Detail → Group Cause

Mapping đã biết:

**NER**
- Business Rule Error
- NER Error

**S2T**
- Extra Speech
- Missing / Extra Speech
- Number And Entity Error
- Recognition Error

Nếu xuất hiện Group Cause mới, phải tự động bổ sung vào hierarchy.

Không giới hạn danh sách.

### LEVEL 3 – FALSE ENTITY

Phân loại theo:

GT Detail → Group Cause → False Entity

Các giá trị đã biết:

- Address
- Amount
- Amount-Term
- Confirm Sec
- Name

Nếu xuất hiện các giá trị mới, ví dụ Phone Number, Proposal Number, Agent Code, Term hoặc bất kỳ giá trị nào khác, phải tự động đưa vào thống kê.

Không giả định False Entity nào chỉ thuộc một Group Cause.

Nếu Amount xuất hiện trong nhiều Group Cause, phải tạo các node Amount riêng theo đúng nhánh cha.

### LEVEL 4 – DETAIL FALSE ENTITY

Phân loại theo:

GT Detail → Group Cause → False Entity → Detail False Entity

Các giá trị đã biết:

- Value
- Format

Nếu có giá trị mới, vẫn phải thống kê.

### LEVEL 5 – ROOT CAUSE

Phân loại theo:

GT Detail → Group Cause → False Entity → Detail False Entity → Root Cause

Mapping đã biết:

**NER + Business Rule Error**
- Inconsistency Model

**NER + NER Error**
- Detect Dư
- Inconsistency Model

**S2T + các Group Cause**
- Prompt Not Detail Enough
- Inconsistency Model

Không gộp Inconsistency Model của S2T với Inconsistency Model của NER.

Nếu có Root Cause mới hoặc tổ hợp khác mapping đã biết, vẫn phải thống kê và đánh dấu để kiểm tra.

### LEVEL 6 – SOLUTION

Phân loại theo:

GT Detail → Group Cause → False Entity → Detail False Entity → Root Cause → Solution

Mapping giải pháp tham khảo:

**S2T**
- Inconsistency Model → Review Environment.
- Prompt Not Detail Enough → Enhance Prompt theo từng False Entity.

**NER**
- Inconsistency Model → Enhance Logging / Trace.
- Detect Dư → Review Detection Logic.

Đây là mapping tham khảo, không phải dữ liệu dùng để tự động điền.

Bắt buộc lấy các Solution thực tế từ sheet `DB Records`.

Nếu có thêm Solution mới, vẫn phải thống kê.

---

## 5. TỰ ĐỘNG PHÁT HIỆN TẤT CẢ GIÁ TRỊ

**KHÔNG HARD-CODE DANH SÁCH GIÁ TRỊ.**

Với mỗi cột phân loại:

1. Quét toàn bộ dữ liệu sau khi filter Label.
2. Phát hiện mọi giá trị DISTINCT.
3. Không giới hạn Top N.
4. Không bỏ qua giá trị có tần suất nhỏ.
5. Không tự sửa chính tả.
6. Không tự gộp các giá trị gần giống nhau.
7. Không tự chuẩn hóa chữ hoa, chữ thường hoặc khoảng trắng.
8. Thống kê riêng Blank / Null.
9. Không tạo tổ hợp không tồn tại trong dataset.
10. Nếu một giá trị xuất hiện dưới nhiều node cha, phải tạo node riêng cho từng nhánh.

Phân biệt rõ:

- Blank thực tế trong dữ liệu.
- Level chưa áp dụng nên không có giá trị.

Sử dụng nhãn hiển thị riêng cho Missing/Blank để không làm mất record, nhưng không được gộp với chuỗi văn bản thật có cùng tên nhãn.

Nếu một ô chứa nhiều giá trị phân loại, giữ nguyên nội dung ô như một giá trị tại cấp đó, không tự tách thành nhiều record.

---

## 6. PHƯƠNG PHÁP THỐNG KÊ

### COUNT

Số record thuộc node hiện tại.

Mỗi node được xác định bằng toàn bộ tổ hợp giá trị từ Level 1 đến Level hiện tại.

### PARENT COUNT

Số record thuộc node cha trực tiếp.

### % OF PARENT

Count / Parent Count

Định dạng kết quả dưới dạng Percentage với 2 chữ số thập phân.

### % OF TOTAL

Count / Total Valid Records

Định dạng dưới dạng Percentage với 2 chữ số thập phân.

### RANK IN PARENT

Xếp hạng các node con theo Count giảm dần trong cùng node cha.

Nếu hai node có Count bằng nhau, áp dụng cùng một quy tắc xếp hạng nhất quán.

### VÍ DỤ MINH HỌA

Giả sử:

TOTAL = 1.000

S2T = 700

Recognition Error = 280

Amount = 100

Value = 80

Prompt Not Detail Enough = 60

Enhance Amount Prompt = 60

Kết quả:

- S2T: 700 / 1.000 = 70%.
- Recognition Error: 280 / 700 = 40%.
- Amount: 100 / 280 = 35,71%.
- Value: 80 / 100 = 80%.
- Prompt Not Detail Enough: 60 / 80 = 75%.
- Enhance Amount Prompt: 60 / 60 = 100%.

**Không sử dụng các số liệu mô phỏng này trong báo cáo thực tế.**

Không cộng Count của tất cả Level lại với nhau vì mỗi record được biểu diễn ở nhiều cấp.

---

## 7. TẠO DUY NHẤT MỘT SHEET MỚI

Tên sheet:

**`Hierarchical_Statistics`**

Chỉ tạo sheet này trong workbook hiện tại.

Nếu tên sheet đã tồn tại, tạo tên mới có hậu tố phù hợp, không ghi đè sheet cũ.

Chia sheet thành bốn khu vực:

### AREA A – OVERALL SUMMARY

Hiển thị:

- Total Source Records.
- Total Valid Records (Label = good).
- Excluded Records.
- GT Detail Distinct Count.
- Group Cause Distinct Count.
- False Entity Distinct Count.
- Detail False Entity Distinct Count.
- Root Cause Distinct Count.
- Solution Distinct Count, nếu có.

Thêm bảng nhỏ thống kê Count theo các cột chính.

### AREA B – FULL HIERARCHICAL STATISTICS TABLE

Đây là bảng dữ liệu quan trọng nhất.

Tạo Excel Table gồm các cột:

| Column | Description |
|---|---|
| Level | Cấp 0 đến 6 |
| Node ID | Định danh node duy nhất |
| Parent ID | Định danh node cha |
| Node Name | Tên giá trị tại level hiện tại |
| GT Detail | Giá trị GT Detail |
| Group Cause | Giá trị Group Cause |
| False Entity | Giá trị False Entity |
| Detail False Entity | Giá trị Detail False Entity |
| Root Cause | Giá trị Root Cause |
| Solution | Giá trị Solution thực tế |
| Count | Số record |
| Parent Count | Số record thuộc node cha |
| % of Parent | Tỷ lệ so với cha |
| % of Total | Tỷ lệ so với tổng |
| Rank in Parent | Thứ hạng trong node cha |
| Hierarchy Path | Đường dẫn từ TOTAL đến node |

**QUY TẮC QUAN TRỌNG:**

Mỗi dòng phải đại diện cho một node riêng biệt.

- Level 0: Một node TOTAL.
- Level 1: Tất cả GT Detail.
- Level 2: Tất cả Group Cause trong từng GT Detail.
- Level 3: Tất cả False Entity trong từng Group Cause.
- Level 4: Tất cả Detail False Entity trong từng False Entity.
- Level 5: Tất cả Root Cause trong từng nhánh tương ứng.
- Level 6: Tất cả Solution thực tế trong từng Root Cause.

### NODE ID VÀ PARENT ID

Yêu cầu:

- Node ID là duy nhất.
- Parent ID phải trỏ đến đúng Node ID của node cha.
- Hai node có cùng tên nhưng khác nhánh cha không được dùng chung Node ID.
- Node ID phải được tạo một cách nhất quán và không phụ thuộc đơn thuần vào tên giá trị.
- Parent ID của TOTAL được để trống.
- Hierarchy Path phải thể hiện đầy đủ các cấp và tránh nhập nhằng khi giá trị chứa ký tự đặc biệt.

### SORTING

Sắp xếp theo cấu trúc cây:

- Node cha trước node con.
- Các node con có Count lớn hơn được xếp trước.
- Không sort toàn bộ bảng chỉ theo Count vì sẽ làm mất cấu trúc phân cấp.

### FILTER

Bật AutoFilter trên toàn bộ bảng.

Cho phép filter theo từng cột hoặc kết hợp nhiều cột.

Không giới hạn số dòng thống kê.

---

## 8. AREA C – AUTOMATIC TREE DIAGRAM

**PHẢI THỰC SỰ VẼ TREE DIAGRAM TRONG EXCEL.**

Không chỉ mô tả cách vẽ.

### 8.1. CÔNG NGHỆ

Ưu tiên sử dụng:

- Excel Shapes.
- Excel Connectors.
- TextFrame / TextFrame2.
- VBA hoặc công cụ tự động hóa Excel có hỗ trợ Shapes.

Không sử dụng Sunburst, Treemap hoặc ảnh tĩnh để thay thế.

### 8.2. CẤU TRÚC DIAGRAM

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

Mỗi node con phải được nối chính xác với node cha dựa trên Parent ID.

### 8.3. NỘI DUNG MỖI NODE

Mỗi node hiển thị:

Node Name

Count: XXX

% Parent: XX.XX%

% Total: XX.XX%

Node TOTAL hiển thị Count và 100% Total.

### 8.4. HIỂN THỊ ĐẦY ĐỦ TẤT CẢ NHÁNH

Phải vẽ:

- Mọi GT Detail thực tế.
- Mọi Group Cause trong từng GT Detail.
- Mọi False Entity trong từng Group Cause.
- Mọi Detail False Entity trong từng False Entity.
- Mọi Root Cause trong từng nhánh.
- Mọi Solution thực tế.

Không giới hạn Top 5 hoặc Top 10.

Không bỏ nhánh có Count nhỏ.

Không gộp các node cùng tên thuộc các Parent ID khác nhau.

Không tạo node cho tổ hợp không tồn tại.

### 8.5. THIẾT KẾ

Tôi muốn diagram **cơ bản, dễ đọc, không màu mè**.

Yêu cầu:

- Nền trắng.
- Chữ đen hoặc xám đậm.
- Hình chữ nhật đơn giản.
- Viền mảnh.
- Đường nối rõ ràng.
- Không dùng icon trang trí.
- Không tạo 3D.
- Không sử dụng hiệu ứng không cần thiết.
- Không để node chồng lên nhau.
- Không để chữ bị cắt.
- Không để các đường nối gây nhầm lẫn.

Ưu tiên layout từ trái sang phải.

Cấu trúc:

Level 0 nằm bên trái.

Level 1 nằm ở cột tiếp theo.

Tiếp tục đến Level 6.

Các node con phải được bố trí gần node cha và cùng một cụm nhánh.

### 8.6. AUTOMATIC TREE LAYOUT

Không sử dụng tọa độ cố định cho toàn bộ node.

Bố trí dựa trên số lượng node và kích thước cây.

Quy trình đề xuất:

1. Đọc Node ID và Parent ID từ bảng thống kê.
2. Xây dựng cấu trúc cây trong bộ nhớ.
3. Tính kích thước cần thiết của từng cây con.
4. Xác định tọa độ cho tất cả node.
5. Tạo Shapes.
6. Tạo Connectors.
7. Nối đúng cha–con.
8. Kiểm tra chồng lấn.
9. Đối chiếu tổng số node và đường nối.

Nếu diagram rất lớn, cho phép mở rộng theo chiều ngang và chiều dọc worksheet.

Không tự động cắt bớt nhánh để vừa màn hình.

### 8.7. ĐỒNG BỘ SỐ LIỆU

Diagram phải được xây dựng trực tiếp từ Full Hierarchical Statistics Table.

Không nhập tay Count hoặc Percentage.

Khi số liệu thay đổi:

- Tính lại bảng.
- Xây dựng lại danh sách node.
- Cập nhật diagram.
- Không tạo trùng Shapes của lần chạy trước.
- Không xóa Shapes không thuộc diagram này.

Nếu bảng được Refresh nhưng diagram chưa được vẽ lại, phải ghi rõ trạng thái chưa cập nhật.

---

## 9. AREA D – DATA VALIDATION

Tạo bảng kiểm tra:

| Validation | Expected | Actual | Difference | Status |
|---|---:|---:|---:|---|

### CHECK 1 – TOTAL RECORDS

Tổng Count Level 1 bằng Total Valid Records.

### CHECK 2 – GROUP CAUSE

Tổng Count của các Group Cause thuộc mỗi GT Detail bằng Count của GT Detail đó.

### CHECK 3 – FALSE ENTITY

Tổng Count các False Entity thuộc mỗi Group Cause bằng Count của Group Cause đó.

### CHECK 4 – DETAIL FALSE ENTITY

Tổng Count các Detail False Entity thuộc mỗi False Entity bằng Count của False Entity đó.

### CHECK 5 – ROOT CAUSE

Tổng Count các Root Cause thuộc mỗi Detail False Entity bằng Count của node cha.

### CHECK 6 – SOLUTION

Nếu tồn tại cột Solution, tổng Count các Solution thuộc mỗi Root Cause phải bằng Count của node cha.

### CHECK 7 – NODE RELATIONSHIP

Kiểm tra:

- Mọi node trừ TOTAL đều có Parent ID hợp lệ.
- Node ID không trùng lặp.
- Không có node mồ côi.
- Không có vòng lặp phân cấp.
- Level của node con lớn hơn Level của node cha đúng một cấp.

### CHECK 8 – DIAGRAM COMPLETENESS

Kiểm tra:

- Tổng số Shapes đại diện cho node bằng số node trong bảng.
- Tổng số Connectors bằng tổng số node trừ một.
- Mỗi Connector nối đúng Parent ID.
- Không bỏ sót nhánh.

Nếu không thể vẽ đầy đủ, ghi trạng thái FAIL và nêu số node hoặc Connector còn thiếu.

### CHECK 9 – DATA QUALITY

Kiểm tra:

- Blank / Null.
- Giá trị mới chưa có trong mapping tham khảo.
- Giá trị sai chính tả nghi ngờ.
- Khoảng trắng đầu/cuối.
- Các tổ hợp khác mapping đã biết.
- Missing Root Cause.
- Missing Solution.
- Các ô chứa nhiều giá trị phân loại.

Giữ nguyên dữ liệu gốc và chỉ báo cáo vấn đề.

**Không tự xóa dữ liệu có vấn đề.**

Nếu Expected = Actual thì Status = PASS.

Nếu không bằng nhau thì Status = FAIL.

---

## 10. FILTER VÀ REFRESH

Bảng thống kê phải cho phép filter theo tất cả các cấp.

Ví dụ:

GT Detail = S2T

Group Cause = Number And Entity Error

False Entity = Amount

Detail False Entity = Value

Root Cause = Prompt Not Detail Enough

Khi filter, bảng cần hiển thị đúng các node thỏa điều kiện.

**Lưu ý:** Không được tự thay đổi Count hoặc % of Parent chỉ vì người dùng filter bảng, trừ khi có chức năng tính lại theo phạm vi lọc được thiết kế riêng.

Tree Diagram mặc định phải thể hiện toàn bộ dữ liệu có Label = "good".

Nếu môi trường hỗ trợ, có thể bổ sung cơ chế vẽ lại một nhánh cụ thể dựa trên lựa chọn filter.

Quy trình Refresh:

1. Đọc lại `DB Records`.
2. Lọc `Label = "good"`.
3. Phát hiện toàn bộ giá trị DISTINCT.
4. Tính lại các cấp hierarchy.
5. Tạo lại Node ID và Parent ID.
6. Cập nhật bảng thống kê.
7. Vẽ lại Tree Diagram.
8. Chạy lại Data Validation.

Không được tuyên bố diagram đã được cập nhật nếu Shapes chưa được làm mới.

---

## 11. BỐ CỤC TRONG MỘT SHEET

Tất cả kết quả phải nằm trong:

**`Hierarchical_Statistics`**

Bố trí:

**AREA A – Overall Summary**

Ở phần trên cùng của sheet.

**AREA B – Full Hierarchical Statistics Table**

Ở bên dưới Overall Summary.

**AREA C – Tree Diagram**

Ở vùng riêng bên phải bảng thống kê, bắt đầu từ các cột đủ xa để không chồng lên dữ liệu.

**AREA D – Data Validation**

Trong một khu vực độc lập, không bị Shapes che khuất.

Phải tính toán kích thước các khu vực trước khi đặt dữ liệu và diagram.

Không cho các khu vực chồng lên nhau khi số lượng dòng tăng.

### ĐỊNH DẠNG

- Excel Table có AutoFilter.
- Freeze Header.
- Count dạng số nguyên.
- Percentage 2 chữ số thập phân.
- Column Width dễ đọc.
- Node Name không bị cắt.
- Không dùng quá nhiều màu sắc.
- Không tạo chart phụ.
- Không tạo thêm sheet.

---

## 12. YÊU CẦU VỀ AUTOMATION VÀ GIỚI HẠN KỸ THUẬT

Ưu tiên Excel Automation có thể tạo trực tiếp Shapes và Connectors.

Nếu sử dụng VBA:

- Có thể dùng Shapes.AddShape.
- Có thể dùng Shapes.AddConnector.
- Có thể dùng TextFrame / TextFrame2.
- Phải có logic tạo lại diagram khi dữ liệu được cập nhật.

Nếu workbook đang là `.xlsx`, không tự ý chuyển sang `.xlsm` hoặc tạo file mới.

Không tự ý bật macro hoặc thay đổi thiết lập bảo mật.

Nếu môi trường hiện tại không hỗ trợ chạy VBA hoặc tạo Shapes tự động:

1. Vẫn hoàn thành toàn bộ bảng thống kê.
2. Tạo sơ đồ cây dạng văn bản trong khu vực diagram nếu có thể.
3. Ghi rõ Tree Diagram bằng Shapes chưa thực hiện được.
4. Nêu chính xác tính năng hoặc quyền truy cập còn thiếu.
5. Không tuyên bố đã hoàn thành Tree Diagram bằng Shapes nếu thực tế chưa tạo được.

Nếu số node vượt giới hạn thực tế của Excel, phải nêu số node có thể vẽ, số node chưa thể vẽ và lý do.

Không âm thầm bỏ bớt nhánh.

---

## 13. KIỂM TRA KẾT QUẢ CUỐI CÙNG

Sau khi hoàn thành, phải kiểm tra:

- Sheet nguồn chính xác là `DB Records`.
- Điều kiện lọc chính xác là `Label = "good"`.
- Không thay đổi dữ liệu nguồn.
- Chỉ tạo một sheet kết quả.
- Các giá trị DISTINCT được thống kê đầy đủ.
- Không giới hạn Top N.
- Các Count đúng.
- Các Percentage đúng.
- Node ID duy nhất.
- Parent ID chính xác.
- Mỗi node có đầy đủ thông tin cấp cha.
- Tree Diagram có đủ node.
- Connectors chính xác.
- Diagram khớp với bảng thống kê.
- Data Validation đã chạy.
- Không có dữ liệu mô phỏng trong kết quả.

Nếu có lỗi, báo cáo rõ các kiểm tra FAIL.

---

## 14. KẾT QUẢ TÔI MONG MUỐN

Tôi muốn nhận được **một sheet Excel duy nhất** tên `Hierarchical_Statistics`, nằm ngay trong workbook hiện tại.

Sheet này phải có:

**1. OVERALL SUMMARY**

Tổng số record và phân bổ tổng quan.

**2. FULL HIERARCHICAL STATISTICS TABLE**

Toàn bộ các cấp từ Total đến Solution, có Count, Parent Count, Percentage, Rank và quan hệ cha–con.

**3. COMPLETE TREE DIAGRAM**

Sơ đồ cây đầy đủ các nhánh thực tế, từ tổng quan rộng nhất đến nguyên nhân và giải pháp chi tiết nhất.

**4. DATA VALIDATION**

Đối chiếu số liệu để đảm bảo không bị thiếu, sai hoặc đếm trùng.

### ƯU TIÊN THEO THỨ TỰ

1. Data Accuracy.
2. Data Completeness.
3. Correct Hierarchy.
4. Correct Parent-Child Relationships.
5. Complete Tree Diagram.
6. Data Validation.
7. Readability.
8. Professional Formatting.

**YÊU CẦU CUỐI CÙNG:**

Hãy thực sự đọc dữ liệu từ sheet `DB Records`, lọc `Label = "good"`, tính toàn bộ số liệu, tạo duy nhất một sheet mới `Hierarchical_Statistics` và tự động vẽ đầy đủ Tree Diagram bằng Excel Shapes và Connectors nếu môi trường hỗ trợ.

Không tạo workbook mới.

Không thay đổi sheet nguồn.

Không tự tạo số liệu.

Không giới hạn các giá trị thực tế.

Không bỏ sót các nhánh.

Không chỉ đưa ra hướng dẫn thực hiện.

**HÃY THỰC HIỆN TOÀN BỘ CÁC YÊU CẦU TRONG WORKBOOK HIỆN TẠI.**
