from typing import List, Optional
import time
from datetime import datetime,timedelta
import requests
from PredictionTestData import PredictionTestData
import pandas as pd

# Function to call the FastAPI endpoint
def fetch_data_from_fastapi(date, time=None):
    # Define the base URL of the FastAPI server
    base_url = "http://localhost:8000/items"
    
    # Set the parameters for the GET request
    params = {"date": date}
    if time:
        params["time"] = time

    print("test")
    
    # Make the GET request to the FastAPI endpoint
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        print("status ok")
        data = response.json()
        #return data.get("items", [])
        return data
    else:
        # Handle errors if needed
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return []


if __name__ == "__main__":

    predictor = PredictionTestData("mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather")
     # Define the date and time you want to filter by
    date = "2024-06-01"
    timestamp = ["0", "300", "600", "900", "1200", "1500", "1800", "2100"]
    index = 0
    newday = 0

    while True:

        date = datetime.strptime(str(date), "%Y-%m-%d").date()
        date += timedelta(days=newday)
        print(date)
        print("index ", index)
        print("newday ", newday)

        weather_data_list = fetch_data_from_fastapi(date, timestamp[index])  
        print(weather_data_list)
        weather_data_df = pd.DataFrame(weather_data_list)
        print(weather_data_df)

        predictor.fetch_and_process(weather_data_df)



        index = (index+1) % 8
        if (index == 0):
            newday = 1
        else:
            newday = 0
           
        time.sleep(60)

    # Call the FastAPI endpoint
    # items = fetch_data_from_fastapi(date, time)

     # Print the fetched items
    # print("Fetched Items:")
    # for item in items:
    #     print(item)

    
    