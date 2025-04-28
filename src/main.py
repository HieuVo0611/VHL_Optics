import os

from config import DATA_DIR, META_COLORS
from processing import process_data
from normalize import getFeature
from model import train_models


def e2e ()->None:

    try:
        process_data(
        data_dir=DATA_DIR,
        meta_path=META_COLORS,
        folder_name='full',
        )
        
        print('\nProcessing Data Success!\n')
        
    except:
        print('\nProcessing Data Fail\n')


    try:    
        getFeature(
            df_path=META_COLORS,
            dir_path= os.path.join(DATA_DIR, 'square image'),
            out_path= os.path.join(DATA_DIR, 'csv')
        )

        print('\nFeature Extracting Success!\n')

    except:
        print('\nFeature Extracting Fail\n')


    try:
        train_models(
            meta_path=META_COLORS,
            dir_path=os.path.join(DATA_DIR, 'csv'),
            out_path=os.path.join(DATA_DIR, 'models'),
            split= 0.4,
            n_estimators= 1000,
        )

        print('\nTraining Model Success!\n')

    except:
        print('\nTraining Model Fail\n')


if __name__ == '__main__':
    e2e()