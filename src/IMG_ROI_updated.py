import cv2
import numpy as np
import os
from multiprocessing import Pool

# Đường dẫn đến thư mục chứa ảnh gốc và đầu ra
input_folder = './folder/meatadataset/'
output_folder = './folder/roidata1/'

# Kiểm tra nếu thư mục đầu ra không tồn tại, tạo mới
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Hàm tính khoảng cách Euclidean giữa hai màu RGB (không cần sqrt)
def color_distance_squared(c1, c2):
    return np.sum((c1 - c2) ** 2)

# Hàm kiểm tra xem màu có phải gần màu đen hay không (dùng khoảng cách bình phương)
def is_black(color, threshold=900):  # Sử dụng threshold là 30^2
    black = np.array([0, 0, 0])
    gray_greenish = np.array([64, 65, 58])
    return (color_distance_squared(color, black) < threshold or 
            color_distance_squared(color, gray_greenish) < threshold)

# Hàm chính xử lý một ảnh
def process_image(filename):
    if not (filename.endswith('.jpg') or filename.endswith('.png')):
        return  # Bỏ qua nếu không phải file ảnh

    image_path = os.path.join(input_folder, filename)
    image = cv2.imread(image_path)
    if image is None:
        return

    image = cv2.resize(image, (300, 400))
    height, width, _ = image.shape

    # Chuyển ảnh sang thang độ xám và thực hiện CLAHE
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Ngưỡng nhị phân
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)

    # Tìm các đường viền
    contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    center_x, center_y = width // 2, height // 2
    closest_square = None
    min_distance = float('inf')

    # Duyệt qua tất cả các đường viền để tìm hình vuông
    for contour in contours:
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:  # Kiểm tra hình vuông/hình chữ nhật
            x, y, w, h = cv2.boundingRect(approx)
            if 0.9 <= w / h <= 1.1:
                square_center_x = x + w // 2
                square_center_y = y + h // 2
                distance = np.sqrt((square_center_x - center_x) ** 2 + (square_center_y - center_y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_square = (x, y, w, h)

    # Nếu tìm thấy hình vuông gần trung tâm nhất
    if closest_square is not None:
        x, y, w, h = closest_square
        square_crop = image[y:y+h, x:x+w]
        avg_color = np.mean(square_crop, axis=(0, 1)).astype(int)

        if is_black(avg_color):
            # Phát hiện cạnh Canny
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                cropped_image = image[y:y+h, x:x+w]
                resized_image = cv2.resize(cropped_image, (256, 256))

                # Lưu ảnh đã xử lý
                output_path = os.path.join(output_folder, 'cropped_' + filename)
                cv2.imwrite(output_path, resized_image)
        else:
            # Nếu màu không đen, xử lý với màu tương tự
            threshold = 50
            lower_bound = avg_color - threshold
            upper_bound = avg_color + threshold
            mask = cv2.inRange(image, lower_bound, upper_bound)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                cropped_image = image[y:y+h, x:x+w]
                resized_image = cv2.resize(cropped_image, (256, 256))

                # Lưu ảnh đã xử lý
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, resized_image)

# Sử dụng multiprocessing để xử lý nhiều ảnh cùng lúc
if __name__ == "__main__":
    with Pool() as pool:
        pool.map(process_image, os.listdir(input_folder))
