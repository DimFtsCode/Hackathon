import os
import pandas as pd
import numpy as np
import re

# Ο φάκελος που περιέχει όλα τα αρχεία CSV
folder_path = r'D:\desktop\Hackathon\Project\GiorgosScripts\Final_datasets_with_fire'

# Δημιουργία κενής λίστας για την αποθήκευση όλων των DataFrames
all_dataframes = []

# Διάβασε όλα τα αρχεία CSV στον φάκελο
for file_name in os.listdir(folder_path):
    if file_name.endswith('_final_dataset.csv'):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        all_dataframes.append(df)

# Συνένωση όλων των DataFrames σε ένα
combined_df = pd.concat(all_dataframes)

# Μετατροπή των στηλών 'date' και 'time' σε strings
combined_df['date'] = combined_df['date'].astype(str)
combined_df['time'] = combined_df['time'].astype(str)

# Έλεγχος και διόρθωση της στήλης 'time' σε περίπτωση που υπάρχουν μη έγκυρες τιμές
def fix_time_format(time_str):
    if re.match(r'^\d{1,2}:\d{2}:\d{2}$', time_str):  # Ελέγχει αν έχει τη μορφή HH:MM:SS
        return time_str
    elif time_str.isdigit():  # Εάν είναι σκέτο ψηφίο (π.χ. "3"), το μετατρέπουμε σε "03:00:00"
        return f"{int(time_str):02}:00:00"
    else:
        return "00:00:00"  # Αν δεν μπορεί να αναγνωριστεί, το ορίζουμε σε "00:00:00" για ασφάλεια

combined_df['time'] = combined_df['time'].apply(fix_time_format)

# Συνένωση των στηλών 'date' και 'time' για πλήρη χρονική πληροφορία
combined_df['datetime'] = pd.to_datetime(combined_df['date'] + ' ' + combined_df['time'], errors='coerce')

# Φιλτράρισμα μη έγκυρων ημερομηνιών που απέτυχαν να μετατραπούν σε datetime
combined_df = combined_df.dropna(subset=['datetime'])

# Ταξινόμηση βάσει της στήλης 'datetime'
combined_df = combined_df.sort_values(by='datetime')

# Κυκλική αναπαράσταση για την ημερομηνία
combined_df['day_of_year'] = combined_df['datetime'].dt.dayofyear
combined_df['day_cos'] = np.cos(2 * np.pi * combined_df['day_of_year'] / 365)
combined_df['day_sin'] = np.sin(2 * np.pi * combined_df['day_of_year'] / 365)

# Κυκλική αναπαράσταση για την ώρα
combined_df['hour'] = combined_df['datetime'].dt.hour
combined_df['hour_cos'] = np.cos(2 * np.pi * combined_df['hour'] / 24)
combined_df['hour_sin'] = np.sin(2 * np.pi * combined_df['hour'] / 24)

# Αφαίρεση της προσωρινής στήλης 'datetime' και άλλων που δεν χρειάζονται, αν υπάρχουν
combined_df = combined_df.drop(columns=['datetime', 'day_of_year', 'hour'])

# Αποθήκευση του ενιαίου αρχείου σε νέο CSV
output_path = r'D:\desktop\Hackathon\Project\GiorgosScripts\Final_datasets_with_fire\combined_final_dataset_with_cyclic.csv'
combined_df.to_csv(output_path, index=False)
