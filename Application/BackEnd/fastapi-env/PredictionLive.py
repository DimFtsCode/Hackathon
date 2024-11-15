from pymongo import MongoClient
from datetime import datetime
from MountainsCycle import MountainsCycle  # Εισαγωγή της MountainsCycle
import pandas as pd
import numpy as np
import xgboost as xgb



class PredictionLive:
    def __init__(self, mongo_uri, api_key):
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client["Weather"]
        self.predictions_collection = self.db["PredictionLive"]
        self.mountains_cycle = MountainsCycle(api_key)
        print("PredictionLive: Initialized and connected to MongoDB successfully.")

        model_path = r"D:\desktop\Hackathon\Project\DimiScripts\Models\xgboost_fire_model.json"        
        # Φόρτωση του XGBoost μοντέλου
        self.model = xgb.Booster()
        self.model.load_model(model_path)
        
        print("PredictionLive: Initialized and connected to MongoDB successfully.")

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
        return predictions
    
    def fetch_and_process(self):
        """
        Λήψη δεδομένων από την MountainsCycle, μετασχηματισμός, πρόβλεψη και αποθήκευση στη MongoDB.
        """
        # Λήψη δεδομένων από την MountainsCycle
        weather_data = self.mountains_cycle.fetch_all_weather_data()

        # Προσθήκη επιπλέον πεδίων στο DataFrame για αποθήκευση
        df_original = pd.DataFrame(weather_data)  # Διατήρηση των πρωτότυπων πεδίων όπως 'name', 'date', 'time', 'radius_km'

        # Μετατροπή δεδομένων
        transformed_data = self.transform_data(weather_data)
        
        # Προσθέστε το πεδίο wind_dir στη σωστή μορφή για το prediction
        transformed_data = transformed_data.rename(columns={"wind_dir_degrees": "wind_dir"})

        # Εκτέλεση πρόβλεψης
        predictions = self.predict(transformed_data)

        # Προσθήκη των προβλέψεων και των επιπλέον πεδίων στα δεδομένα καιρού
        transformed_data['prediction'] = predictions
        transformed_data['name'] = df_original['name']
        transformed_data['date'] = df_original['date']
        transformed_data['time'] = df_original['time']
        transformed_data['radius_km'] = df_original['radius_km']

        # Αναδιάταξη των στηλών στη σωστή σειρά για αποθήκευση
        transformed_data = transformed_data[
            ['name', 'date', 'time', 'latitude', 'longitude', 'radius_km', 'temperature', 'wind_speed', 'wind_dir',
            'humidity', 'visibility', 'day_cos', 'day_sin', 'hour_cos', 'hour_sin', 'prediction']
        ]

        # Μετατροπή σε λίστα από dictionaries για αποθήκευση στη MongoDB
        prediction_data = transformed_data.to_dict(orient='records')

        # Αποθήκευση των αποτελεσμάτων στη MongoDB
        if prediction_data:
            self.predictions_collection.insert_many(prediction_data)
            print(f"[{datetime.now()}] Predictions with name, date, time, and radius_km saved to MongoDB.")
