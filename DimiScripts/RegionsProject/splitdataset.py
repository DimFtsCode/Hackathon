import pandas as pd
import os

# Διαδρομή του αρχείου δεδομένων
data_path = os.path.join(".", "GiorgosScripts", "Final_datasets_with_fire", "combined_with_cyclic_features.csv")

# Φόρτωση δεδομένων
df = pd.read_csv(data_path)

# Μετατροπή της στήλης 'date' σε μορφή datetime
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Ορισμός της ημερομηνίας ορίου
cutoff_date = pd.Timestamp('2024-04-30')

# Δημιουργία δύο DataFrames, ένα πριν και ένα μετά την ημερομηνία ορίου
df_train = df[df['date'] <= cutoff_date]
df_test = df[df['date'] > cutoff_date]

# Αποθήκευση των DataFrames σε νέα αρχεία CSV
train_path = os.path.join(".", "DimiScripts", "Datasets", "train_data.csv")
test_path = os.path.join(".", "DimiScripts", "Datasets", "test_data.csv")

df_train.to_csv(train_path, index=False)
df_test.to_csv(test_path, index=False)

print(f"Train data saved to {train_path}")
print(f"Test data saved to {test_path}")
