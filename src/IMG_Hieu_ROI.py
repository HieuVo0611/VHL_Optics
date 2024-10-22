import cv2
import numpy as np
import os

# Đường dẫn đến thư mục chứa ảnh gốc
# input_folder = './ppmdataset/Image/'
# output_folder = './final1/'
input_folder = './folder/meatadataset/'
output_folder = './folder/roidata/'

# Kiểm tra nếu thư mục đầu ra không tồn tại, tạo mới
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Hàm tính khoảng cách Euclidean giữa hai màu RGB
def color_distance(c1, c2):
    return np.sqrt(np.sum((c1 - c2) ** 2))

# Hàm kiểm tra xem màu có phải gần màu đen hay không
def is_black(color, threshold=30):
    black = np.array([0, 0, 0])
    gray_greenish = np.array([64, 65, 58])
    a = np.array([108,  25,  35])
    b = np.array([183, 201, 186])
    c = np.array([176, 177, 132])
    
    # Kiểm tra nếu màu trung bình gần với màu đen hoặc màu xám đậm ánh xanh lá
    return (color_distance(color, black) < threshold or 
            color_distance(color, gray_greenish) < threshold or
            color_distance(color, a) < threshold or
            color_distance(color, b) < threshold or
            color_distance(color, c) < threshold)

# Duyệt qua tất cả các tệp trong thư mục đầu vào
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):  # Chỉ xử lý ảnh jpg hoặc png
        # Đọc ảnh
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        image = cv2.resize(image, (300, 400))
        height, width, _ = image.shape

        # Chuyển ảnh sang thang độ xám
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)

        adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY, 11, 2)

        # Tìm các đường viền
        contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Xác định tâm của ảnh
        center_x, center_y = width // 2, height // 2

        # Biến để lưu hình vuông gần trung tâm nhất
        closest_square = None
        min_distance = float('inf')

        # Duyệt qua tất cả các đường viền để tìm hình vuông
        for contour in contours:
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4:  # Kiểm tra nếu có 4 cạnh (ô vuông hoặc hình chữ nhật)
                x, y, w, h = cv2.boundingRect(approx)
                if 0.9 <= w / h <= 1.1:  # Điều kiện để coi là hình vuông
                    # Tính tâm của hình vuông
                    square_center_x = x + w // 2
                    square_center_y = y + h // 2

                    # Tính khoảng cách từ tâm của ô vuông đến tâm của ảnh
                    distance = np.sqrt((square_center_x - center_x) ** 2 + (square_center_y - center_y) ** 2)

                    # Nếu khoảng cách nhỏ hơn khoảng cách nhỏ nhất hiện tại, cập nhật
                    if distance < min_distance:
                        min_distance = distance
                        closest_square = (x, y, w, h)

        # Nếu tìm thấy ô vuông gần trung tâm nhất
        if closest_square is not None:
            x, y, w, h = closest_square
            # Cắt phần hình vuông để lấy màu sắc
            square_crop = image[y:y+h, x:x+w]

            # Lấy màu trung bình của hình vuông
            avg_color = np.mean(square_crop, axis=(0, 1)).astype(int)  # Màu RGB
            # Kiểm tra nếu màu trung bình gần màu đen
            if is_black(avg_color):
                # Nếu màu trung bình gần đen, áp dụng thuật toán phát hiện cạnh
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Làm mờ ảnh để giảm nhiễu
                edges = cv2.Canny(blurred, 50, 150)  # Phát hiện cạnh bằng Canny

                # Tìm các đường viền trong ảnh dựa trên các cạnh
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                max_area = 0
                largest_contour = None

                # Duyệt qua tất cả các đường viền tìm được
                for contour in contours:
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)

                    if len(approx) == 4:  # Nếu là tứ giác
                        area = cv2.contourArea(approx)
                        if area > max_area:
                            max_area = area
                            largest_contour = approx

                # Nếu tìm thấy tứ giác lớn nhất, cắt và resize
                if largest_contour is not None:
                    # Tính toán trung tâm của tứ giác
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:  # Kiểm tra tránh chia cho 0
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])

                        # Lấy màu tại điểm trung tâm
                        center_color = image[cY, cX].tolist()  # Lấy màu BGR

                        # Chuyển đổi màu trung tâm sang khoảng giá trị màu
                        lower_bound = np.array([max(center_color[0] - 20, 0), max(center_color[1] - 20, 0), max(center_color[2] - 20, 0)])
                        upper_bound = np.array([min(center_color[0] + 20, 255), min(center_color[1] + 20, 255), min(center_color[2] + 20, 255)])

                        # Tạo mặt nạ để tìm các pixel có màu gần giống với màu trung tâm
                        mask = cv2.inRange(image, lower_bound, upper_bound)

                        # Tìm các đường viền trong mặt nạ
                        masked_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                        # Tìm mảng màu có diện tích lớn nhất
                        max_mask_area = 0
                        largest_masked_contour = None

                        for masked_contour in masked_contours:
                            area = cv2.contourArea(masked_contour)
                            if area > max_mask_area:
                                max_mask_area = area
                                largest_masked_contour = masked_contour

                        # Nếu tìm thấy mảng màu lớn nhất, cắt nó ra và resize
                        if largest_masked_contour is not None:
                            x, y, w, h = cv2.boundingRect(largest_masked_contour)  # Lấy vùng giới hạn của mảng màu
                            cropped_image = image[y:y+h, x:x+w]  # Cắt ảnh
                            resized_image = cv2.resize(cropped_image, (256, 256))  # Resize về 256x256

                            # Lưu ảnh đã được cắt và resize
                            output_path = os.path.join(output_folder, filename)
                            cv2.imwrite(output_path, resized_image)
            else:
                # Nếu màu trung bình không phải màu đen, xử lý với màu tương tự
                threshold = 50  # Ngưỡng để xác định độ tương đồng màu
                mask = np.zeros((height, width), dtype=np.uint8)
                for i in range(height):
                    for j in range(width):
                        pixel_color = image[i, j]
                        if color_distance(pixel_color, avg_color) < threshold:
                            mask[i, j] = 255

                # Tìm các đường viền xung quanh các vùng có màu tương tự
                sample_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                closest_sample = None
                min_sample_distance = float('inf')
                for contour in sample_contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    sample_center_x = x + w // 2
                    sample_center_y = y + h // 2

                    sample_distance = np.sqrt((sample_center_x - center_x) ** 2 + (sample_center_y - center_y) ** 2)

                    if sample_distance < min_sample_distance:
                        min_sample_distance = sample_distance
                        closest_sample = (x, y, w, h)

                if closest_sample is not None:

                    x, y, w, h = closest_sample
                    sample_crop = image[y:y+h, x:x+w]
                    
                    # Xác định vùng trung tâm của closest sample
                    center_x, center_y = w // 2, h // 2
                    center_region_size = 100  # Kích thước vùng trung tâm để phân tích màu

                    # Tạo một vùng nhỏ ở trung tâm closest sample
                    center_crop = sample_crop[center_y - center_region_size//2:center_y + center_region_size//2,
                                            center_x - center_region_size//2:center_x + center_region_size//2]

                    # Tính toán màu trung bình của vùng trung tâm
                    avg_color = np.mean(center_crop, axis=(0, 1)).astype(int)

                    # Tạo mặt nạ dựa trên màu trung bình của vùng trung tâm
                    mask = np.zeros(sample_crop.shape[:2], dtype=np.uint8)
                    threshold = 40  # Ngưỡng xác định độ tương đồng của màu
                    for i in range(sample_crop.shape[0]):
                        for j in range(sample_crop.shape[1]):
                            pixel_color = sample_crop[i, j]
                            if np.linalg.norm(pixel_color - avg_color) < threshold:
                                mask[i, j] = 255

                    # Tìm đường viền xung quanh các vùng có màu tương tự
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    # Chọn vùng contour lớn nhất để cắt
                    if len(contours) > 0:
                        largest_contour = max(contours, key=cv2.contourArea)
                        x, y, w, h = cv2.boundingRect(largest_contour)
                        color_crop = sample_crop[y:y+h, x:x+w]
                        sample_resized = cv2.resize(color_crop, (256, 256))

                        # Lưu ảnh đã được cắt và resize
                        output_path = os.path.join(output_folder, filename)
                        cv2.imwrite(output_path, sample_resized)
