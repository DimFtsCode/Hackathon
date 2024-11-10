from transformers import AutoTokenizer, AutoModel
import torch
from pymongo import MongoClient

# Σύνδεση με MongoDB χρησιμοποιώντας το URI
uri = "mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather"
client = MongoClient(uri)


# Επιλογή βάσης δεδομένων και συλλογής
db = client["Weather"]
weather_collection = db["Hackathon"]

print("Connected to MongoDB successfully.")


# Φορτώνουμε το μοντέλο και τον tokenizer από το Hugging Face
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


# Συνάρτηση για τη δημιουργία embeddings χρησιμοποιώντας PyTorch
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Μέσος όρος των embeddings
    return embeddings[0].numpy()

# Δημιουργία ενός δοκιμαστικού κειμένου και εκτύπωση των embeddings
test_text = "Temperature: 25°C, Humidity: 45%, Wind Speed: 10 kph, Wind Direction: North"
test_embedding = get_embedding(test_text)
print("Embeddings for the test text:")
print(test_embedding)