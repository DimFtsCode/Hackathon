import os
import pandas as pd

# Ο φάκελος που περιέχει όλα τα αρχεία CSV
folder_path = r'D:\desktop\Hackathon\Project\GiorgosScripts\Final_datasets_with_fire'

# Δημιουργία κενής λίστας για την αποθήκευση όλων των DataFrames
all_dataframes = []

# Προκαθορισμένη σειρά ωρών
time_order = [0, 300, 600, 900, 1200, 1500, 1800, 2100]

# Διάβασε όλα τα αρχεία CSV στον φάκελο
for file_name in os.listdir(folder_path):
    if file_name.endswith('_final_dataset.csv'):
        file_path = os.path.join(folder_path, file_name)
        # Ανάγνωση αρχείου και ορισμός ονομάτων στηλών
        df = pd.read_csv(file_path, header=None)
        df.columns = ['name', 'latitude', 'longitude', 'date', 'time', 'temperature', 'wind_speed', 'wind_dir', 'humidity', 'visibility', 'fire']
        
        # Εξασφάλιση ότι η στήλη `time` έχει αριθμητικές τιμές
        df['time'] = pd.to_numeric(df['time'], errors='coerce')
        
        # Αντικατάσταση των κενών τιμών στη στήλη 'time' με την προκαθορισμένη σειρά
        if df['time'].isnull().any():  # Ελέγχει αν υπάρχουν κενές τιμές
            num_rows = len(df)
            time_values = (time_order * (num_rows // len(time_order))) + time_order[:num_rows % len(time_order)]
            df['time'].fillna(pd.Series(time_values), inplace=True)
        
        all_dataframes.append(df)

# Συνένωση όλων των DataFrames σε ένα
combined_df = pd.concat(all_dataframes, ignore_index=True)

# Μετατροπή της στήλης `date` σε τύπο ημερομηνίας για σωστή ταξινόμηση
combined_df['date'] = pd.to_datetime(combined_df['date'], format='%Y-%m-%d', errors='coerce')

# Αφαίρεση τυχόν μη έγκυρων γραμμών που περιέχουν NaT στη στήλη `date`
combined_df = combined_df.dropna(subset=['date'])

# Καθορισμός σειράς `time` ως κατηγορία για ταξινόμηση
combined_df['time'] = pd.Categorical(combined_df['time'], categories=time_order, ordered=True)

# Ταξινόμηση των δεδομένων κατά `date` και `time`
combined_df = combined_df.sort_values(by=['date', 'time'])

# Αποθήκευση του τελικού αρχείου σε νέο CSV
output_path = r'D:\desktop\Hackathon\Project\GiorgosScripts\Final_datasets_with_fire\combined_sorted_by_day_and_time.csv'
combined_df.to_csv(output_path, index=False)
