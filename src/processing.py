import os
import shutil
import cv2

from config import DATA_DIR, HSV_KITS
from load import load_data
from roi import cut_image, square_image, roi_image


def process_data(data_dir=DATA_DIR):
    """
    Process the data by copying images to their respective directories and cropping them.
    :param data_dir: directory to load the data from
    :return: None
    """

    # Load data
    df = load_data()
    
    lst_phones = df['Phones'].unique()
    lst_types = df['Types'].unique()

    # Copy the original image
    for phone in lst_phones:
        os.makedirs(os.path.join(data_dir, phone), exist_ok=True)

        for type_ in lst_types:
            os.makedirs(os.path.join(data_dir,phone, type_), exist_ok=True)
            os.makedirs(os.path.join(data_dir,phone, type_, "cropped"), exist_ok=True)
        
            # Process each image
            for index, row in df.iterrows():
                if row['Phones'] == phone and row['Types'] == type_:
                    image_name = row['Id_imgs']
                    image_path = os.path.join(data_dir, "full",image_name)
                    save_path = os.path.join(data_dir,phone, type_, image_name)
                    if os.path.exists(save_path):
                        print(f"Image already exists: {save_path}")
                    else:
                        shutil.copy(image_path, save_path)

                    # Read image
                    image = cv2.imread(save_path)
                    if image is None:
                        print(f"Error reading image: {save_path}")
                        continue
                    
                    # Crop image
                    cropped_image = cut_image(image)
                    cropped_image = square_image(cropped_image)
                    if row['Phones'] == 'samsung':
                        cropped_image = roi_image(cropped_image, kit=HSV_KITS['1.1.1.0.1'])
                    else:
                        cropped_image = roi_image(cropped_image, kit=HSV_KITS['1.1.1.1.0'])

                    if cropped_image is None:
                        print(f"Error cropping image: {save_path}")
                        continue

                    # Save cropped image
                    cropped_image_path = os.path.join(data_dir,phone, type_, "cropped", image_name)
                    cv2.imwrite(cropped_image_path, cropped_image)
                    print(f"Processed and saved image: {index}\n")


if __name__ == "__main__":
    process_data()