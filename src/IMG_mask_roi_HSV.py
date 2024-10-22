import os 
import cv2
import numpy as np
import matplotlib.pyplot as plt


def mask_roi(image_path):
    image = cv2.imread(image_path)

    # Chuyển đổi ảnh từ BGR sang HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Xác định ngưỡng màu cho mẫu 
    lower_bound_obj = np.array([0, 0, 56])   # Ngưỡng dưới cho màu xanh
    upper_bound_obj = np.array([120, 130, 56]) # Ngưỡng trên cho màu xanh
    kernel = np.ones((3,3), np.uint8)
    mask_obj = cv2.inRange(hsv_image, lower_bound_obj, upper_bound_obj)
    mask_obj = cv2.morphologyEx(mask_obj, cv2.MORPH_OPEN, kernel)
    mask_obj = cv2.morphologyEx(mask_obj, cv2.MORPH_CLOSE, kernel)

    # Tìm ROI bằng cách áp dụng mask lên ảnh HSV
    roi_obj = cv2.bitwise_and(hsv_image, hsv_image, mask=mask_obj)
   

    # Xác định ngưỡng màu cho vùng nước
    lower_bound = np.array([75, 70, 101])   # Ngưỡng dưới cho màu xanh
    upper_bound = np.array([130, 255, 255]) # Ngưỡng trên cho màu xanh

    # Tạo mask bằng cách áp dụng ngưỡng màu
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    kernel = np.ones((15,15), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


    # Tìm ROI bằng cách áp dụng mask lên ảnh gốc
    roi = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)

    # Hiển thị ảnh gốc, mask, và ROI
    plt.figure(figsize=(15,5))
    plt.subplot(1, 5, 1)
    plt.imshow(cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),cv2.COLOR_RGB2BGR))
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('BGR Image')

    plt.subplot(1, 5, 2)
    # plt.imshow(cv2.cvtColor(hsv_image,cv2.COLOR_HSV2RGB))
    plt.imshow(hsv_image)
    plt.title('HSV Image')

    plt.subplot(1, 5, 3)
    plt.imshow(cv2.cvtColor(cv2.cvtColor(roi_obj, cv2.COLOR_HSV2BGR),cv2.COLOR_BGR2HSV))
    plt.imshow(roi_obj)
    plt.title('ROI_OBJ')

    plt.subplot(1, 5, 4)
    plt.imshow(mask, cmap='gray')
    plt.title('Mask')

    plt.subplot(1, 5, 5)
    plt.imshow(cv2.cvtColor(roi, cv2.COLOR_HSV2BGR))
    plt.title('ROI')

    plt.show()
    # return mask, roi




    
path='D:/Work/Water Environment Pollution/hinhanh_05082024/hinhanh/'
# image = '00tbm_ngochanpham274@gmail.com_2024-06-10 16_38_05_0.6_0.6_R3_P3_F_Phuc__.thumbnail.jpg'
# image = '0aNvD_ngochanpham274@gmail.com_2024-08-01 15_48_54_10 ppm_R2_P1_F_1.3356_10.8769656_106.6783962.thumbnail.jpg'
image = '0hnK2_ngochanpham274@gmail.com_2024-06-10 11_54_59_0.04_0.04_R2_P1_0_Linh__.thumbnail.jpg'
mask_roi(path+image)



# if __name__ == '__main__':
#     path= 'hinhanh_05082024/hinhanh/full/'
#     mask_path='folder/mask/'
#     roi_path='folder/roi/'
#     image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
#     for image in os.listdir(path):
#         if any(image.lower().endswith(ext) for ext in image_extensions):
#             img_path = os.path.join(path, image)
#             if os.path.isfile(img_path):
#                 mask_img, roi_img = mask_roi(img_path)
#                 cv2.imwrite(os.path.join(mask_path,f'mask_{image}'),mask_img, [cv2.IMWRITE_JPEG_QUALITY,100])
#                 cv2.imwrite(os.path.join(roi_path,f'roi_{image}'),roi_img, [cv2.IMWRITE_JPEG_QUALITY,100])
#         else:
#             pass