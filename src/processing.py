import os
import shutil
import cv2
import pandas as pd
from config import DATA_DIR, HSV_KITS
from loading import load_data
from roi import runROI


def process_data(data_dir=DATA_DIR)-> None:
    """Process the data by copying images to their respective directories and cropping them.

    Args:
        data_dir: directory to load the data from
    """

    # Load data
    df = load_data(file_name='metadata_colors_2025-04-06.csv')
    
    lst_phones = df['Phones'].unique()
    lst_types = df['Types'].unique()

    if os.path.exists(os.path.join(os.path.dirname(data_dir), "failed_images.csv")):
        lst_failed = pd.read_csv(os.path.join(os.path.dirname(data_dir), "failed_images.csv"))['Failed Images'].tolist()
    else:
        lst_failed = []

    # Copy the original image
    for phone in lst_phones:
        os.makedirs(os.path.join(data_dir, "dataset",phone), exist_ok=True)

        for type_ in lst_types:
            os.makedirs(os.path.join(data_dir, "dataset",phone, type_), exist_ok=True)
            os.makedirs(os.path.join(data_dir,"square image",phone, type_), exist_ok=True)
            os.makedirs(os.path.join(data_dir,"roi image",phone, type_), exist_ok=True)
            os.makedirs(os.path.join(data_dir,"background image",phone, type_), exist_ok=True)

            # if phone == 'oppo':
        # Process each image
            for index, row in df.iterrows():
                if row['Phones'] == phone and row['Types'] == type_:
                    image_name = row['Id_imgs']
                    image_path = os.path.join(data_dir, "full",image_name)
                    save_path = os.path.join(data_dir,"dataset",phone, type_, image_name)
                    if os.path.exists(save_path):
                        print(f"Image already exists: {save_path}")
                    else:
                        shutil.copy(image_path, save_path)

                    # Read image
                    image = cv2.imread(save_path)
                    if image is None:
                        print(f"Error reading image: {save_path}")
                        lst_failed.append(image_name)
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
                        lst_failed.append(image_name)
                        continue

                    # Save image
                    raw_image_path = os.path.join(data_dir,"square image",phone, type_, image_name)
                    cv2.imwrite(raw_image_path, raw_image)

                    sample_path = os.path.join(data_dir,"roi image",phone, type_, image_name)
                    cv2.imwrite(sample_path, sample)

                    background_path = os.path.join(data_dir,"background image",phone, type_, image_name)
                    cv2.imwrite(background_path, background)


                    print(f"Processed and saved image: {save_path}\n")

    # Save failed images to csv file
    lst_failed= list(set(lst_failed))  # Remove duplicates
    df_failed = pd.DataFrame(lst_failed, columns=['Failed Images'])  
    df_failed.to_csv(os.path.join(os.path.dirname(data_dir), 'failed_images.csv'), index=False)             

if __name__ == "__main__":
    process_data()