import os

from config import DATA_DIR, META_COLORS
from processing import process_data
from normalize import getFeature
from model import train_models


def e2e ()->None:

    try:
        process_data(
        data_dir=DATA_DIR,
        meta_data=META_COLORS,
        folder_name='full')
        
        print('Processing Data Success!')
        
    except:
        print('Processing Data Fail')


    try:    
        getFeature(
            df=META_COLORS,
            dir_path= os.path.join(DATA_DIR, 'square image'),
        )

        print('Feature Extracting Success!')

    except:
        print('Feature Extracting Fail')


    try:
        train_models(
            metadata=META_COLORS,
            dir_path=os.path.join(DATA_DIR, 'csv'),
        )

        print('Training Model Success!')

    except:
        print('Training Model Fail')


if __name__ == '__main__':
    e2e()