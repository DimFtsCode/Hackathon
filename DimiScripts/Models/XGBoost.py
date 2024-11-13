import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import os

# Διαδρομή του αρχείου δεδομένων
data_path = os.path.join(".", "Dimiscripts", "Datasets", "train_data.csv")

# Φόρτωση δεδομένων
df = pd.read_csv(data_path)

# Αφαίρεση των μη αναγκαίων στηλών 'date' και 'time' (διατηρούμε το 'name')
df = df.drop(columns=['date', 'time'])

# Υποθέτουμε ότι η στήλη 'fire' είναι η στήλη-στόχος και οι υπόλοιπες είναι τα χαρακτηριστικά
# Χωρισμός των χαρακτηριστικών και των στόχων
X = df.drop(columns=['fire'])
y = df['fire']

# Υπολογισμός του λόγου κατηγοριών
ratio = len(y[y == 0]) / len(y[y == 1])

# Διαχωρισμός δεδομένων σε σύνολα εκπαίδευσης και δοκιμών
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Μετατροπή των δεδομένων σε DMatrix
dtrain = xgb.DMatrix(X_train.drop(columns=['name']), label=y_train)
dtest = xgb.DMatrix(X_test.drop(columns=['name']), label=y_test)

# Ορισμός υπερπαραμέτρων με scale_pos_weight
params = {
    'objective': 'binary:logistic',  # Αλλάζουμε σε classification
    'max_depth': 5,
    'eta': 0.1,
    'eval_metric': 'logloss',  # Χρησιμοποιούμε log loss για ταξινόμηση
    'scale_pos_weight': ratio  # Προσθήκη της βαρύτητας
}

# Εκπαίδευση του μοντέλου με cross-validation
num_round = 100
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

# Εκπαίδευση του τελικού μοντέλου με τον καλύτερο αριθμό γύρων από το cross-validation
best_num_round = cv_results['test-logloss-mean'].idxmin()
bst = xgb.train(params, dtrain, best_num_round)

# Αποθήκευση του μοντέλου σε αρχείο
model_path = os.path.join(".", "Dimiscripts", "Models", "xgboost_fire_model.json")
bst.save_model(model_path)
print(f"Model saved to {model_path}")

# Πρόβλεψη και υπολογισμός ακρίβειας
preds = bst.predict(dtest)
predictions = [1 if p > 0.8 else 0 for p in preds]  # Μετατροπή σε κατηγορίες 0/1

# Υπολογισμός μέτρων απόδοσης
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

# Εμφάνιση του Confusion Matrix
cm = confusion_matrix(y_test, predictions)
print("Confusion Matrix:\n", cm)
