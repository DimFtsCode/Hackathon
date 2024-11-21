from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from mongodbendpoints import router as weather_router
from PredictionLive import PredictionLive
from PredictionTestData import PredictionTestData
from Gemini_Bot import initialize_llm, llm_response
import asyncio
from datetime import datetime, timedelta
import pandas as pd

# Δημιουργία εφαρμογής FastAPI
app = FastAPI()

# Σύνδεση με MongoDB
mongo_uri = "mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather"
mongo_client = MongoClient(mongo_uri)
db = mongo_client["Weather"]
weather_collection = db["PredictionLive"]
weather_collection_demo = db["PredictionTestData"]
print("Connected to MongoDB successfully.")

# Middleware για CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Προσθήκη endpoints για MongoDB
app.include_router(weather_router)

# Δημιουργία αντικειμένου PredictionLive
api_key = "23ecd879f082445734dc2066bf821571"
prediction_live = PredictionLive(mongo_uri, api_key)

# Global μεταβλητή για το background task
background_task = None
shutdown_event = False  # Global μεταβλητή για τερματισμό

# Background task για περιοδική ανανέωση δεδομένων
async def fetch_weather_and_predict_periodically():
    """
    Ενημερώνει δεδομένα και προβλέψεις περιοδικά.
    """
    global shutdown_event
    while not shutdown_event:
        print(f"[{datetime.now()}] Fetching and processing weather data...")
        prediction_live.fetch_and_process()
        print(f"[{datetime.now()}] Prediction data updated.")
        try:
            await asyncio.sleep(300)  # Κάθε 5 λεπτά
        except asyncio.CancelledError:
            print("Background task cancelled.")
            break


# Background task για την επεξεργασία TestData
async def fetch_testdata_periodically():
    """
    Ανακτά περιοδικά δεδομένα από τη συλλογή TestData και τα επεξεργάζεται.
    """
    global shutdown_event
    predictor = PredictionTestData(mongo_uri)  # Δημιουργία αντικειμένου predictor
    date = "2024-06-05"
    timestamp = ["0", "300", "600", "900", "1200", "1500", "1800", "2100"]
    index = 0
    newday = 0

    while not shutdown_event:
        try:
            # Ενημέρωση ημερομηνίας
            current_date = datetime.strptime(str(date), "%Y-%m-%d").date()
            current_date += timedelta(days=newday)
            #print(f"Processing date: {current_date}")
            #print(f"Timestamp index: {index}, New day increment: {newday}")

            # Ανάκτηση δεδομένων από MongoDB
            documents = db["TestData"].find({
                "date": str(current_date),
                "time": int(timestamp[index])
            })
            weather_data_list = list(documents)  # Μετατροπή σε λίστα
            #print(f"Fetched data: {weather_data_list}")

            # Μετατροπή δεδομένων σε DataFrame
            if weather_data_list:
                weather_data_df = pd.DataFrame(weather_data_list)
                #print(f"Weather DataFrame: \n{weather_data_df}")

                # Επεξεργασία δεδομένων μέσω του fetch_and_process
                predictor.fetch_and_process(weather_data_df)
            else:
                print("No data fetched for the current timestamp.")

            # Ενημέρωση δεικτών
            index = (index + 1) % len(timestamp)
            newday = 1 if index == 0 else 0

            # Αναμονή πριν τον επόμενο κύκλο
            await asyncio.sleep(60)  # 1 λεπτό
        except Exception as e:
            print(f"An error occurred: {e}")
            break


# Εκκίνηση των background tasks κατά την εκκίνηση της εφαρμογής
@app.on_event("startup")
async def start_background_tasks():
    global background_task, shutdown_event
    shutdown_event = False  # Βεβαιωθείτε ότι το shutdown_event είναι False κατά την εκκίνηση
    # Εκκίνηση των δύο tasks
    background_task_weather = asyncio.create_task(fetch_weather_and_predict_periodically())
    background_task_testdata = asyncio.create_task(fetch_testdata_periodically())
    # Αποθήκευση των tasks για μελλοντική διαχείριση
    global background_tasks
    background_tasks = [background_task_weather, background_task_testdata]
    print("Background tasks started.")


# Τερματισμός όλων των εργασιών κατά το shutdown της εφαρμογής
@app.on_event("shutdown")
async def stop_background_tasks():
    global shutdown_event, background_tasks
    shutdown_event = True
    print("Shutting down...")
    for task in background_tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("Task cancelled successfully.")
    # Τερματισμός σύνδεσης MongoDB
    mongo_client.close()
    print("MongoDB connection closed.")


# Τερματισμός εργασιών κατά το shutdown της εφαρμογής
@app.on_event("shutdown")
async def stop_background_task():
    global shutdown_event, background_task
    shutdown_event = True
    print("Shutting down...")
    if background_task:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            print("Background task cancelled successfully.")
    # Τερματισμός σύνδεσης MongoDB
    mongo_client.close()
    print("MongoDB connection closed.")


# Endpoint για όλα τα predictions
@app.get("/predictions")
def get_all_predictions():
    """
    Επιστρέφει όλα τα δεδομένα από τη συλλογή PredictionLive.
    """
    documents = weather_collection.find()
    predictions = [
        {**doc, "_id": str(doc["_id"])} for doc in documents
    ]  # Μετατροπή ObjectId σε string
    return {"data": predictions}


# Endpoint για τα τελευταία 29 predictions
@app.get("/latest-predictions")
def get_latest_predictions():
    """
    Επιστρέφει τα τελευταία 29 δεδομένα από τη συλλογή PredictionLive.
    """
    documents = weather_collection.find().sort([("date", -1), ("time", -1)]).limit(29)
    predictions = [
        {**doc, "_id": str(doc["_id"])} for doc in documents
    ]  # Μετατροπή ObjectId σε string
    return {"data": predictions}

@app.get("/latest-predictions_demo")
def get_latest_predictions():
    """
    Επιστρέφει τα τελευταία 29 δεδομένα από τη συλλογή PredictionLive.
    """
    documents = weather_collection_demo.find().sort([("date", -1), ("time", -1)]).limit(29)

    predictions = []
    for doc in documents:
        time_value = doc.get("time")  # Assuming time is in HHMM format
        if time_value is not None:
            # Format time to HH:MM
            hours = time_value // 100
            minutes = time_value % 100
            formatted_time = f"{hours:02}:{minutes:02}"
            doc["time"] = formatted_time  # Replace original time with formatted time

    #   Convert ObjectId to string and append to predictions
        predictions.append({**doc, "_id": str(doc["_id"])})

    return {"data": predictions}


# Μοντέλο για εισερχόμενο μήνυμα στο chat
class ChatMessage(BaseModel):
    message: str


#Αρχικοποίηση του LLM
model = initialize_llm()

#Endpoint για την απάντηση του chatbot
@app.post("/api/chat")
async def chat_endpoint(chat_message: ChatMessage):
    """
    Επιστρέφει απάντηση από το LLM βάσει του εισερχόμενου μηνύματος.
    """
    user_message = chat_message.message
    
    # Call your LLM script here and get the response
    bot_reply = llm_response(model, user_message)
    return {"reply": bot_reply}

