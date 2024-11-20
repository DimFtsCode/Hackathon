import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import os

def load_data(data_path):
    """Φορτώνει τα δεδομένα από το καθορισμένο αρχείο και προετοιμάζει τα χαρακτηριστικά και τις ετικέτες."""
    df = pd.read_csv(data_path)
    df = df.drop(columns=['date', 'time'])  # Αφαίρεση των μη αναγκαίων στηλών
    X = df.drop(columns=['fire'])
    y = df['fire']
    return X, y

def split_data(X, y, test_size=0.2, random_state=42):
    """Διαχωρίζει τα δεδομένα σε σύνολα εκπαίδευσης και δοκιμών."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def prepare_dmatrix(X_train, X_test, y_train, y_test):
    """Μετατρέπει τα δεδομένα σε DMatrix, που χρησιμοποιείται από το XGBoost."""
    dtrain = xgb.DMatrix(X_train.drop(columns=['name']), label=y_train)
    dtest = xgb.DMatrix(X_test.drop(columns=['name']), label=y_test)
    return dtrain, dtest

def calculate_scale_pos_weight(y):
    """Υπολογίζει το scale_pos_weight για αντιστάθμιση της ανισορροπίας στις κλάσεις."""
    return len(y[y == 0]) / len(y[y == 1])

def train_model(dtrain, params, num_round=100):
    """Εκπαιδεύει το XGBoost μοντέλο με cross-validation και επιστρέφει το καλύτερο μοντέλο."""
    cv_results = xgb.cv(
        params,
        dtrain,
        num_boost_round=num_round,
        nfold=5,
        early_stopping_rounds=10,
        metrics="logloss",
        as_pandas=True,
        seed=42
    )
    best_num_round = cv_results['test-logloss-mean'].idxmin()
    model = xgb.train(params, dtrain, best_num_round)
    return model

def save_model(model, model_path):
    """Αποθηκεύει το εκπαιδευμένο μοντέλο σε αρχείο."""
    model.save_model(model_path)
    print(f"Model saved to {model_path}")

def evaluate_model(model, dtest, y_test, threshold=0.8):
    """Αξιολογεί το μοντέλο χρησιμοποιώντας διάφορα μέτρα απόδοσης."""
    preds = model.predict(dtest)
    predictions = [1 if p > threshold else 0 for p in preds]

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    cm = confusion_matrix(y_test, predictions)

    return accuracy, precision, recall, f1, cm

def main():
    # Διαδρομή δεδομένων και αρχείου μοντέλου
    data_path = os.path.join(".", "Dimiscripts", "Datasets", "train_data.csv")
    model_path = os.path.join(".", "Dimiscripts", "Models", "xgboost_fire_model_demo.json")

    # Φόρτωση και προετοιμασία δεδομένων
    X, y = load_data(data_path)
    X_train, X_test, y_train, y_test = split_data(X, y)
    dtrain, dtest = prepare_dmatrix(X_train, X_test, y_train, y_test)
    scale_pos_weight = calculate_scale_pos_weight(y)

    # Ορισμός υπερπαραμέτρων
    params = {
        'objective': 'binary:logistic',
        'max_depth': 5,
        'eta': 0.1,
        'eval_metric': 'logloss',
        'scale_pos_weight': scale_pos_weight
    }

    # Εκπαίδευση του μοντέλου
    model = train_model(dtrain, params)
    save_model(model, model_path)

    # Αξιολόγηση του μοντέλου
    accuracy, precision, recall, f1, cm = evaluate_model(model, dtest, y_test)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)
    print("Confusion Matrix:\n", cm)

# Εκτέλεση του κύριου προγράμματος
if __name__ == "__main__":
    main()
