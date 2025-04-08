import os
import pandas as pd
from config import DATA_DIR, META_COLORS, COLUMNS, IMAGE_EXTENSIONS


def create_meta_data(
        data_dir= None, 
        file_name=None,
        cols=None,
        )-> pd.DataFrame:
    """
    Create meta data for the specified directory. (./data/meta.csv).

    :param data_dir: directory to create the meta data for
    :param file_name: name of the file to create
    :return: dataframe with the meta data
    """
    if data_dir is None:
        data_dir = os.path.join(DATA_DIR, 'full')

    if file_name is None:
        file_name = os.path.join(os.path.dirname(os.path.dirname(data_dir)),META_COLORS)
    else:
        pass
    
    if cols is None:
        cols = COLUMNS
    
    # with open(file_name, 'w') as f:
    #     f.write("Meta Data")
    
    df = pd.DataFrame(columns=cols)

    for file in os.listdir(data_dir):
        sample=[]
        try:
            if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                if '2025' in file:
                    name_sample = file.strip().split(' ',1)[-1].strip().split('_',3)[-1].strip()
                    sample.append(name_sample)
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
            print(f"Error processing file {file}: {e}")

    # Only keep the first 3 most common types of 'Types' in the dataset
    types_to_keep = df['Types'].value_counts().nlargest(3).index
    df = df[df['Types'].isin(types_to_keep)]
    df.reset_index(drop=True, inplace=True)

    # Only keep the first 5 most common types of 'Phones' in the dataset
    phones_to_keep = df['Phones'].value_counts().nlargest(5).index
    df = df[df['Phones'].isin(phones_to_keep)]
    df.reset_index(drop=True, inplace=True)

    # Sort the dataframe by 'Date'
    df.sort_values(by='Date', inplace=True)

    df.to_csv(file_name, index=False)



def load_data(
        data_dir= None, 
        file_name=None
        )-> pd.DataFrame:
    """
    Load data from the specified directory (./data/meta.csv).

    :param data_dir: directory to load the data from 
    :param file_name: name of the file to load
    :return: dataframe with the loaded data in
    """
    if data_dir is None:
        data_dir = DATA_DIR

    if file_name is None:
        create_meta_data()
        file_name = os.path.join(os.path.dirname(data_dir),META_COLORS)
    else:
        file_name = os.path.join(data_dir, file_name)
    
    # with open(file_name, 'r') as f:
    #     data = f.read()
    data = pd.read_csv(file_name)
    return data


# if __name__ == "__main__":
#     data = load_data()
#     print(data.head(10))