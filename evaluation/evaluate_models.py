import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import DATA_DIR


def evaluate_summary(summary_path=None, output_dir=None):
    if summary_path is None:
        summary_path = os.path.join(DATA_DIR, 'models', 'classification_summary.csv')
    if output_dir is None:
        output_dir = os.path.join('evaluation')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(summary_path)

    # Plot accuracy per model per phone
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='model', y='accuracy', hue='phone')
    plt.title('Accuracy per Model per Phone')
    plt.ylabel('Accuracy')
    plt.xlabel('Model')
    plt.xticks(rotation=45)
    plt.legend(title='Phone')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_per_model.png'))
    plt.close()

    # Plot F1 macro per model per phone if available
    if 'f1_macro' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='model', y='f1_macro', hue='phone')
        plt.title('F1 Macro Score per Model per Phone')
        plt.ylabel('F1 Macro Score')
        plt.xlabel('Model')
        plt.xticks(rotation=45)
        plt.ylim(0.8, 1.01)
        plt.legend(title='Phone')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'f1_macro_per_model.png'))
        plt.close()
        print("F1 macro plot saved.")

    # Average accuracy per model
    avg_acc = df.groupby('model')['accuracy'].mean().reset_index().sort_values(by='accuracy', ascending=False)
    print("\nAverage Accuracy per Model:")
    print(avg_acc.to_string(index=False))
    avg_acc.to_csv(os.path.join(output_dir, 'average_accuracy_summary.csv'), index=False)

    # Average F1 macro per model
    if 'f1_macro' in df.columns:
        avg_f1 = df.groupby('model')['f1_macro'].mean().reset_index().sort_values(by='f1_macro', ascending=False)
        print("\nAverage F1 Macro per Model:")
        print(avg_f1.to_string(index=False))
        avg_f1.to_csv(os.path.join(output_dir, 'average_f1_macro_summary.csv'), index=False)

    print(f"\nEvaluation complete. Results saved in: {output_dir}")


if __name__ == '__main__':
    evaluate_summary()
