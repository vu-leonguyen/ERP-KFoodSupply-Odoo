# ĐỒ ÁN MÔN HỌC: HOẠCH ĐỊNH NGUỒN LỰC DOANH NGHIỆP (ERP)
## TRIỂN KHAI HỆ THỐNG ERP ODOO 19 CHO DOANH NGHIỆP CUNG ỨNG NGUYÊN LIỆU HÀN VIỆT (K-FOOD SUPPLY CO.)

---

## 📌 1. THÔNG TIN CHUNG
* **Tên đề tài:** Hoạch định và triển khai hệ thống ERP Odoo cho Doanh nghiệp Cung ứng Nguyên liệu Hàn Việt (**K-Food Supply Co.**)
* **Nền tảng công nghệ:** Odoo Community / Enterprise version 19.0
* **Giảng viên hướng dẫn:** ThS. Văn Đức Sơn Hà
* **Đơn vị đào tạo:** Trường Đại học Công nghệ Thông tin – ĐHQG-HCM (UIT)
* **Nhóm thực hiện:** Nhóm 7
  * **Nguyễn Ngọc Lợi** - MSSV: `23520871` (Bộ phận Mua & Bán hàng)
  * **Đặng Hữu Thọ** - MSSV: `23521517` (Bộ phận Quản lý Vốn & Nhân lực)
  * **Nguyễn Trường Vũ** - MSSV: `23521812` (Bộ phận Kho)

---

## 🏢 2. BỐI CẢNH DOANH NGHIỆP & PHẠM VI DỰ ÁN

### 2.1. Giới thiệu Doanh nghiệp K-Food Supply Co.
**K-Food Supply Co.** là doanh nghiệp thương mại trung gian chuyên nhập khẩu các mặt hàng thực phẩm chính ngạch từ Hàn Quốc (như thịt bò, thịt heo, thịt gà, hải sản đông lạnh, kim chi, bánh gạo, tương ớt, các loại gia vị & sốt đặc trưng...) và phân phối theo mô hình B2B cho chuỗi các nhà hàng Hàn Quốc, quán lẩu, nướng (BBQ, lẩu Hàn, tokbokki, cơm trộn, gà rán phong cách Hàn,...) tại khu vực TP.HCM và các tỉnh lân cận. Doanh nghiệp vận hành hệ thống kho lạnh và kho khô tại khu phố 6, TP. Thủ Đức để duy trì chất lượng hàng hóa theo chuỗi lạnh nghiêm ngặt.

### 2.2. Dữ liệu chủ của hệ thống (Master Data)
Master Data được xây dựng và chuẩn hóa đồng bộ để hệ thống ERP vận hành trơn tru:
* **Danh mục sản phẩm:** Gồm 8 nhóm chính (Thịt heo, thịt bò, thịt gà, hải sản, sốt Hàn, kim chi, phụ liệu Hàn Quốc, bao bì thực phẩm) với **620 sản phẩm** có thiết lập quản lý theo Số Lô (Lot/Serial) và Hạn sử dụng (Expiry Date).
* **Danh mục đối tác:** **215 khách hàng** (nhà hàng, chuỗi F&B) và **42 nhà cung cấp** (đơn vị nhập khẩu từ Hàn Quốc & nội địa).
* **Cơ cấu người dùng (Users):** **7 người dùng** phân quyền chi tiết tương ứng với các vai trò (Kho, Bán hàng, Mua hàng, Kế toán, Quản lý doanh nghiệp).
* **Hệ thống kho bãi:** Gồm 2 kho chính là **Kho lạnh** (lưu trữ thịt, hải sản, kim chi) và **Kho khô** (lưu trữ sốt, phụ liệu, bao bì) chia thành **36 vị trí chi tiết** (ngăn đông, kệ lạnh, khu phân loại,...).

### 2.3. Các phân hệ tiêu chuẩn đã triển khai
1. **Quản lý Bán hàng (Sales):** Quản lý báo giá, đơn hàng B2B định kỳ, chính sách giá bán lẻ/chiết khấu, điều khoản trả trước/trả sau và công nợ khách hàng.
2. **Quản lý Mua hàng (Purchase):** Gửi yêu cầu báo giá (RFQ), đánh giá nhà cung cấp, lập đơn mua hàng (PO), tính toán chi phí nhập khẩu (landed costs).
3. **Quản lý Kho vận (Inventory):** Xử lý quy trình nhập kho 2 bước (Input -> Kiểm tra chất lượng QC -> Stock), xuất kho (Picking -> Packing -> Delivery Validate), và theo dõi Lot/Expiry Date để giảm thiểu thất thoát chuỗi lạnh.
4. **Quản lý Nhân sự (HRM - Time Off):** 
   * *Nghỉ phép có lương (Paid Time Off):* Luồng phê duyệt 1 cấp bởi Line Manager, hệ thống tự động kiểm tra số dư phép và trừ ngày nghỉ trực tiếp.
   * *Nghỉ ốm (Sick Time Off):* Luồng phê duyệt 2 cấp bảo mật (Line Manager duyệt sơ bộ -> Time Off Approver phê duyệt chính thức) kèm yêu cầu đính kèm chứng từ y tế.
5. **Kế toán & Công nợ (Invoicing & Accounting):** Tạo hóa đơn khách hàng (Customer Invoice), hóa đơn nhà cung cấp (Vendor Bill), đối chiếu thanh toán 3 chiều (PO - Phiếu kho - Hóa đơn) và theo dõi công nợ trễ hạn.
6. **Tự động hóa & Tích hợp:** Cấu hình Automation Rules (ví dụ thông báo tồn kho/đơn hàng) và tích hợp Webhook/API phục vụ đồng bộ hệ thống.

---

## 🚀 3. PHÂN HỆ TÙY BIẾN MỚI: HÀN VIỆT FINANCE (`kfood_finance`)

### 3.1. Bài toán thực tế & Mục tiêu
Với đặc thù nhập khẩu khối lượng lớn nguyên liệu từ Hàn Quốc, biến động tỷ giá hối đoái giữa đồng Won Hàn Quốc (**KRW**) và Việt Nam Đồng (**VND**) ảnh hưởng rất lớn đến giá vốn hàng bán và biên lợi nhuận của K-Food Supply Co. 

Phân hệ **Hàn Việt Finance** được nhóm tự phát triển trên Odoo 19 nhằm:
* **Tự động hóa:** Tự động gọi API trực tuyến lấy dữ liệu tỷ giá theo thời gian thực (Live) hoặc lịch sử (Historical).
* **Tính toán quy đổi chéo:** Xử lý chênh lệch thông qua đồng tiền trung gian USD.
* **Hỗ trợ ra quyết định:** Áp dụng các chỉ báo tài chính chuyên sâu để phân tích xu hướng biến động và tự động đề xuất khuyến nghị phòng Mua hàng nên chốt mua đơn hàng nhập khẩu hay tiếp tục giữ trạng thái chờ nhằm tối ưu hóa chi phí.

### 3.2. Quy trình Hoạt động của Phân hệ
```text
[Tạo bản ghi (New)] ──> [Nhập tay (Manual) HOẶC Gọi API (Fetch)] ──> [Tính toán chỉ số MA7/MA30 & Độ mạnh xu hướng] ──> [Hệ thống đưa khuyến nghị] ──> [Duyệt (Approve) / Hủy] ──> [Lưu trữ CSDL & Vẽ biểu đồ]
```
1. **Khởi tạo bản ghi tỷ giá:** 
   * *Manual Input (Nhập thủ công):* Người dùng tự điền tỷ giá ngoại tệ phục vụ mục đích kiểm thử hoặc giả lập kịch bản tài chính.
   * *Fetch API (Lấy tự động):* Chọn một ngày bất kỳ trên lịch, hệ thống tự động kết nối API bên ngoài để tải về tỷ giá thực tế của ngày đó.
2. **Phân tích tài chính & Khuyến nghị tự động:**
   * Sau khi nhận tỷ giá, hệ thống so khớp với dữ liệu lịch sử để tính toán các chỉ số kỹ thuật: Trung bình trượt 7 ngày ($MA_7$), 30 ngày ($MA_{30}$), chỉ số sức mạnh xu hướng (Trend Strength), và độ ổn định xu hướng (Stability Index).
   * Đưa ra khuyến nghị tự động như `Hold` (Giữ nguyên trạng thái) kèm giải thích chi tiết (Ví dụ: `"Signal detected"` cảnh báo tín hiệu thị trường đang bị nhiễu do biến động bất thường).
3. **Phê duyệt & Lưu vết hệ thống:**
   * Người quản trị kiểm tra thông tin phân tích và nhấn **Approve** để lưu chính thức bản ghi vào cơ sở dữ liệu làm căn cứ kiểm soát giá vốn khi tạo đơn mua hàng (PO).

### 3.3. Tích hợp API & Thuật toán Quy đổi Chéo
* **Nguồn API:** Sử dụng API từ nhà cung cấp dịch vụ *Exchange Host*, hỗ trợ lấy dữ liệu Live và Historical.
* **Thuật toán quy đổi gián tiếp KRW/VND:** 
  Vì API của dịch vụ trả về tỷ giá của các đồng ngoại tệ quy đổi theo đồng tiền chuẩn USD, hệ thống thực hiện thuật toán tính toán chéo như sau:
  $$\text{Tỷ giá KRW/VND} = \frac{\text{Tỷ giá USD/VND}}{\text{Tỷ giá USD/KRW}}$$
* **Bảo mật API Key qua Tham số Hệ thống:**
  Để tránh lộ khóa bảo mật (API Key) trong mã nguồn, hệ thống lưu trữ thông tin này dưới dạng biến cấu hình Odoo:
  * Đường dẫn thiết lập: `Settings` $\rightarrow$ `Technical` $\rightarrow$ `Parameters` $\rightarrow$ `System Parameters`.
  * Khởi tạo bản ghi có Key là `hang_viet_exchange_api_key` và gán giá trị API Key được cấp. Module sẽ tự động gọi tham số này khi chạy hàm Fetch.

### 3.4. Trực quan hóa Biểu đồ (Visualizations)
Module tích hợp sâu vào Graph View & Pivot View mặc định của Odoo 19:
* **Chỉ số đo lường hiển thị:** Biến động tỷ giá, $MA_7$, $MA_{30}$, Trend Strength, Stability Index.
* **Tích hợp dữ liệu:** Bộ dữ liệu lịch sử phong phú được nạp sẵn từ tháng 01/2024 đến tháng 12/2025.
* **Chế độ hiển thị:** Cho phép xem dưới dạng biểu đồ đường (Line chart), biểu đồ tròn (Pie chart), hoặc biểu đồ cột (Bar chart), hỗ trợ bộ lọc sắp xếp tăng/giảm linh hoạt để phục vụ báo cáo quản trị.

---

## 💻 4. HƯỚNG DẪN CÀI ĐẶT MODULE TRÊN ODOO 19 (LOCAL)

Thực hiện cài đặt module **Hàn Việt Finance** trên môi trường Local theo chuẩn hướng dẫn của Odoo Developer Documentation:

### Bước 1: Sao chép module và cấu hình `addons_path`
1. Di chuyển hoặc sao chép thư mục module `kfood_finance` vào trong thư mục `custom_addons` của đồ án.
2. Mở file cấu hình Odoo (`odoo.conf` hoặc `odoo-server.conf`), tìm dòng `addons_path` và bổ sung thêm đường dẫn đến thư mục `custom_addons` (phân tách với các đường dẫn cũ bằng dấu phẩy `,`):
   ```ini
   [options]
   addons_path = /path/to/odoo/addons,/path/to/ERP-KFoodSupply-Odoo/custom_addons
   ```
   *(Trường hợp khởi động Odoo trực tiếp từ dòng lệnh Terminal, sử dụng tham số `--addons-path`:)*
   ```bash
   python3 odoo-bin -c odoo.conf --addons-path=addons,custom_addons
   ```

### Bước 2: Khởi động lại Server Odoo
Bạn cần khởi động lại tiến trình chạy Odoo để hệ thống quét và nạp đường dẫn thư mục addons mới:
* **Nếu chạy trực tiếp từ Terminal:** Nhấn tổ hợp phím `Ctrl + C` để dừng và chạy lại lệnh khởi động.
* **Nếu chạy bằng Linux Systemd Service:**
  ```bash
  sudo systemctl restart odoo
  ```
* **Nếu chạy bằng Docker Compose:**
  ```bash
  docker-compose restart web
  ```

### Bước 3: Kích hoạt Developer Mode & Cập nhật danh sách ứng dụng
1. Truy cập giao diện Odoo Local bằng tài khoản quản trị viên (**Administrator**).
2. Vào phân hệ **Settings (Cài đặt)** $\rightarrow$ Cuộn xuống cuối trang chọn kích hoạt **Activate the developer mode (Kích hoạt chế độ nhà phát triển)**.
3. Di chuyển đến phân hệ **Apps (Ứng dụng)**.
4. Trên thanh menu ngang trên cùng, nhấn chọn menu con **Update Apps List (Cập nhật danh sách ứng dụng)** $\rightarrow$ Bấm nút **Update** để Odoo quét các module mới trong thư mục `custom_addons`.

### Bước 4: Cài đặt và cấu hình tham số hệ thống
1. Tại ô tìm kiếm của phân hệ **Apps**, **xóa bỏ bộ lọc mặc định "Apps"** để Odoo không lọc ẩn các module tùy biến.
2. Nhập từ khóa tìm kiếm: `kfood_finance` hoặc `Hàn Việt Finance`.
3. Nhấn nút **Activate (Kích hoạt)** hoặc **Install (Cài đặt)** và đợi hệ thống tự động thiết lập.
4. **Cấu hình API Key bảo mật:**
   * Truy cập: **Settings (Cài đặt)** $\rightarrow$ **Technical (Kỹ thuật)** $\rightarrow$ **Parameters (Tham số)** $\rightarrow$ **System Parameters (Tham số hệ thống)**.
   * Nhấn nút **New** để tạo mới tham số cấu hình:
     * **Key:** `hang_viet_exchange_api_key`
     * **Value:** `<Dán_API_Key_nhận_được_từ_Exchange_Host_vào_đây>`
   * Nhấn **Save (Lưu)** để hoàn tất.

---

## 📂 5. CẤU TRÚC KHO LƯU TRỮ (REPOSITORY STRUCTURE)

Sắp xếp cấu trúc thư mục của repository theo mô hình chuẩn của một dự án công nghệ thông tin (Code + Tài liệu + Dữ liệu mẫu):

```text
ERP-KFoodSupply-Odoo/
│
├── 📁 custom_addons/                          # Mã nguồn phân hệ tự phát triển (Mục 4.8)
│   └── 📁 kfood_finance/                      # Phân hệ Hàn Việt Finance (Odoo 19 Module)
│       ├── __init__.py
│       ├── __manifest__.py
│       ├── 📁 models/                         # Xử lý logic nghiệp vụ, gọi API & thuật toán
│       │   ├── __init__.py
│       │   └── exchange_rate_analysis.py
│       ├── 📁 views/                          # Giao diện hiển thị Form, Tree, Graph/Pivot
│       │   ├── exchange_rate_views.xml
│       │   └── menu_views.xml
│       ├── 📁 security/                       # File phân quyền truy cập người dùng
│       │   └── ir.model.access.csv
│       └── 📁 data/                           # Dữ liệu khởi tạo mặc định (Demo data)
│
├── 📁 docs/                                   # Toàn bộ tài liệu báo cáo của dự án
│   ├── Report_Nhom7_KFoodSupply.pdf           # Toàn văn báo cáo đồ án (Xuất từ file Word)
│   ├── A4-10_DeXuat_DichVu_DatHang_B2B.pdf    # Đề xuất dịch vụ đặt hàng định kỳ (Mục 4.10)
│   │
│   ├── 📁 01_quy_trinh_bpmn/                  # Sơ đồ và đặc tả quy trình nghiệp vụ (Mục 4.3 & 4.4)
│   │   ├── quy_trinh_ban_hang.png
│   │   ├── quy_trinh_mua_hang.png
│   │   ├── quy_trinh_nhap_kho.png
│   │   ├── quy_trinh_xuat_kho.png
│   │   └── quy_trinh_hcm_time_off.png
│   │
│   ├── 📁 02_api_va_webhook/                  # Nghiên cứu và gọi API, Webhook (Mục 4.6)
│   │   ├── Tim_Hieu_API_Nhom7.pdf
│   │   ├── Kham_Pha_Webhook_Nhom7.pdf
│   │   └── 📁 individual/                     # Báo cáo tìm hiểu cá nhân của từng thành viên
│   │       ├── API_23520871_NguyenNgocLoi.pdf
│   │       ├── API_23521517_DangHuuTho.pdf
│   │       └── API_23521812_NguyenTruongVu.pdf
│   │
│   └── 📁 03_automation_rules/                # Hướng dẫn thiết lập Automation Rules (Mục 4.7)
│       └── Automation_Rules_Nhom7.pdf
│
├── 📁 data/                                   # Các file Master Data phục vụ Import (Mục 4.5)
│   ├── 01_master_data_products.xlsx           # Danh mục 620 sản phẩm quản lý lô/hạn
│   ├── 02_master_data_partners.xlsx           # Danh mục 215 khách hàng & 42 nhà cung cấp
│   └── 03_initial_inventory.xlsx              # Dữ liệu tồn kho đầu kỳ chi tiết theo lô
│
├── 📁 screenshots/                            # Ảnh minh chứng cấu hình thực tế trên Odoo (Mục 4.2.1)
│   ├── 01_thong_tin_nguoi_cai_dat.png
│   ├── 02_thong_tin_cong_ty.png
│   ├── 03_don_vi_tien_te.png
│   ├── 04_nguoi_dung_va_phan_quyen.png
│   ├── 05_cau_hinh_san_pham.png
│   └── 06_thay_doi_layout_hoa_don.png
│
├── .gitignore                                 # Loại bỏ file tạm Office, file rác OS và Python cache
└── README.md                                  # Hướng dẫn và mô tả tổng quan dự án (File này)
```
