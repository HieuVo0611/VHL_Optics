import os

from config import DATA_DIR, META_COLORS
from processing import process_data
from normalize import getFeature
from model import train_models
from predict import predictImage


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
    # Run end-to-end process
    while True:
        choice = input("Do you want to run the end-to-end process? (y/n): ").lower()
        if choice == 'y':
            e2e()
            break
        elif choice == 'n':
            print("Skipping end-to-end process.")
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")
        
    out_path = os.path.join(DATA_DIR, 'predict')

    # Loop until user wants to exit
    while True:
        print("Do you want to predict an image? (y/n)")
        choice = input().lower()
        if choice == 'y':
            try:
                image_path = str(input('Input image path you want to predict: '))
                while True:
                    print('=========Select your phone=========\n1. mi8 lite\n2. nokia\n3. oppo\n4. poco f3\n5. samsung\n')
                    phone = int(input('Your slelection: '))
                    if phone == 1:
                        phone = 'mi8 lite'
                        break
                    elif phone == 2:
                        phone = 'nokia'
                        break
                    elif phone == 3:
                        phone = 'oppo'
                        break
                    elif phone == 4:
                        phone = 'poco f3'
                        break
                    elif phone == 5:
                        phone = 'samsung'
                        break
                    elif phone == 0:
                        print('Exit')
                        break
                    else:
                        raise ValueError("Invalid selection")

                if phone ==0:
                    break
                else:
                    print(f"Selected phone: {phone}\n")
                    predictImage(
                        image_path=image_path,
                        model_path=os.path.join(DATA_DIR, 'models', f'classifier_model_{phone}.pkl'),
                        scaler_path=os.path.join(DATA_DIR, 'models', f'classifier_scaler_model_{phone}.pkl'),
                        out_path=out_path,
                    )
                    print("Prediction completed!\n")

            except Exception as e:
                print(f"Error: {e}")
        elif choice == 'n':
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")

