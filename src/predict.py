import os
import cv2
import numpy as np
import pandas as pd
import joblib


from config import HSV_KITS
from roi import runROI
from normalize import FeatureExtractor


def predictImage(
        image_path:str=None,
        model_path:str=None,
        scaler_path:str=None,
        out_path:str=None,
):
    os.makedirs(out_path, exist_ok=True)
    os.makedirs(os.path.join(out_path, "image"), exist_ok=True)
    os.makedirs(os.path.join(out_path, "square image"), exist_ok=True)
    os.makedirs(os.path.join(out_path, "roi image"), exist_ok=True)
    os.makedirs(os.path.join(out_path, "background image"), exist_ok=True)
    os.makedirs(os.path.join(out_path, "csv"), exist_ok=True)

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found")
    cv2.imwrite(os.path.join(out_path, "image", os.path.basename(image_path)), image)
    
    if image_path.__contains__('samsung'):
        kit = HSV_KITS['1.1.1.0.1']
    else:
        kit = HSV_KITS['1.1.1.1.0']
    squared_image, sample, background, _ = runROI(image=image, kit=kit)

    if squared_image is None:
        raise ValueError("Error cropping image")
    
    squared_image_path = os.path.join(out_path, "square image", os.path.basename(image_path))
    cv2.imwrite(squared_image_path, squared_image)

    sample_path = os.path.join(out_path, "roi image", os.path.basename(image_path))
    cv2.imwrite(sample_path, sample)

    background_path = os.path.join(out_path, "background image",os.path.basename(image_path))
    cv2.imwrite(background_path, background)

    del image, squared_image, sample, background, sample_path, background_path

    extractor = FeatureExtractor()
    classification_features, regression_features = extractor.extract_features(squared_image_path, os.path.basename(image_path))
    if classification_features is None or regression_features is None:
        raise ValueError("Error extracting features")
    

    cls_df = pd.DataFrame(classification_features, index=[0])
    # rgs_df = pd.DataFrame(regression_features)

    cls_df.to_csv(os.path.join(out_path, "csv", os.path.basename(image_path).replace('.jpg', '_clf.csv')), index=False)
    # rgs_df.to_csv(os.path.join(out_path, "csv", os.path.basename(image_path).replace('.jpg', '_rgs.csv')), index=False)

    del extractor, classification_features, regression_features

    X_class = cls_df.drop(columns=['id_img','type'])
    scaler = joblib.load(scaler_path)
    X_class_scaled = scaler.transform(X_class)
    clf_model = joblib.load(model_path)
    class_pred = clf_model.predict(X_class_scaled)
    
    print(f"Predicted class: {class_pred[0]}")

    