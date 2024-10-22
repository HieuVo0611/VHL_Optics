import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']




def apply_clahe(image,threshold=2.0):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # mean_l = np.mean(l)
    clahe = cv2.createCLAHE(clipLimit=threshold, tileGridSize=(64,64))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final


def mask_roi(image_path):
    image = cv2.imread(image_path)
    clahe_img = apply_clahe(image)
    # Chuyển đổi ảnh từ BGR sang GreyScale
    gray_image = cv2.cvtColor(clahe_img, cv2.COLOR_BGR2GRAY)
    # rgb_image= cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    # Xác định ngưỡng màu cho mẫu 
    lower_bound_obj = np.array([55])   # Ngưỡng dưới cho màu xanh
    upper_bound_obj = np.array([255]) # Ngưỡng trên cho màu xanh
    kernel = np.ones((64,64), np.uint8)
    mask_obj = cv2.inRange(gray_image, lower_bound_obj, upper_bound_obj)
    mask_obj = cv2.morphologyEx(mask_obj, cv2.MORPH_OPEN, kernel)
    mask_obj = cv2.morphologyEx(mask_obj, cv2.MORPH_CLOSE, kernel)

    # Tìm các contours (biên) của vùng màu
    contours, _ = cv2.findContours(mask_obj, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Duyệt qua các contours và tìm bounding box của từng vùng màu
    for contour in contours:    
        x, y, w, h = cv2.boundingRect(contour)  # Tọa độ và kích thước của bounding box
        print(f'Tọa độ vùng màu: ({x}, {y}), Kích thước: {w}x{h}')
    
        # Vẽ hình chữ nhật bao quanh vùng màu
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 20)


    # Tìm ROI bằng cách áp dụng mask lên ảnh HSV
    roi_obj = cv2.bitwise_and(clahe_img, clahe_img, mask=mask_obj)
   

    # Xác định ngưỡng màu cho vùng nước
    lower_bound = np.array([70,101,0])   # Ngưỡng dưới cho màu xanh 
    upper_bound = np.array([255,255,255]) # Ngưỡng trên cho màu xanh

    # Tạo mask bằng cách áp dụng ngưỡng màu
    mask = cv2.inRange(roi_obj, lower_bound, upper_bound)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


    # Tìm ROI bằng cách áp dụng mask lên ảnh gốc
    roi = cv2.bitwise_and(image, image, mask=mask)
    # Hiển thị ảnh gốc, mask, và ROI
    plt.figure(figsize=(15,5))
    plt.subplot(1, 5, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(' Image')

    plt.subplot(1, 5, 2)
    plt.imshow(gray_image)
    plt.title('Gray Image')

    plt.subplot(1, 5, 3)
    # plt.imshow(cv2.cvtColor(roi_obj,cv2.COLOR_GRAY2RGB))
    plt.imshow(roi_obj)
    plt.title('ROI_OBJ')

    plt.subplot(1, 5, 4)
    plt.imshow(mask, cmap='gray')
    plt.title('Mask')

    plt.subplot(1, 5, 5)
    plt.imshow(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    plt.title('ROI')

    plt.show()
    # return mask, roi

path = './folder/meatadataset/'
save = 'D:/Work/Water Environment Pollution/folder/hsvimg/'

img = 'Hs2l2_ngochanpham274@gmail.com_2024-08-02 11_13_40_0.05 ppm_R2_P1_F_0.0534_ip6_10.877250171361_106.67835215932.jpg'
image_path =  path+img
mask_roi(image_path)




# for file in os.listdir(path):
#     if any(file.lower().endswith(ext) for ext in image_extensions):
#         img_path = os.path.join(path+file)
#         img = cv2.imread(img_path)
#         final, limg = apply_clahe(img)
#         final_img = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
#         cv2.imwrite(os.path.join(save,f'CLAHE_{file}'),final_img, [cv2.IMWRITE_JPEG_QUALITY,100])