import os
import pandas as pd
from config import DATA_DIR, META_COLORS, COLUMNS, IMAGE_EXTENSIONS


def create_meta_data(
        data_dir:str= None, 
        out_dir:str=None,
        cols:list=None,
        lst_failed:list=None,
        labels:int=3,
        phones:int=5
        )-> pd.DataFrame:
    """Create meta data for the specified directory. (./data/meta.csv).

    Args:
        data_dir: directory to create the meta data for 
        file_name: name of the file to create
        cols: columns to use in the meta data

    return: dataframe with the meta data
    """
    if data_dir is None:
        data_dir = os.path.join(DATA_DIR, 'full')

    if out_dir is None:
        out_dir = META_COLORS
    
    if cols is None:
        cols = COLUMNS
    

    df = pd.DataFrame(columns=cols)

    for file in os.listdir(data_dir):
        sample=[]
        try:
            if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                if '2025' in file:
                    # name_sample = file.strip().split(' ',1)[-1].strip().split('_',3)[-1].strip()
                    # sample.append(name_sample)
                    sample.append(file)
                    sample_info = file.split('ppm')
                    sample.append(sample_info[0].strip().split('_')[-2].lower())
                    sample.append(sample_info[0].strip().split('_')[-1])
                    sample.append(sample_info[0].strip().split('_')[-3].lower())
                    sample.append(sample_info[1].strip().split('_')[1])
                    sample.append(sample_info[0].strip().split(' ')[0].split('_')[-1])
            if len(sample) == 6:
                sample_df = pd.DataFrame([sample], columns=cols)
                df = pd.concat([df, sample_df], ignore_index=True)
        except Exception as e:
            error = [file, "Can't get image into metadata"]
            if error not in lst_failed:
                lst_failed.append(error)
            print(f"Error processing file {file}: {e}")

    # Only keep the first 3 most common types of 'Types' in the dataset
    types_to_keep = df['Types'].value_counts().nlargest(labels).index
    df = df[df['Types'].isin(types_to_keep)]
    df.reset_index(drop=True, inplace=True)

    # Only keep the first 5 most common types of 'Phones' in the dataset
    phones_to_keep = df['Phones'].value_counts().nlargest(phones).index
    df = df[df['Phones'].isin(phones_to_keep)]
    df.reset_index(drop=True, inplace=True)

    # Sort the dataframe by 'Date'
    df.sort_values(by='Date', inplace=True)

    df.to_csv(out_dir, index=False)
    return lst_failed


def load_data(
        data_dir= None, 
        df_path=None,
        lst_failed:list=None,
        ):
    """Load data from the specified directory (./data/meta.csv).

    Args:
        data_dir: directory to load the data from 
        file_name: name of the file to load

    return: dataframe with the loaded data in
    """
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
    data = load_data()
