from fastapi import FastAPI, BackgroundTasks, Depends
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from mongodbendpoints import router as weather_router
from PredictionLive import PredictionLive  # Εισαγωγή της PredictionLive
from Gemini_Bot import initialize_llm, llm_response
import asyncio
from datetime import datetime  # Ορισμός του datetime για εκτύπωση χρόνου

# Αρχικοποίηση του FastAPI app
app = FastAPI()

# Σύνδεση με τη MongoDB
mongo_uri = "mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather"
mongo_client = MongoClient(mongo_uri)
db = mongo_client["Weather"]
weather_collection = db["PredictionLive"]

print("Connected to MongoDB successfully.")

# Middleware για CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Προσθήκη των MongoDB endpoints
app.include_router(weather_router)


# Δημιουργία αντικειμένου PredictionLive
api_key = "23ecd879f082445734dc2066bf821571"
prediction_live = PredictionLive(mongo_uri, api_key)  # Αφαίρεση του model_path

# Δημιουργία task αντικειμένου για παρακολούθηση του background task
background_task = None

# Background task για περιοδική ανανέωση καιρικών δεδομένων και προβλέψεων
async def fetch_weather_and_predict_periodically():
    while True:
        print(f"[{datetime.now()}] Starting fetch_weather_and_predict_periodically")
        
        # Κλήση της fetch_and_process χωρίς επιστροφή δεδομένων
        prediction_live.fetch_and_process()
        
        print(f"[{datetime.now()}] Prediction data updated.")
        await asyncio.sleep(300)  # 5 λεπτά

# Εκκίνηση του background task κατά την εκκίνηση του appA
@app.on_event("startup")
async def start_weather_fetcher():
    global background_task
    background_task = asyncio.create_task(fetch_weather_and_predict_periodically())

# Διακοπή του background task κατά τον τερματισμό του app
@app.on_event("shutdown")
async def stop_weather_fetcher():
    global background_task
    if background_task:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            print("Background task cancelled successfully")

# Endpoint για ανάκτηση τελευταίων δεδομένων για συγκεκριμένη περιοχή
@app.get("/weather/{region_name}")
def get_latest_weather(region_name: str):
    document = weather_collection.find_one({"name": region_name}, sort=[("date", -1), ("time", -1)])
    if document:
        return document
    return {"error": f"No data found for region {region_name}"}

# Endpoint για εμφάνιση όλων των περιοχών
@app.get("/regions")
def list_regions():
    return prediction_live.mountains_cycle.list_regions()


@app.get("/predictions")
def get_all_predictions():
    """
    Επιστρέφει όλα τα δεδομένα από τη συλλογή PredictionLive.
    """
    documents = weather_collection.find()
    predictions = []
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Μετατροπή του ObjectId σε string για επιστροφή
        predictions.append(doc)
    return {"data": predictions}


@app.get("/latest-predictions")
def get_latest_predictions():
    """
    Επιστρέφει τα τελευταία 29 δεδομένα από τη συλλογή PredictionLive.
    """
    # Ανάκτηση των 29 τελευταίων εγγραφών, ταξινομημένες με βάση την ημερομηνία και ώρα
    documents = weather_collection.find().sort([("date", -1), ("time", -1)]).limit(29)
    
    predictions = []
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Μετατροπή του ObjectId σε string για επιστροφή
        predictions.append(doc)
    
    return {"data": predictions}

# Δημιουργία Pydantic BaseModel για το incoming chat message
class ChatMessage(BaseModel):
    message: str
    
# initialize the LLM
model = initialize_llm()

# Endpoint για την απάντηση του chatbot
@app.post("/api/chat")
async def chat_endpoint(chat_message: ChatMessage):
    user_message = chat_message.message
    # Call your LLM script here and get the response
    bot_reply = await llm_response(model, user_message)
    return {"reply": bot_reply}
