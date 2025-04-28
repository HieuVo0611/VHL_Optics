import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy

from config import DATA_DIR, META_COLORS,IMAGE_EXTENSIONS

class FeatureExtractor:
    def __init__(self, hue_bins=16):
        self.hue_bins = hue_bins

    def extract_features(self, image_path: str, id_imgs:str, types:str, ppm:float):
        classification_features = {}
        regression_features = {}

        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            return None, None
        
        classification_features['id_img'], regression_features['id_img'] = id_imgs, id_imgs
        classification_features['type'] = types
        regression_features['ppm'] = ppm

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        # img_resized = cv2.resize(img_rgb, (256, 256))
        hsv_resized = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
        gray_resized = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

        h, s, v = cv2.split(hsv_resized)

        # Hue histogram (classification)
        hue_hist = cv2.calcHist([h], [0], None, [self.hue_bins], [0, 180])
        hue_hist = hue_hist.flatten()
        hue_hist = hue_hist / hue_hist.sum()
        for i in range(self.hue_bins):
            classification_features[f'hue_hist_{i}'] = hue_hist[i]

        # Hue & Saturation statistics
        classification_features['mean_hue'] = np.mean(h)
        classification_features['std_hue'] = np.std(h)
        classification_features['mean_sat'] = np.mean(s)

        regression_features['mean_sat'] = np.mean(s)
        regression_features['std_sat'] = np.std(s)
        regression_features['mean_val'] = np.mean(v)
        regression_features['std_val'] = np.std(v)

        # GLCM Texture
        gray_scaled = np.uint8(gray_resized / 4)
        glcm = graycomatrix(gray_scaled, distances=[1], angles=[0], levels=64, symmetric=True, normed=True)
        regression_features['glcm_contrast'] = graycoprops(glcm, 'contrast')[0, 0]

        # Entropy
        regression_features['entropy'] = shannon_entropy(gray_resized)

        # Edge density
        edges = cv2.Canny(gray_resized, 100, 200)
        regression_features['edge_density'] = np.sum(edges > 0) / edges.size

        # Contour features
        _, thresh = cv2.threshold(gray_resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            hull = cv2.convexHull(largest_contour)
            hull_area = cv2.contourArea(hull)
            solidity = area / hull_area if hull_area != 0 else 0
        else:
            area = solidity = 0

        regression_features['contour_area'] = area
        regression_features['solidity'] = solidity

        # Ratio (Hue/Saturation) - approximate metric
        mean_hue_total = np.mean(h)
        mean_sat_total = np.mean(s)
        regression_features['hue_sat_ratio'] = mean_hue_total / mean_sat_total if mean_sat_total != 0 else 0

        return classification_features, regression_features



def getFeature(
        df_path:str=None, 
        dir_path:str=None, 
        out_path:str=None
    )->None:

    if df_path is None:
        df_path = META_COLORS
    df = pd.read_csv(df_path)

    if dir_path is None:
        dir_path = os.path.join(DATA_DIR, 'square image')

    if out_path is None:
        out_path = os.path.join(DATA_DIR, 'csv')

    os.makedirs(out_path, exist_ok=True)

    extractor = FeatureExtractor()

    lst_phone= df['Phones'].unique().tolist()
    for phone in lst_phone:
        df_phone = df[df['Phones']==str(phone)].sort_values(by='Types')

        clf_images = []
        rgs_images = []
        # Initialize progress bar
        total_images = len(df_phone)
        with tqdm(total=total_images, desc=f"Feature Extracting [{phone}]", unit="image") as pbar:
            for _, row in df_phone.iterrows():
                id_imgs = row['Id_imgs']
                types = row['Types']
                ppm = row['ppm']
                type_path = os.path.join(dir_path, phone, types)

                if any(str(id_imgs).lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                    image_path = os.path.join(type_path, id_imgs)
                    
                    if not os.path.exists(image_path):
                        pbar.update(1)
                        continue

                    clf_image, rgs_image = extractor.extract_features(image_path, id_imgs, types, ppm)

                    if (clf_image is not None) and (rgs_image is not None):
                        clf_images.append(clf_image)
                        rgs_images.append(rgs_image)
                    
                    # Update progress bar
                    pbar.update(1)
            
            clf_images =pd.DataFrame(clf_images)
            rgs_images =pd.DataFrame(rgs_images)

            clf_images.to_csv(os.path.join(out_path,f'clf_{phone}.csv'), index=False)
            rgs_images.to_csv(os.path.join(out_path,f'rgs_{phone}.csv'), index=False)

        # print(f"Extract {phone} DONE!!!")

                

if __name__ == '__main__':
    import time
    start = time.time()

    getFeature(df_path=META_COLORS, dir_path=os.path.join(DATA_DIR,'square image'))

    print('\nTime processing: ',time.time()- start)     