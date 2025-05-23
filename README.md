# VHL_Optics

## Tổng quan

VHL_Optics là một dự án AI được thiết kế để phân tích dữ liệu quang học từ các hình ảnh thu thập được từ nhiều thiết bị di động khác nhau. Dự án cung cấp các công cụ để xử lý dữ liệu, phân tích hình ảnh, trích xuất đặc trưng và huấn luyện các mô hình học máy nhằm phân loại và dự đoán các thông số quang học.

## Tính năng chính

1. **Xử lý dữ liệu quang học**:
   - Tổ chức và xử lý dữ liệu hình ảnh từ các thiết bị di động (smartphones). 
   - Tự động phát hiện và tách vùng quan tâm (ROI) chứa phản ứng hóa học.
   - Áp dụng chuẩn hóa hình ảnh để giảm nhiễu và tăng tính nhất quán đầu vào.

2. **Trích xuất đặc trưng**:
   - Trích xuất các đặc trưng màu sắc và kết cấu từ vùng phản ứng để sử dụng trong mô hình.
   - Sử dụng các kỹ thuật như GLCM, entropy, và histogram màu.

3. **Huấn luyện mô hình**:
   - Huấn luyện các mô hình phân loại và hồi quy dựa trên các đặc trưng đã trích xuất.
   - Hỗ trợ các thuật toán phổ biến:
        + Random Forest
        + SVM
        + KNN
        + MLP (Neural Network)
        + XGBoost
        + Logistic Regression
        + Naive Bayes
   - Đánh giá mô hình với cross-validation (Stratified K-fold), thống kê độ chính xác, F1-score và độ lệch chuẩn.
   
4. **Pipeline tự động**:
   - Thực hiện toàn bộ quy trình từ xử lý dữ liệu, trích xuất đặc trưng đến huấn luyện mô hình chỉ với một lệnh duy nhất.

## Cấu trúc dự án
```
   VHL_Optics/
├── data/
│   ├── _uploadRGB_5phones_sorted/     # Dữ liệu gốc
│   ├── square image/                  # Ảnh xử lý chuẩn hóa
│   ├── csv/                           # Đặc trưng đầu vào cho mô hình
│   └── models/                        # File mô hình .pkl và kết quả đánh giá
│   └── ...
├── evaluation/                        # Biểu đồ và bảng đánh giá mô hình
│   ├── accuracy_per_model.png
│   ├── f1_macro_per_model.png
│   ├── average_accuracy_summary.csv
│   └── average_f1_macro_summary.csv
│   └── ...
├── src/                               # Mã nguồn chính
│   ├── config.py
│   ├── processing.py
│   ├── normalize.py
│   ├── model.py
│   ├── classifiers.py
│   ├── evaluate_models.py
│   └── predict.py
│   └── ....
├── requirements.txt
└── README.md
```
## Hướng dẫn cài đặt

1. **Clone dự án**:
   ```bash
   git clone <repository-url>
   cd VHL_Optics
   ```
2. **Cài đặt các thư viện cần thiết**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Chuẩn bị dữ liệu**:
   Tạo thư mục data và đặt dữ liệu hình ảnh gốc vào đó.

## Hướng dẫn sử dụng
1. Chạy toàn bộ pipeline
   Chạy toàn bộ quy trình xử lý dữ liệu, trích xuất đặc trưng và huấn luyện mô hình bằng lệnh sau:
   ```bash
   python src/main.py
   ```
2. Đánh giá mô hình và xuất biểu đồ
      ```bash
      python -m evaluation.evaluate_models
      ```

## Yêu cầu hệ thống
 - Python 3.9 hoặc cao hơn.
 - Các thư viện được liệt kê trong `requirements.txt`.

## Giấy phép
Dự án được cấp phép theo MIT License.
