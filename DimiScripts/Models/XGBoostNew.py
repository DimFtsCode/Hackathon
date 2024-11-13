
import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import os

# Διαδρομή του αρχείου δεδομένων
data_path = os.path.join(".", "Dimiscripts", "Datasets", "train_data.csv")

# Φόρτωση δεδομένων από το αρχείο CSV
df = pd.read_csv(data_path)


# # Φόρτωση δεδομένων
# df = pd.read_csv('/Users/giorgosziakas/Desktop/train_data.csv')
# df.head()


# Interaction feature: fire risk score
df['fire_risk_score'] = df['temperature'] * 0.3 + df['humidity'] * -0.2 + df['wind_speed'] * 0.5

# Geospatial clustering
# coords = df[['latitude', 'longitude']]
# kmeans = KMeans(n_clusters=5, random_state=0).fit(coords)
# df['location_cluster'] = kmeans.labels_

# Drop unnecessary columns
df = df.drop(columns=['date', 'time', 'name'])

# Split features and target
X = df.drop(columns=['fire'])
y = df['fire']

# Handle class imbalance
# Calculate class weights
class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(y), y=y)
weight_0, weight_1 = class_weights[0], class_weights[1]
print(f"Class Weights: 0: {weight_0}, 1: {weight_1}")


# Διαχωρισμός δεδομένων σε σύνολα εκπαίδευσης και δοκιμών
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data (important for tree-based models in some cases)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert data to DMatrix format
dtrain = xgb.DMatrix(X_train_scaled, label=y_train)
dtest = xgb.DMatrix(X_test_scaled, label=y_test)

# Ορισμός υπερπαραμέτρων με scale_pos_weight
params = {
    'objective': 'binary:logistic',  # Αλλάζουμε σε classification
    'max_depth': 5,
    'eta': 0.1,
    'eval_metric': 'logloss',  # Χρησιμοποιούμε log loss για ταξινόμηση
    'scale_pos_weight': weight_1 / weight_0  # Προσθήκη της βαρύτητας
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


# Predictions and Evaluation
preds_train = bst.predict(dtrain)
preds_test = bst.predict(dtest)
train_predictions = [1 if p > 0.8 else 0 for p in preds_train]
test_predictions = [1 if p > 0.8 else 0 for p in preds_test]


# Metrics
print("\nTraining Set Metrics:")
print("Accuracy:", accuracy_score(y_train, train_predictions))
print("Precision:", precision_score(y_train, train_predictions))
print("Recall:", recall_score(y_train, train_predictions))
print("F1 Score:", f1_score(y_train, train_predictions))
print("Classification Report:\n", classification_report(y_train, train_predictions))

print("\nTesting Set Metrics:")
print("Accuracy:", accuracy_score(y_test, test_predictions))
print("Precision:", precision_score(y_test, test_predictions))
print("Recall:", recall_score(y_test, test_predictions))
print("F1 Score:", f1_score(y_test, test_predictions))
print("Classification Report:\n", classification_report(y_test, test_predictions))

# Confusion Matrix
print("\nConfusion Matrix for Testing Set:")
print(confusion_matrix(y_test, test_predictions))