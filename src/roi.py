import cv2
from config import HSV_KITS, RATIO, SIZE_IMG, SIZE_CUT

def cut_image(image, ratio=None, size=None):
    """
    Crop the image to the specified ratio and size.
    :param image: The input image
    :param ratio: The aspect ratio for cropping
    :param size: The size of the cropped image
    :return: The cropped image
    """
    # Set default values for ratio and size if not provided
    if ratio is None:
        ratio = RATIO
    if size is None:
        size = SIZE_CUT
    # Check if the image is empty 
    if image is None:
        raise ValueError("The image is empty. Please check the input image path.")

    # Get the coordinates of middle of the image
    height, width = image.shape[:2]
    center_x = width // 2
    center_y = height // 2

    # Cropping the image with ratio 3:4 for the center of the image
    # Calculate the cropping box dimensions
    crop_width = int(width * ratio)  # 3:4 ratio
    crop_height = int(height * ratio)  # 3:4 ratio
    x1 = max(center_x - crop_width // 2, 0)
    y1 = max(center_y - crop_height // 2, 0)
    x2 = min(center_x + crop_width // 2, width)
    y2 = min(center_y + crop_height // 2, height)
    # Crop the image using the calculated coordinates
    cropped_image = image[y1:y2, x1:x2]
    # Resize the cropped image to 300x300 pixels
    resized_image = cv2.resize(cropped_image, size, interpolation=cv2.INTER_AREA)
    return resized_image

def square_image(image, size=None):
    """
    Crop the image to a square centered around the middle of the image.
    :param image: The input image
    :param size: The size of the square crop
    :return: The cropped square image
    """
    # Set default size if not provided
    if size is None:
        size = SIZE_IMG
    # Get the dimensions of the image
    height, width = image.shape[:2]

    # Calculate the center of the image
    center_x = width // 2
    center_y = height // 2

    # Calculate the cropping box dimensions
    crop_size = size  # 224x224 square crop
    x1 = max(center_x - crop_size // 2, 0)
    y1 = max(center_y - crop_size // 2, 0)
    x2 = min(center_x + crop_size // 2, width)
    y2 = min(center_y + crop_size // 2, height)

    # Crop the image using the calculated coordinates
    cropped_image = image[y1:y2, x1:x2]

    return cropped_image

def roi_image(cropped_image, kit=None, size=None):
    """
    Get the squared frame of the image.
    :param cropped_image: The cropped image
    :return: The squared frame of the image
    """
    # Set default kit and size if not provided
    if kit is None:
        kit = HSV_KITS['1.1.1.1.0']
    if size is None:
        size = (SIZE_IMG, SIZE_IMG)
    
    # Change the color space to HSV
    img_hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)

    # Create a mask using the HSV kit
    mask = cv2.inRange(img_hsv, kit[0], kit[1])
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if not contours:
        # raise ValueError("Your image does not have any countours")
        return None
    
    x, y, w, h = cv2.boundingRect(contours[0])
    roi = cropped_image[y : y + h, x : x + w]
    # Resize the cropped image to the specified size
    roi = cv2.resize(roi, size, interpolation=cv2.INTER_AREA)

    return roi


# if __name__ == "__main__":
#     # Example usage
#     root = "D:/Work/VHL/VHL_Optics/data/hinhanh/poco f3/rhodamine b/"
#     image_path = "1kI1M_ngochanpham274@gmail.com_2025-03-28 15_33_14_Tien_poco f3_Rhodamine B_100ppm_3_6__10.877064_106.6781564.jpg"
#     image = cv2.imread(root+image_path)
#     cropped_image = cut_image(image, ratio=RATIO, size=SIZE_CUT)
#     squared_frame = square_image(cropped_image) 
#     roi_image, counts = roi_image(squared_frame)

#     # Display contours on the original image
#     plt.figure(figsize=(10, 5))
#     plt.subplot(1, 2, 1)
#     plt.imshow(cv2.cvtColor(squared_frame, cv2.COLOR_BGR2HSV))
#     plt.title("Original Image")
#     plt.axis("off")

#     for contour in counts:
#         cv2.drawContours(squared_frame, [contour.astype(int)], -1, (0, 255, 0), 1)
#     plt.subplot(1, 2, 2)
#     plt.imshow(cv2.cvtColor(squared_frame, cv2.COLOR_BGR2HSV))
#     plt.title("Squared Frame with Contours")
#     plt.axis("off")
#     plt.show()
