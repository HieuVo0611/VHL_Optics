# VHL_Optics

## Giới thiệu

VHL_Optics là một dự án AI được thiết kế để phân tích dữ liệu quang học, bao gồm các mô hình xử lý hình ảnh để phát hiện và phân tích hợp chất hóa học như NO₂ và NH₃ từ các thiết bị di động khác nhau. Dự án cung cấp các công cụ cho việc xử lý dữ liệu, phân tích hình ảnh, trích xuất thông tin từ dữ liệu quang học và đánh giá các mô hình học máy.

## Tính năng chính

1. **Xử lý và phân tích dữ liệu quang học:**
   - Đọc dữ liệu hình ảnh từ các thiết bị di động.
   - Tiền xử lý dữ liệu và tách riêng thông tin quang học.
   - Trích xuất thông tin từ metadata của hình ảnh.
   
2. **Phân tích dữ liệu từ nhiều thương hiệu điện thoại:**
   - Hỗ trợ dữ liệu từ các hãng Nokia, Samsung và Xiaomi.
   - Chuẩn hóa và xử lý dữ liệu theo từng thương hiệu.
   - So sánh sự khác biệt về quang học giữa các thiết bị.

## Cấu trúc dự án

```
VHL_Optics-main/
├── src/
│   ├── Metadata.ipynb                # Phân tích và xử lý metadata
│   ├── Seperate.ipynb                 # Tách dữ liệu quang học
│   ├── nokia/                         # Phân tích dữ liệu từ điện thoại Nokia
│   │   ├── Nokia.ipynb
│   │   ├── middle/Optic_middle_NO2_nokia.ipynb
│   ├── samsung/                       # Phân tích dữ liệu từ điện thoại Samsung
│   │   ├── Samsung.ipynb
│   │   ├── middle/Optic_middle_NH3_samsung.ipynb
│   │   ├── middle/Optic_middle_NO2_samsung.ipynb
│   ├── xiaomi/                        # Phân tích dữ liệu từ điện thoại Xiaomi
│   │   ├── Xiaomi.ipynb
│   │   ├── middle/Optic_middle_NH3_xiaomi.ipynb
│   │   ├── middle/Optic_middle_NO2_xiaomi.ipynb
├── requirements.txt                   # Danh sách các thư viện cần thiết
├── README.md                           # Tài liệu dự án
├── LICENSE                             # Giấy phép sử dụng
```

## Cài đặt

1. **Clone dự án:**
   ```bash
   git clone <repository-url>
   cd VHL_Optics-main
   ```
2. **Cài đặt các thư viện:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Tạo thư mục data và bỏ dữ liệu gốc vào**
## Sử dụng
* Phân chia dữ liệu quang học: Chạy notebook `src/Seperate.ipynb` để tách dữ liệu quang học. Chạy nhiều lần tương ứng với mỗi chất.
* Phân tích metadata: Chạy notebook `src/Metadata.ipynb` để trích xuất thông tin từ metadata. Chạy nhiều lần tương ứng cho mỗi chất của mỗi loại điện thoại.
* Xử lý dữ liệu quang học: Chạy notebook `src/Nokia/Nokia.ipynb` để tách dữ liệu quang học ra ảnh viền và ảnh nhân. Tương ứng cho loại chất và điện thoại khác nhau.
* Huấn luyện mô hình: Chạy các notebook trong thư mục tương ứng với từng hãng (Nokia, Samsung, Xiaomi) để thực hiện phân tích chuyên sâu.

## Yêu cầu hệ thống

* Python 3.9 trở lên.
* Các thư viện Python được liệt kê trong `requirements.txt`.

## Giấy phép

* Dự án được cấp phép theo MIT License.

