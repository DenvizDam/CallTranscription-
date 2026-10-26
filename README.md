# FULL PROMPT – REDESIGN ERROR TREE DIAGRAM ON A SEPARATE EXCEL SHEET

## 1. MỤC TIÊU

Hãy đóng vai chuyên gia Data Analyst, Business Analyst và Excel Automation Developer.

Tôi muốn thiết kế lại Hierarchical Error Tree Diagram cho báo cáo phân tích lỗi Speech-to-Text (S2T) và Named Entity Recognition (NER).

**Yêu cầu quan trọng:**

- Vẽ Tree Diagram trên một sheet riêng.
- Không vẽ diagram chung với bảng thống kê.
- Tự động điều chỉnh kích thước sơ đồ phù hợp với trang Excel.
- Tô màu theo Percentage.
- Không hiển thị Blank/Null node.
- Không làm sai lệch Count và Percentage khi ẩn Blank.
- Thiết kế chuyên nghiệp, đơn giản, phù hợp trình bày với Management.

---

## 2. WORKBOOK STRUCTURE

Sử dụng workbook Excel hiện tại.

### Sheet 1 – DB Records

Đây là sheet chứa dữ liệu nguồn.

Chỉ sử dụng các dòng thỏa điều kiện:

`Label = "good"`

Phải so khớp chính xác cả chữ hoa/thường và khoảng trắng.

Không chỉnh sửa sheet này.

### Sheet 2 – Hierarchical_Statistics

Đây là sheet chứa bảng thống kê phân cấp đã được tạo trước đó.

Sử dụng các thông tin:

- Node ID
- Parent ID
- Level
- Node Name
- Count
- Parent Count
- % of Parent
- % of Total
- Hierarchy Path

Nếu các số liệu chưa chính xác, hãy đối chiếu và tính lại dựa trên `DB Records`.

### Sheet 3 – Error_Tree_Diagram

**Tạo một sheet mới có tên `Error_Tree_Diagram`.**

Toàn bộ sơ đồ cây phải nằm trên sheet này.

Không đưa bảng thống kê chi tiết vào sheet diagram.

Không tạo workbook mới.

Không chỉnh sửa hay xóa các sheet nguồn.

Nếu `Error_Tree_Diagram` đã tồn tại, chỉ cập nhật khu vực diagram của sheet này, không xóa dữ liệu không liên quan.

---

## 3. HIERARCHY

Vẽ sơ đồ theo thứ tự:

Level 0: TOTAL RECORDS

Level 1: GT Detail

Level 2: Group Cause

Level 3: False Entity

Level 4: Detail False Entity

Level 5: Root Cause

Level 6: Solution

Các node phải dựa trên giá trị thực tế.

Không tạo nhánh giả và không gộp các giá trị có cùng tên nhưng thuộc Parent ID khác nhau.

Nếu không có cột Solution, dừng tại Root Cause.

---

## 4. BLANK HANDLING

**Không hiển thị Blank, Null hoặc Empty node trên Tree Diagram.**

Nhưng các record này vẫn phải được tính trong tổng dữ liệu.

Ví dụ:

Recognition Error = 100 records

- Name = 50
- Amount = 30
- Address = 10
- Blank = 10

Diagram chỉ vẽ ba node Name, Amount và Address.

Recognition Error vẫn có Count = 100.

Thêm ghi chú nhỏ:

`Chưa phân loại tiếp: 10`

Không thay đổi mẫu số khi tính Percentage.

Nếu một Level bị Blank nhưng những Level sau có giá trị, không được tự nối tắt qua Level Blank để tạo quan hệ phân cấp giả.

Các record này vẫn được tính vào node cha gần nhất còn hợp lệ.

---

## 5. COUNT & PERCENTAGE

Mỗi node cần hiển thị:

**Node Name**

Count: XXX

Parent: XX.XX%

Total: XX.XX%

Công thức:

`% of Parent = Node Count / Direct Parent Count × 100`

`% of Total = Node Count / Total Valid Records × 100`

Trong đó Total Valid Records là toàn bộ record có Label chính xác bằng `"good"`.

Không tính lại Percentage dựa trên các node còn hiển thị sau khi ẩn Blank.

---

## 6. COLOR RULES

Tô màu dựa trên **% of Parent**.

| Percentage | Màu sắc |
|---|---|
| ≥ 60% | Đỏ |
| ≥ 30% và < 60% | Cam |
| ≥ 10% và < 30% | Vàng |
| < 10% | Xanh dương nhạt |

Riêng TOTAL RECORDS sử dụng màu xanh navy đậm.

Yêu cầu:

- Màu nền nhẹ, dễ đọc.
- Chữ có độ tương phản tốt.
- Không sử dụng gradient quá mạnh.
- Có Color Legend ở phía dưới diagram.
- Quy tắc màu nhất quán ở mọi Level.

Màu phản ánh tỷ trọng lỗi trong nhóm cha, không mặc định là mức độ nghiêm trọng của lỗi.

---

## 7. PAGE SIZE & LAYOUT – YÊU CẦU QUAN TRỌNG NHẤT

**Diagram phải được thiết kế phù hợp với kích thước trang Excel.**

### 7.1. PAGE SETUP

Thiết lập mặc định:

- Paper Size: A3.
- Orientation: Landscape.
- Margins: Narrow.
- Horizontal Alignment: Center.
- Print Area: Chỉ bao gồm vùng diagram, tiêu đề, legend và chú thích.
- Không in các vùng trống không cần thiết.
- Ẩn Gridlines khi xem và khi in.

### 7.2. FIT TO PAGE

Tính kích thước diagram dựa trên:

- Số lượng Level.
- Số node ở mỗi Level.
- Chiều rộng nội dung.
- Chiều cao các nhánh.
- Kích thước trang in.

Tự động điều chỉnh:

- Node Width.
- Node Height.
- Horizontal Spacing.
- Vertical Spacing.
- Font Size.
- Connector Position.

Diagram phải nằm gọn trong vùng trình bày được xác định.

Không để bất kỳ node nào vượt ngoài Print Area.

### 7.3. KHÔNG THU NHỎ QUÁ MỨC

Không ép toàn bộ diagram rất lớn vào một trang nếu làm chữ quá nhỏ hoặc không đọc được.

Ưu tiên tối thiểu:

- Node Name: 10–11 pt.
- Count: 11–12 pt.
- Percentage: 9–10 pt.
- Diagram Title: 18–22 pt.

Nếu không thể vừa một trang A3 với cỡ chữ dễ đọc, hãy tự động chia diagram thành nhiều vùng/trang hợp lý.

Không giảm font xuống quá nhỏ chỉ để đạt một trang.

### 7.4. NGUYÊN TẮC PHÂN TRANG

**Trang đầu tiên – Executive Overview**

Hiển thị:

TOTAL RECORDS → GT Detail → Group Cause

Đây là sơ đồ tổng quan, phải vừa một trang A3 Landscape.

**Các trang tiếp theo – Detailed Error Trees**

Thể hiện các nhánh chi tiết từ:

GT Detail → Group Cause → False Entity → Detail False Entity → Root Cause → Solution

Ưu tiên phân chia theo GT Detail hoặc Group Cause, tùy số lượng node.

Mỗi phần phải giữ đúng đường dẫn phân cấp.

Không chia một nhánh theo cách khiến người đọc không xác định được node cha.

Nếu một nhánh lớn cần nhiều trang, phải lặp lại các node tổ tiên cần thiết để giải thích ngữ cảnh, nhưng không tính lặp vào dữ liệu thống kê.

Không giới hạn Top N hoặc bỏ sót node hợp lệ chỉ để vừa trang.

### 7.5. PAGE BREAKS

Sử dụng Page Breaks hợp lý.

Khi Print Preview:

- Không cắt ngang node.
- Không cắt chữ.
- Không làm mất Connectors.
- Không để một trang gần như trống.
- Không để Legend bị tách khỏi diagram tương ứng.

---

## 8. NODE & CONNECTOR DESIGN

Vẽ bằng Excel Shapes và Connectors.

### NODE

- Rounded Rectangle.
- Width đồng nhất trong cùng Level nếu có thể.
- Height tự động theo nội dung.
- Tên node nổi bật.
- Count và Percentage rõ ràng.
- Màu theo % of Parent.

### CONNECTOR

- Sử dụng đường nối vuông góc hoặc đường nối gấp khúc.
- Nối chính xác Parent ID → Node ID.
- Không nối vào Blank node.
- Không tạo đường nối sai nhánh.
- Hạn chế tối đa đường nối giao nhau.
- Các node con nên nằm gần node cha.

### SORTING

Sắp xếp các node con theo Count giảm dần trong cùng node cha.

Nhánh lớn nhất hiển thị trước.

---

## 9. SHEET PRESENTATION

Sheet `Error_Tree_Diagram` cần có bố cục:

**HEADER**

S2T & NER – Hierarchical Error Analysis

Subtitle:

Data Source: DB Records | Filter: Label = "good"

**MAIN CONTENT**

Executive Tree Diagram và các Detailed Tree Diagram được bố trí thành những vùng in liên tiếp trong cùng sheet.

**FOOTER**

- Percentage Color Legend.
- Total Valid Records.
- Hidden Blank Records, nếu có.
- Chú thích: Màu phản ánh % of Parent.
- Data Validation Status.

Không thêm bảng dữ liệu chi tiết làm rối diagram.

Không tạo chart khác.

---

## 10. DATA VALIDATION

Bắt buộc kiểm tra:

1. Total Count bằng tổng record có Label = "good".
2. Count của mỗi node khớp bảng Hierarchical Statistics.
3. % of Parent tính chính xác.
4. % of Total tính chính xác.
5. Node được tô đúng màu.
6. Không hiển thị Blank/Null node.
7. Hidden Blank Count được giữ trong số liệu.
8. Mọi Connector nối đúng Parent ID.
9. Không bỏ sót node không Blank đủ điều kiện.
10. Print Area chứa đầy đủ nội dung.
11. Không có node bị cắt khi in.
12. Không có chữ hoặc Connectors chồng lấn nghiêm trọng.
13. Các trang in có cỡ chữ dễ đọc.
14. Không có nhánh giả hoặc Count bị nhân đôi do lặp node tổ tiên giữa các trang.

Nếu một node cha có các record thiếu phân loại, cần đối chiếu:

`Parent Count = Visible Children Count + Hidden Blank Count`

Trong trường hợp diagram chia thành nhiều trang, phải tính đủ mọi node con thực tế thuộc node cha, không chỉ các node nằm trên một trang.

---

## 11. AUTOMATIC REDRAW

Nếu diagram cũ đã tồn tại:

- Chỉ thay thế Shapes và Connectors thuộc diagram cũ.
- Không xóa dữ liệu nguồn.
- Không phá vỡ bảng thống kê.
- Tính lại layout.
- Cập nhật màu sắc.
- Thiết lập lại Print Area và Page Breaks.
- Kiểm tra lại Print Preview.

Nếu môi trường không hỗ trợ tạo Excel Shapes và Connectors, phải báo cáo rõ giới hạn kỹ thuật, không được tuyên bố đã tạo thành công.

---

## 12. FINAL EXPECTED RESULT

Workbook phải có các sheet:

`DB Records` – Dữ liệu nguồn.

`Hierarchical_Statistics` – Bảng thống kê đầy đủ.

`Error_Tree_Diagram` – Sơ đồ cây trình bày cho Management.

**Sheet `Error_Tree_Diagram` phải đạt các yêu cầu:**

- Executive Overview vừa một trang A3 Landscape.
- Detailed Tree được phân trang hợp lý.
- Count và Percentage chính xác.
- Màu sắc theo % of Parent.
- Không có Blank node.
- Không làm mất số liệu khi ẩn Blank.
- Mỗi nhánh được nối đúng.
- Không có node bị chồng hoặc bị cắt.
- Có Legend và chú thích.
- Có thể xem trực tiếp trong Excel hoặc in ra để trình bày.

**HÃY THỰC SỰ TẠO HOẶC VẼ LẠI TREE DIAGRAM TRÊN SHEET `Error_Tree_Diagram`, TỰ ĐỘNG CĂN CHỈNH KÍCH THƯỚC VÀ THIẾT LẬP TRANG IN PHÙ HỢP.**
