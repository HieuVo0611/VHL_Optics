from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

def get_classifiers(n_estimators=100):
    """Return a dictionary of classifiers to train."""
    classifiers = {
        'random_forest': RandomForestClassifier(n_estimators=n_estimators, random_state=42),
        'svm': SVC(kernel='rbf', probability=True),
        'knn': KNeighborsClassifier(n_neighbors=5),
        'mlp': MLPClassifier(
            hidden_layer_sizes=(100,),
            max_iter=1000,
            early_stopping=True,
            validation_fraction=0.1,
            random_state=42
        ),
        'xgboost': XGBClassifier(eval_metric='logloss'),
        'logistic_regression': LogisticRegression(max_iter=1000, solver='lbfgs'),
        'naive_bayes': GaussianNB()
    }
    return classifiers
