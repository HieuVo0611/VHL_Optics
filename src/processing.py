import os
import shutil
import cv2
import pandas as pd

from config import DATA_DIR, META_COLORS, HSV_KITS
from loading import load_data
from roi import runROI

def process_data(
        data_dir:str =DATA_DIR, 
        meta_data:str =META_COLORS,
        folder_name:str ='full',
        )-> None:
    """Process the data by copying images to their respective directories and cropping them.

    Args:
        data_dir: directory to load the data from
    """

    # Load data
    df = load_data(file_name=meta_data)
    
    lst_phones = df['Phones'].unique()
    lst_types = df['Types'].unique()    #Label

    if os.path.exists(os.path.join(os.path.dirname(data_dir), "failed_images.csv")):
        lst_failed = pd.read_csv(os.path.join(os.path.dirname(data_dir), "failed_images.csv"))['Failed Images'].tolist()
    else:
        lst_failed = []

    # Process each image
    for phone in lst_phones:
        os.makedirs(os.path.join(data_dir, "dataset",phone), exist_ok=True)

        for type_ in lst_types:
            os.makedirs(os.path.join(data_dir,"dataset",phone, type_), exist_ok=True)
            os.makedirs(os.path.join(data_dir,"square image",phone, type_), exist_ok=True)      #BG + ROI
            os.makedirs(os.path.join(data_dir,"roi image",phone, type_), exist_ok=True)
            os.makedirs(os.path.join(data_dir,"background image",phone, type_), exist_ok=True)  
            os.makedirs(os.path.join(data_dir,"csv",phone), exist_ok=True)

            for index, row in df.iterrows():
                
                # Copy image to the respective directory
                if row['Phones'] == phone and row['Types'] == type_:
                    image_name = row['Id_imgs']
                    image_path = os.path.join(data_dir, folder_name,image_name)
                    save_path = os.path.join(data_dir,"dataset",phone, type_, image_name)
                    if os.path.exists(save_path):
                        print(f"Image already exists: {save_path}")
                    else:
                        shutil.copy(image_path, save_path)

                    # Read image
                    image = cv2.imread(save_path)
                    if image is None:
                        print(f"Error reading image: {save_path}")
                        lst_failed.append([image_name,"Image not found"])
                        continue
                    
                    # Crop image
                    try:
                        if row['Phones'] == 'samsung':
                            raw_image, sample, background, _ = runROI(image=image, kit=HSV_KITS['1.1.1.0.1'])
                        else:
                            raw_image, sample, background, _ = runROI(image=image, kit=HSV_KITS['1.1.1.1.0'])

                        if raw_image is None:
                            print(f"Error cropping image: {save_path}")
                            lst_failed.append(image_name)
                            continue
                    except Exception as e:
                        print(f"Error cropping image: {save_path} - {e}")
                        lst_failed.append([image_name, "Error cropping image"])
                        continue

                    # Save image

                    raw_image_path = os.path.join(data_dir,"square image",phone, type_, image_name)
                    cv2.imwrite(raw_image_path, raw_image)

                    sample_path = os.path.join(data_dir,"roi image",phone, type_, image_name)
                    cv2.imwrite(sample_path, sample)

                    background_path = os.path.join(data_dir,"background image",phone, type_, image_name)
                    cv2.imwrite(background_path, background)

                    print(f"Processed and saved image: {save_path}\n")

    lst_failed= list(set(lst_failed))  # Remove duplicates
    df_failed = pd.DataFrame(lst_failed, columns=['Failed Images', 'Error'])  
    df_failed.to_csv(os.path.join(os.path.dirname(data_dir), 'failed_images.csv'), index=False)

    failed_ids = df_failed['Failed Images'].astype(str).tolist()
    cleaned_df = df[~df['Id_imgs'].astype(str).isin(failed_ids)]     
    cleaned_df.to_csv(os.path.join(os.path.dirname(data_dir), 'metadata_colors.csv'), index=False)

if __name__ == "__main__":
    process_data()