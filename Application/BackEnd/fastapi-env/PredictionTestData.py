from pymongo import MongoClient
from datetime import datetime
#from MountainsCycle import MountainsCycle  # Εισαγωγή της MountainsCycle
import pandas as pd
import numpy as np
import xgboost as xgb
import pytz  # Για μετατροπή ζώνης ώρας
import csv
from prediction_utils import process_prediction_row

# Function to read a CSV file and convert it to a list of tuples
# def csv_to_list_of_tuples(filename):
#     list_of_tuples = []
    
#     # Open the CSV file
#     with open(filename, mode='r') as file:
#         # Create a CSV reader object
#         csv_reader = csv.reader(file)
        
#         # Skip the header (first row) if there is one
#         next(csv_reader)
        
#         # Read each row and convert it to a tuple, then add to the list
#         for row in csv_reader:
#             # Convert latitude, longitude, and area to appropriate types
#             name = row[0]
#             latitude = float(row[1])
#             longitude = float(row[2])
#             date = row[3]
#             time = int(row[4])
            
#             # Append the tuple to the list
#             list_of_tuples.append((category, latitude, longitude, description, area))
    
#     return list_of_tuples


class PredictionTestData:
    def __init__(self, mongo_uri):
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client["Weather"]
        self.predictions_collection = self.db["PredictionTestData"]
        self.critical_points_collection = self.db["CriticalInfra"]

        # self.mountains_cycle = MountainsCycle(api_key)
        print("PredictionTestData: Initialized and connected to MongoDB successfully.")

        model_path = "C:/Users/ziziz/Desktop/Hackathon/DimiScripts/Models/xgboost_fire_model_demo.json"      
        # Φόρτωση του XGBoost μοντέλου
        self.model = xgb.Booster()
        self.model.load_model(model_path)
        
        print("PredictionTestData: Initialized and connected to MongoDB successfully.")

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
        return predictions
    
    def fetch_and_process(self, transformed_data):
       
        predictions = self.predict(transformed_data)

        # Προσθήκη των προβλέψεων και των επιπλέον πεδίων στα δεδομένα
        transformed_data['prediction'] = predictions
        transformed_data['name'] = transformed_data['name']
        transformed_data['date'] = transformed_data['date']
        transformed_data['time'] = transformed_data['time']  # Τοπική ώρα
        # transformed_data['radius_km'] = transformed_data['radius_km']

        # Αναδιάταξη των στηλών στη σωστή σειρά για αποθήκευση
        transformed_data = transformed_data[
            ['name', 'date', 'time', 'latitude', 'longitude', 'temperature', 'wind_speed', 'wind_dir',
            'humidity', 'visibility', 'day_cos', 'day_sin', 'hour_cos', 'hour_sin', 'prediction']
        ]
        
        # transformed_data['time'] = transformed_data.apply(
        #     lambda row: self.convert_utc_to_local(row['time'], row['date']),
        #     axis=1
        # )

        # Μετατροπή σε λίστα από dictionaries για αποθήκευση στη MongoDB
        prediction_data = transformed_data.to_dict(orient='records')
        
        all_areas = transformed_data[['name', 'latitude', 'longitude']].drop_duplicates()

    
        # κλήση της συνάρτησης process_prediction_row για κάθε γραμμή του DataFrame
        processed_data = []
        for row in prediction_data:
            row = process_prediction_row(row, all_areas, self.critical_points_collection)
            processed_data.append(row)
        
        # Αποθήκευση των αποτελεσμάτων στη MongoDB
        if processed_data:
            self.predictions_collection.insert_many(processed_data)
            print(f"[{datetime.now()}] Predictions with additional data saved to MongoDB.")

