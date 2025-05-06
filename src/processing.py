import os
import shutil
import cv2
import pandas as pd
from tqdm import tqdm

from config import DATA_DIR, META_COLORS, HSV_KITS
from loading import load_data
from roi import runROI

def process_data(
        data_dir: str = DATA_DIR,
        meta_path: str = META_COLORS,
        folder_name: str = 'full',
) -> None:
    """Process the data by copying images to their respective directories and cropping them.

    Args:
        data_dir: directory to load the data from
    """
    if os.path.exists(os.path.join(data_dir, "failed_images.csv")):
        lst_failed = pd.read_csv(os.path.join(data_dir, "failed_images.csv"))['Failed Images'].tolist()
    else:
        lst_failed = []

    # Load data
    df, lst_failed = load_data(df_path=meta_path, lst_failed=lst_failed)
    
    lst_phones = sorted(df['Phones'].unique())
    lst_types = sorted(df['Types'].unique())  # Label

    
    # Process each image
    for phone in lst_phones:
        for type_ in lst_types:
            os.makedirs(os.path.join(data_dir, "dataset", phone, type_), exist_ok=True)
            os.makedirs(os.path.join(data_dir, "square image", phone, type_), exist_ok=True)  # BG + ROI
            os.makedirs(os.path.join(data_dir, "roi image", phone, type_), exist_ok=True)
            os.makedirs(os.path.join(data_dir, "background image", phone, type_), exist_ok=True)

            # Initialize progress bar
            total_images = len(df[(df['Phones'] == phone) & (df['Types'] == type_)])
            with tqdm(total=total_images, desc=f"Processing [{phone}] - [{type_}]", unit="image") as pbar:

                for index, row in df.iterrows():
                    if row['Phones'] == phone and row['Types'] == type_:
                        image_name = row['Id_imgs']
                        image_path = os.path.join(data_dir, folder_name, image_name)
                        save_path = os.path.join(data_dir, "dataset", phone, type_, image_name)
                        if os.path.exists(save_path):
                            pbar.update(1)
                            continue
                        else:
                            shutil.copy(image_path, save_path)
                        
                        # Read image
                        image = cv2.imread(save_path)
                        if image is None:
                            error = [image_name, "Image not found"]
                            if error not in lst_failed:
                                lst_failed.append(error)
                            pbar.update(1)
                            continue
                        
                        # Crop image
                        try:
                            if row['Phones'] == 'samsung':
                                squared_image, sample, background, _ = runROI(image=image, kit=HSV_KITS['1.1.1.0.1'])
                            else:
                                squared_image, sample, background, _ = runROI(image=image, kit=HSV_KITS['1.1.1.1.0'])

                            if squared_image is None:
                                error = [image_name, "Error cropping image"]
                                if error not in lst_failed:
                                    lst_failed.append(error)
                                pbar.update(1)
                                continue
                        except Exception as e:
                            error = [image_name, "Error cropping image"]
                            if error not in lst_failed:
                                lst_failed.append(error)
                            pbar.update(1)
                            continue

                        # Save image
                        squared_image_path = os.path.join(data_dir, "square image", phone, type_, image_name)
                        cv2.imwrite(squared_image_path, squared_image)

                        sample_path = os.path.join(data_dir, "roi image", phone, type_, image_name)
                        cv2.imwrite(sample_path, sample)

                        background_path = os.path.join(data_dir, "background image", phone, type_, image_name)
                        cv2.imwrite(background_path, background)

                        # Update progress bar
                        pbar.update(1)

    lst_failed = list(set(lst_failed))  # Remove duplicates
    df_failed = pd.DataFrame(lst_failed, columns=['Failed Images', 'Error'])  
    df_failed.to_csv(os.path.join(data_dir, 'failed_images.csv'), index=False)

    failed_ids = df_failed['Failed Images'].astype(str).tolist()
    cleaned_df = df[~df['Id_imgs'].astype(str).isin(failed_ids)]     
    cleaned_df.to_csv(META_COLORS, index=False)


if __name__ == "__main__":
    process_data()