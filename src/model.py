import joblib
import os
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, mean_squared_error
import pandas as pd

from config import DATA_DIR, META_COLORS

def train_models(
        meta_data:str = None, 
        dir_path:str = None,
          out_path:str = None
    )->None:
    """
    Train classification and regression models from extracted features.

    Args:
        class_df (pd.DataFrame): Feature dataframe for classification (must contain 'label' column).
        reg_df (pd.DataFrame): Feature dataframe for regression (must contain 'ppm' column).

    Returns:
        clf_model, reg_model: trained models.
    """
    if dir_path is None:
        dir_path = os.path.join(DATA_DIR, 'csv')
    
    if meta_data is None:
        meta_data = META_COLORS

    if out_path is None:
        out_path = os.path.join(os.path.dirname(DATA_DIR),'models')
    os.makedirs(out_path, exist_ok=True)


    df = pd.read_csv(meta_data)
    lst_phone = df['Phones'].unique().tolist()

    for phone in lst_phone:
        class_df = pd.read_csv(os.path.join(dir_path, f'clf_{phone}.csv'))
        reg_df = pd.read_csv(os.path.join(dir_path, f'rgs_{phone}.csv'))

        # --- Classification --- #
        X_class = class_df.drop(columns=['id_img','type'])
        y_class = class_df['type']

        Xc_train, Xc_test, yc_train, yc_test = train_test_split(X_class, y_class, test_size=0.2, random_state=42, stratify=y_class)

        scaler_c = StandardScaler()
        X_train_c_scaled = scaler_c.fit_transform(Xc_train)
        X_test_c_scaled = scaler_c.transform(Xc_test)

        clf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        clf_model.fit(X_train_c_scaled, yc_train)
        

        print(f"\n================== {phone} report ==================")
        # Report
        class_preds = clf_model.predict(X_test_c_scaled)
        print("\n--- Classification Report ---")
        print(classification_report(yc_test, class_preds))

        # Save model
        joblib.dump(clf_model, os.path.join(out_path,f'classifier_model_{phone}.pkl'))

        # # --- Regression --- #
        
        # X_reg = reg_df.drop(columns=['id_img','ppm'])
        # y_reg = reg_df['ppm']

        # Xr_train, Xr_test, yr_train, yr_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42, stratify=y_reg)

        # scaler_r = StandardScaler()
        # X_train_r_scaled = scaler_r.fit_transform(Xr_train)
        # X_test_r_scaled = scaler_r.transform(Xr_test)
        # reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
        # reg_model.fit(X_train_r_scaled, yr_train)

        # # Report
        # reg_preds = reg_model.predict(X_test_r_scaled)
        # mse = mean_squared_error(yr_test, reg_preds)
        # print("\n--- Regression Report ---")
        # print(f"MSE: {mse:.4f}")

        # # Save model
        # joblib.dump(reg_model, os.path.join(out_path,f'regression_model_{phone}.pkl'))


if __name__ == '__main__':
    meta_data = './data/metadata_colors.csv'
    train_models(meta_data=meta_data)