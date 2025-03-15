# VHL_Optics

## Giới thiệu
VHL_Optics là một dự án liên quan đến xử lý hình ảnh quang học để phân tích các hợp chất hóa học như NO₂ và NH₃ từ các thiết bị di động khác nhau. Dự án bao gồm các tập tin Jupyter Notebook phục vụ cho việc phân tích dữ liệu từ các hãng điện thoại như Nokia, Samsung, và Xiaomi.

## Cài đặt
### Yêu cầu hệ thống
- Python 3.x
- Jupyter Notebook
- Các thư viện Python cần thiết (có trong `requirements.txt`)

### Cài đặt thư viện
Chạy lệnh sau để cài đặt các thư viện cần thiết:
```sh
pip install -r requirements.txt
```

## Cấu trúc thư mục
```
VHL_Optics-main/
│── requirements.txt       # Danh sách các thư viện cần thiết
│── src/                   # Thư mục chứa mã nguồn chính
│   ├── Metadata.ipynb     # Phân tích và xử lý metadata
│   ├── Seperate.ipynb     # Tách dữ liệu quang học
│   ├── nokia/             # Phân tích dữ liệu từ điện thoại Nokia
│   ├── samsung/           # Phân tích dữ liệu từ điện thoại Samsung
│   ├── xiaomi/            # Phân tích dữ liệu từ điện thoại Xiaomi
```

## Hướng dẫn sử dụng
1. Mở Jupyter Notebook:
   ```sh
   jupyter notebook
   ```
2. Điều hướng đến thư mục `src/` và mở các notebook phù hợp với nhu cầu phân tích của bạn.
3. Chạy từng cell theo thứ tự để thực hiện phân tích dữ liệu.

## Giấy phép
Dự án này được phát hành theo giấy phép MIT. Xem thêm trong tập tin `LICENSE`.

