from pymongo import MongoClient
from datetime import datetime
from MountainsCycle import MountainsCycle  # Εισαγωγή της MountainsCycle
import pandas as pd
import numpy as np
import xgboost as xgb
import pytz  # Για μετατροπή ζώνης ώρας
from prediction_utils import process_prediction_row
import os
import folium


class PredictionLive:
    def __init__(self, mongo_uri, api_key):
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client["Weather"]
        self.predictions_collection = self.db["PredictionLive"]
        self.combine_data = self.db["Combined_data"]
        self.critical_points_collection = self.db["CriticalInfra"]
        self.mountains_cycle = MountainsCycle(api_key)
        print("PredictionLive: Initialized and connected to MongoDB successfully.")

        current_dir = os.path.dirname(__file__)  
        model_path = os.path.join(current_dir, "Models", "xgboost_fire_model.json")       
        # Φόρτωση του XGBoost μοντέλου
        self.model = xgb.Booster()
        self.model.load_model(model_path)
        
        
    def transform_data(self, data):
        """
        Μετατρέπει τα δεδομένα σε μορφή έτοιμη για επεξεργασία (με κυκλική αναπαράσταση και μετατροπή κατεύθυνσης ανέμου).
        :param data: Λίστα από dictionaries με δεδομένα καιρού.
        :return: DataFrame με μετασχηματισμένα δεδομένα.
        """
        # Δημιουργία DataFrame
        df = pd.DataFrame(data)

        # Μετατροπή κατεύθυνσης ανέμου σε μοίρες
        wind_translation = {
            "N": 360, "S": 180, "E": 90, "W": 270, 
            "NW": 315, "NE": 45, "SE": 135, "SW": 225,
            "WNW": 315, "WSW": 225, "NNW": 335, "NNE": 25,
            "ENE": 65, "ESE": 115, "SSE": 155, "SSW": 205
        }
        df['wind_dir_degrees'] = df['wind_dir'].map(wind_translation)

        # Μετατροπή ημερομηνίας σε κυκλική αναπαράσταση
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df['day_of_year'] = df['date'].dt.dayofyear
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)

        # Μετατροπή `time` σε κυκλική αναπαράσταση ώρας
        df['hour'] = pd.to_datetime(df['time'], format='%H:%M').dt.hour
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)

        # Επιλογή μόνο των στηλών που χρειάζεται το μοντέλο για πρόβλεψη
        df = df[['latitude', 'longitude', 'temperature', 'wind_speed', 'wind_dir_degrees', 
                 'day_cos', 'day_sin', 'hour_cos', 'hour_sin', 'humidity', 'visibility']]
        
        return df
    
    def convert_utc_to_local(self, time_str, date_str):
        """
        Μετατρέπει UTC ώρα σε τοπική ώρα με βάση την ημερομηνία.
        :param time_str: Η ώρα σε μορφή 'HH:MM'.
        :param date_str: Η ημερομηνία σε μορφή 'YYYY-MM-DD'.
        :return: Τοπική ώρα σε μορφή 'HH:MM'.
        """
        # Συνδυασμός ημερομηνίας και ώρας
        utc = pytz.utc
        local_tz = pytz.timezone("Europe/Athens")

        # Μετατροπή σε datetime αντικείμενο
        utc_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=utc)

        # Μετατροπή σε τοπική ώρα
        local_datetime = utc_datetime.astimezone(local_tz)

        # Επιστροφή μόνο της ώρας σε μορφή 'HH:MM'
        return local_datetime.strftime("%H:%M")


    def predict(self, transformed_data):
        # Ορισμός της σωστής σειράς χαρακτηριστικών όπως αναμένεται από το μοντέλο
        feature_order = [
            'latitude', 'longitude', 'temperature', 'wind_speed', 'wind_dir',
            'humidity', 'visibility', 'day_cos', 'day_sin', 'hour_cos', 'hour_sin'
        ]
        
        # Αναδιατάσσουμε τις στήλες του DataFrame σύμφωνα με το feature_order
        transformed_data = transformed_data[feature_order]
        
        # Μετατροπή του DataFrame σε DMatrix για πρόβλεψη
        dmatrix = xgb.DMatrix(transformed_data)
        predictions = self.model.predict(dmatrix)
        
        # Generate the map
        self.generate_map(transformed_data, predictions)
        
        return predictions
    
    def fetch_and_process(self):
        """
        Λήψη δεδομένων από την MountainsCycle, μετασχηματισμός, πρόβλεψη και αποθήκευση στη MongoDB.
        """
        # Λήψη δεδομένων από την MountainsCycle
        weather_data = self.mountains_cycle.fetch_all_weather_data()

        # Δημιουργία DataFrame με τα αρχικά δεδομένα
        df_original = pd.DataFrame(weather_data)  # Διατήρηση των πρωτότυπων πεδίων όπως 'name', 'date', 'time', 'radius_km'

        # Μετατροπή UTC χρόνου σε τοπική ώρα
        df_original['time'] = df_original.apply(
            lambda row: self.convert_utc_to_local(row['time'], row['date']),
            axis=1
        )

        # Μετατροπή δεδομένων σε μορφή που χρειάζεται το μοντέλο
        transformed_data = self.transform_data(weather_data)

        # Προσθέστε το πεδίο wind_dir στη σωστή μορφή για το prediction
        transformed_data = transformed_data.rename(columns={"wind_dir_degrees": "wind_dir"})

        # Εκτέλεση πρόβλεψης
        predictions = self.predict(transformed_data)

        # Προσθήκη των προβλέψεων και των επιπλέον πεδίων στα δεδομένα
        transformed_data['prediction'] = predictions
        transformed_data['name'] = df_original['name']
        transformed_data['date'] = df_original['date']
        transformed_data['time'] = df_original['time']  # Τοπική ώρα
        transformed_data['radius_km'] = df_original['radius_km']

        # Αναδιάταξη των στηλών στη σωστή σειρά για αποθήκευση
        transformed_data = transformed_data[[
            'name', 'date', 'time', 'latitude', 'longitude', 'radius_km', 'temperature', 
            'wind_speed', 'wind_dir', 'humidity', 'visibility', 'day_cos', 'day_sin', 
            'hour_cos', 'hour_sin', 'prediction'
        ]]

        # Μετατροπή σε λίστα από dictionaries για επεξεργασία
        prediction_data = transformed_data.to_dict(orient='records')

        # Ορισμός της μεταβλητής all_areas
        all_areas = df_original[['name', 'latitude', 'longitude']].drop_duplicates()

        # κλήση της συνάρτησης process_prediction_row για κάθε γραμμή του DataFrame
        processed_data = []
        for row in prediction_data:
            row = process_prediction_row(row, all_areas, self.critical_points_collection)
            processed_data.append(row)

        # Αφαίρεση των ανεπιθύμητων πεδίων από το processed_data
        for row in processed_data:
            row.pop('day_cos', None)
            row.pop('day_sin', None)
            row.pop('hour_cos', None)
            row.pop('hour_sin', None)
            row.pop('radius_km', None)

        # Αποθήκευση των αποτελεσμάτων στη MongoDB
        if processed_data:
            self.predictions_collection.insert_many(processed_data)
            print(f"[{datetime.now()}] Predictions with additional data saved to MongoDB.")

    def generate_map(self, data, predictions):
        
        updated_areas = [
            ("Anthousa", (38.025, 23.876), 1.4025986048164334),
            ("Melissia", (38.050, 23.833), 0.8992058199184515),
            ("Vrilissia", (38.034, 23.830), 0.8992058199184515),
            ("Kifisia", (38.074, 23.811), 1.4691849631144436),
            ("Nea Erythraia", (38.100, 23.817), 1.1761135742986502),
            ("Ekali", (38.117, 23.833), 1.1761135742986502),
            ("Rapentosa", (38.093, 23.904), 1.6979075742179193),
            ("Aigeirouses", (38.070, 23.159), 8),
            ("Rodopoli", (38.117, 23.880), 1.6979075742179193),
            ("Vothon", (38.170, 23.883), 2.5125866368807515),
            ("Grammatiko", (38.203, 23.965), 2.7812470716125284),
            ("Kato Soulion", (38.168, 24.016), 2.4624335228499525),
            ("Marathonas", (38.153, 23.963), 2.4624335228499525),
            ("Ntaou Penteli", (38.041, 23.945), 1.0097431650920101),
            ("Dioni", (38.023, 23.933), 1.096344526615976),
            ("Kallitechnoupoli", (38.026, 23.958), 1.0097431650920101),
            ("Ntrafi", (38.024, 23.908), 1.096344526615976),
            ("Parnis", (38.150, 23.740), 2.4169729483303666),
            ("Acharnes", (38.080, 23.730), 1.3129068926495644),
            ("Ano Liosia", (38.080, 23.700), 1.3129068926495644),
            ("Fyli", (38.100, 23.660), 2.073642211536794),
            ("Aspropyrgos", (38.060, 23.590), 3.7855574971756876),
            ("Skourta", (38.210, 23.550), 4.5084400164592005),
            ("Moni Osiou Meletiou", (38.190, 23.450), 4.5084400164592005),
            ("Avlonas", (38.250, 23.690), 4.9304627840362025),
            ("Varympompi", (38.120, 23.780), 1.9637351988491942),
            ("Afidnes", (38.200, 23.840), 2.1845824632344217),
            ("Agia Triada", (38.200, 23.790), 1.7241773367135118),
            ("Malakasa", (38.230, 23.800), 1.7241773367135118),
        ]
    
        data["prediction"] = predictions 
        sorted_data = data.sort_values(by=["latitude", "longitude"])
        sorted_areas = sorted(updated_areas, key=lambda x: (x[1][0], x[1][1]))
        updated_list = [(t[0], t[1], t[2], sorted_data['prediction'].iloc[i]) for i, t in enumerate(sorted_areas)]

        center_lat, center_lon = 38.1, 23.8  # Rough center for Athens
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        # Add each area as a circle on the map
        for name, (lat, lon), radius, prediction in updated_list:  
            color = get_color(prediction)  
            folium.Circle(
                location=(lat, lon),
                radius=radius * 1000,  # Convert radius from km to meters
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.3,
                popup=name
            ).add_to(m)

        # Save the map to an HTML file
        current_dir = os.path.dirname(__file__)  # Φάκελος που περιέχει το τρέχον script
        save_path = os.path.join(current_dir, '..','..', 'Frontend', 'hackinterface', 'public', 'map_colored.html')

        # Αποθήκευση χάρτη
        m.save(save_path)
        print("Map saved!")
            
#print(updated_areas)
def get_color(prediction):
    if 0 <= prediction <= 0.39:
        return 'blue'
    elif 0.4 <= prediction <= 0.79:
        return 'yellow'
    elif 0.8 <= prediction <= 1:
        return 'red'
    else:
        return 'gray'  # Default color if out of range