import os
import sys
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, f1_score

# Ensure the parent directory is in the Python path for module import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.classifiers import get_classifiers
from config import DATA_DIR, META_COLORS

def train_models(
    meta_path: str = None,
    dir_path: str = None,
    out_path: str = None,
    n_estimators: int = 100,
    n_splits: int = 5,
) -> None:
    if dir_path is None:
        dir_path = os.path.join(DATA_DIR, 'csv')
    if meta_path is None:
        meta_path = META_COLORS
    if out_path is None:
        out_path = os.path.join(DATA_DIR, 'models')
    os.makedirs(out_path, exist_ok=True)

    df = pd.read_csv(meta_path)
    lst_phone = df['Phones'].unique().tolist()

    classifiers = get_classifiers(n_estimators=n_estimators)
    results = []

    for phone in lst_phone:
        clf_path = os.path.join(dir_path, f'clf_{phone}.csv')
        if not os.path.exists(clf_path):
            print(f"Missing file: {clf_path}, skipping")
            continue

        df_phone = pd.read_csv(clf_path)
        if df_phone['type'].nunique() < 2:
            print(f"Not enough classes for {phone}, skipping")
            continue

        X = df_phone.drop(columns=['id_img', 'type'])
        y = df_phone['type']

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)

        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

        for name, model in classifiers.items():
            print(f"\nCross-validating {name} for {phone}...")

            acc_scores = []

            for train_idx, test_idx in skf.split(X_scaled, y_encoded):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y_encoded[train_idx], y_encoded[test_idx]

                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                acc_scores.append(acc)

            avg_acc = np.mean(acc_scores)
            std_acc = np.std(acc_scores)

            # Save final model (trained on full data)
            model.fit(X_scaled, y_encoded)
            joblib.dump(model, os.path.join(out_path, f'{name}_model_{phone}.pkl'))
            joblib.dump(scaler, os.path.join(out_path, f'{name}_scaler_{phone}.pkl'))
            joblib.dump(label_encoder, os.path.join(out_path, f'{name}_label_encoder_{phone}.pkl'))

            print(f"Average Accuracy (CV): {avg_acc:.4f} ± {std_acc:.4f}")

            y_full_pred = model.predict(X_scaled)
            y_full_pred_str = label_encoder.inverse_transform(y_full_pred)
            y_true_str = label_encoder.inverse_transform(y_encoded)

            report = classification_report(y_true_str, y_full_pred_str)
            f1_macro = f1_score(y_true_str, y_full_pred_str, average='macro')
            print(report)

            results.append({
                'phone': phone,
                'model': name,
                'accuracy': avg_acc,
                'std': std_acc,
                'f1_macro': f1_macro
            })

    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(out_path, 'classification_summary.csv'), index=False)

    # Export LaTeX table
    latex_table = results_df.pivot(index='model', columns='phone', values='accuracy').round(4).to_latex()
    with open(os.path.join(out_path, 'classification_summary_table.tex'), 'w') as f:
        f.write(latex_table)

    print("\nAll models cross-validated. Summary saved to classification_summary.csv and LaTeX table exported.")

if __name__ == '__main__':
    train_models(meta_path=META_COLORS)
