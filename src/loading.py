import os
import pandas as pd
from config import DATA_DIR, META_COLORS, COLUMNS, IMAGE_EXTENSIONS


def create_meta_data(
        data_dir: str = None, 
        out_dir: str = None,
        cols: list = None,
        lst_failed: list = None,
        labels: int = 3,
        phones: int = 5,
        ) -> pd.DataFrame:
    """Create meta data for the specified directory. (./data/meta.csv).

    Args:
        data_dir: directory to create the meta data for 
        file_name: name of the file to create
        cols: columns to use in the meta data

    return: dataframe with the meta data
    """
    if data_dir is None:
        data_dir = os.path.join(DATA_DIR, '_uploadRGB_5phones_sorted')

    if out_dir is None:
        out_dir = META_COLORS
    
    if cols is None:
        cols = COLUMNS

    if lst_failed is None:
        lst_failed = []

    df = pd.DataFrame(columns=cols)

    for phone_dir in os.listdir(data_dir):
        phone_path = os.path.join(data_dir, phone_dir)
        if not os.path.isdir(phone_path):
            continue

        for repeat_dir in os.listdir(phone_path):
            repeat_path = os.path.join(phone_path, repeat_dir)
            if not os.path.isdir(repeat_path):
                continue

            for file in os.listdir(repeat_path):
                sample = []
                try:
                    if not any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                        continue
                    if 'ppm' not in file or '2025' not in file:
                        continue

                    # Parse the file name
                    filename = file
                    name_part = file.split('ppm')
                    info = name_part[0].split('_')
                    after_ppm = name_part[1].split('.')

                    ppm_str = info[-1].replace('ppm', '').strip().replace(',', '.')
                    ppm = float(ppm_str)
                    chemical = info[-2].strip().lower()
                    phone = info[-3].strip().lower()
                    date_raw = file.split('_')[2]
                    photo_idx = after_ppm[1].strip()

                    sample.append(filename)
                    sample.append(chemical)
                    sample.append(ppm)
                    sample.append(phone)
                    sample.append(photo_idx)
                    sample.append(date_raw)

                    if len(sample) == 6:
                        sample_df = pd.DataFrame([sample], columns=cols)
                        df = pd.concat([df, sample_df], ignore_index=True)

                except Exception as e:
                    error = [file, "Can't parse metadata"]
                    if error not in lst_failed:
                        lst_failed.append(error)
                    print(f"Error processing file {file}: {e}")

    # Filter the data
    types_to_keep = df['Types'].value_counts().nlargest(labels).index
    df = df[df['Types'].isin(types_to_keep)]

    phones_to_keep = df['Phones'].value_counts().nlargest(phones).index
    df = df[df['Phones'].isin(phones_to_keep)]

    df.reset_index(drop=True, inplace=True)
    df.sort_values(by='Date', inplace=True)
    df.to_csv(out_dir, index=False)
    return lst_failed
                    

def load_data(
        data_dir= None, 
        df_path=None,
        lst_failed:list=None,
        ):
    if data_dir is None:
        data_dir = DATA_DIR

    if df_path is None:
        lst_failed = create_meta_data(lst_failed=lst_failed)
        df_path = META_COLORS
    else:
        if not os.path.exists(META_COLORS):
            lst_failed = create_meta_data(lst_failed=lst_failed)

    data = pd.read_csv(df_path)
    return data, lst_failed


if __name__ == "__main__":
    data, failed = load_data()
    print("Metadata loaded successfully", data.shape[0])