import pandas as pd
import numpy as np

# Διαδρομή του αρχείου εισόδου και του αρχείου εξόδου
input_path = r'D:\desktop\Hackathon\Project\GiorgosScripts\Final_datasets_with_fire\combined_sorted_by_day_and_time.csv'
output_path = r'D:\desktop\Hackathon\Project\GiorgosScripts\Final_datasets_with_fire\combined_with_cyclic_features.csv'

# Φόρτωση δεδομένων σε DataFrame
df = pd.read_csv(input_path)

# Μετατροπή της στήλης `date` σε τύπο ημερομηνίας
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Κυκλική αναπαράσταση για την ημερομηνία
df['day_of_year'] = df['date'].dt.dayofyear
df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)

# Μετατροπή `time` στη σωστή αναπαράσταση της ώρας
time_to_hour = {0: 0, 300: 3, 600: 6, 900: 9, 1200: 12, 1500: 15, 1800: 18, 2100: 21}
df['hour'] = df['time'].map(time_to_hour)

# Κυκλική αναπαράσταση για την ώρα
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)

# Αφαίρεση προσωρινών στηλών που δεν χρειάζονται πλέον
df = df.drop(columns=['day_of_year', 'hour'])

# Αποθήκευση του ενημερωμένου DataFrame σε νέο αρχείο CSV
df.to_csv(output_path, index=False)

print("Το αρχείο δημιουργήθηκε επιτυχώς στη διαδρομή:", output_path)
