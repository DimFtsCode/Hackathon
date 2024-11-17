import xgboost as xgb
import pandas as pd
import os

# Φόρτωση του αποθηκευμένου μοντέλου
model_path = os.path.join(".", "Dimiscripts", "Models", "xgboost_fire_model.json")
loaded_model = xgb.Booster()
loaded_model.load_model(model_path)

# Διαδρομή του αρχείου test_data
test_data_path = os.path.join(".", "Dimiscripts", "Datasets", "test_data.csv")

# Φόρτωση του test_data
df_test = pd.read_csv(test_data_path)

# Εντοπισμός 50 γραμμών όπου το fire είναι 1
fire_rows = df_test[df_test['fire'] == 1].head(50)

# Εκτύπωση των δεδομένων
print("Δεδομένα με fire=1:")
print(fire_rows)

# Αφαίρεση των μη αναγκαίων στηλών όπως 'name', 'date', και 'time' (αν υπάρχουν)
fire_rows_for_prediction = fire_rows.drop(columns=['name', 'date', 'time', 'fire'], errors='ignore')

# Μετατροπή των δεδομένων σε DMatrix
dtest_fire = xgb.DMatrix(fire_rows_for_prediction)

# Πρόβλεψη με το μοντέλο (πιθανότητες)
fire_probs = loaded_model.predict(dtest_fire)

# Εκτύπωση των αποτελεσμάτων πρόβλεψης με πιθανότητες
print("\nΑποτελέσματα πρόβλεψης με πιθανότητες:")
for index, (data, prob) in enumerate(zip(fire_rows.values, fire_probs)):
    print(f"Περιοχή {index+1} - Δεδομένα: {data} - Πιθανότητα φωτιάς: {prob:.2f}")
