from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import re

client=OpenAI(api_key="") 
mongo_uri = "mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather"
mongo_client = MongoClient(mongo_uri)


# Επιλογή βάσης δεδομένων και συλλογής
db = mongo_client["Weather"]
weather_collection = db["Hackathon"]

print("Connected to MongoDB successfully.")

# Φόρτωση του SentenceTransformer μοντέλου
embedding_model = SentenceTransformer("thenlper/gte-large")
print("Loaded SentenceTransformer model successfully.")


# Συνάρτηση για τη δημιουργία embedding χρησιμοποιώντας το SentenceTransformer
def get_embedding(text):
    if not text.strip():
        print("Attempted to get embedding for empty text.")
        return []
    
    # Χρήση της μεθόδου encode για τη δημιουργία του embedding
    embedding = embedding_model.encode(text)
    return embedding.tolist()


# Συνάρτηση για μετατροπή εγγραφής σε περιγραφικό κείμενο
def create_text_from_record(record):
    text = (f"Location: {record.get('name', 'Unknown')}, Latitude: {record.get('latitude', 'N/A')}, "
            f"Longitude: {record.get('longitude', 'N/A')}, Date: {record.get('date', 'N/A')}, "
            f"Time: {record.get('time', 'N/A')}, Temperature: {record.get('temperature', 'N/A')}°C, "
            f"Wind Speed: {record.get('wind_speed', 'N/A')} kph, Wind Direction: {record.get('wind_dir', 'N/A')}, "
            f"Humidity: {record.get('humidity', 'N/A')}%, Visibility: {record.get('visibility', 'N/A')} km")
    return text


# Δημιουργία και αποθήκευση embeddings για κάθε εγγραφή στη συλλογή
def generate_and_store_embeddings():
    documents = weather_collection.find()
    
    for doc in documents:
        # Δημιουργία περιγραφικού κειμένου από την εγγραφή
        text = create_text_from_record(doc)
        
        # Δημιουργία embedding για το κείμενο
        embedding = get_embedding(text)
        
        # Αποθήκευση του embedding στην εγγραφή
        weather_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"embedding": embedding.tolist()}}
        )
        print(f"Stored embedding for document with _id: {doc['_id']}")

# Κλήση της συνάρτησης για τη δημιουργία και αποθήκευση embeddings
generate_and_store_embeddings()




def extract_date_and_locations(query):
    # Εξαγωγή ημερομηνίας με χρήση regex
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", query)
    date = date_match.group(0) if date_match else None

    # Λίστα γνωστών τοποθεσιών (ενημέρωσέ την με τις δικές σου τοποθεσίες)
    locations = ["Anthousa", "Dioni", "OtherLocation"]  # Προσάρμοσε αυτή τη λίστα
    found_locations = []
    for loc in locations:
        if loc.lower() in query.lower():
            found_locations.append(loc)

    return date, found_locations

def query_results(query):
    """
    Δημιουργεί embedding για την ερώτηση και εκτελεί αναζήτηση στη MongoDB
    για τις πιο σχετικές εγγραφές, χρησιμοποιώντας τον δείκτη `vector_index`
    και φίλτρα για ημερομηνία και τοποθεσία.
    """
    # Δημιουργία embedding της ερώτησης
    query_embedding = get_embedding(query)

    # Εξαγωγή ημερομηνίας και τοποθεσίας από την ερώτηση
    date_filter, location_filters = extract_date_and_locations(query)

    # Δημιουργία φίλτρου για την αναζήτηση
    filter_conditions = {}
    if date_filter:
        filter_conditions['date'] = date_filter
    if location_filters:
        # Χρήση του τελεστή $in για να συμπεριληφθούν όλες οι τοποθεσίες
        filter_conditions['name'] = {'$in': location_filters}

    # Εκτέλεση αναζήτησης vector similarity με φίλτρα
    pipeline = [
        {
            
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 150,
                "limit": 5
            }
        }
    ]

    # Εάν υπάρχουν φίλτρα, τα προσθέτουμε στο pipeline
    if filter_conditions:
        pipeline[0]["$vectorSearch"]["filter"] = filter_conditions

    results = db.Hackathon.aggregate(pipeline)
    return list(results)

# Συνάρτηση για τη διαμόρφωση των αποτελεσμάτων της αναζήτησης σε κείμενο
def get_search_results(query):
    """
    Λαμβάνει τα πιο σχετικά αποτελέσματα από την MongoDB και δημιουργεί
    μια περιγραφή για το LLM.
    """
    results = query_results(query)
    
    # Δημιουργία περιγραφικού κειμένου για τα αποτελέσματα
    search_results = ""
    for result in results:
        search_results += create_text_from_record(result) + "\n"
    return search_results, results


# Συνάρτηση για την ανάλυση των καιρικών συνθηκών και την παραγωγή οδηγιών
def analyze_weather_conditions(results):
    """
    Αναλύει τα αποτελέσματα και εντοπίζει επικίνδυνες συνθήκες.
    Επιστρέφει μια λίστα με οδηγίες.
    """
    instructions = []
    for result in results:
        temperature = result.get('temperature', 0)
        humidity = result.get('humidity', 100)
        wind_speed = result.get('wind_speed', 0)
        wind_dir = result.get('wind_dir', 'N/A')
        location = result.get('name', 'Unknown')
        date = result.get('date', 'N/A')
        time = result.get('time', 'N/A')

        # Εντοπισμός επικίνδυνων συνθηκών
        if temperature > 30 and humidity < 20:
            instruction = f"High risk of fire in {location} on {date} at {time}. "
            if wind_dir in ['NE', 'ENE', 'NNE']:
                instruction += f"Recommend sending drone to the northeast direction due to {wind_dir} winds."
            elif wind_dir in ['E', 'SE', 'SSE']:
                instruction += f"Recommend sending drone to the southeast direction due to {wind_dir} winds."
            # Προσθέστε επιπλέον συνθήκες για άλλες κατευθύνσεις ανέμου
            else:
                instruction += f"Recommend monitoring the area closely."
            instructions.append(instruction)
    return instructions


# Συνάρτηση για την παραγωγή απάντησης με χρήση του OpenAI API
def generate_text(query):
    """
    Συνδυάζει την ερώτηση του χρήστη με τα αποτελέσματα της αναζήτησης,
    αναλύει τις συνθήκες και χρησιμοποιεί το OpenAI API για να παράγει την τελική απάντηση.
    """
    # Λήψη των αποτελεσμάτων της αναζήτησης και των ακατέργαστων δεδομένων
    source_information, results = get_search_results(query)

    # Ανάλυση των συνθηκών για παραγωγή οδηγιών
    instructions = analyze_weather_conditions(results)

    # Δημιουργία του περιεχομένου για το LLM
    if source_information.strip():
        combined_information = (
            f"Question: {query}\n"
            f"Using the following information, answer the question and provide any necessary fire prevention instructions:\n"
            f"{source_information}\n"
        )
        if instructions:
            combined_information += "\nDetected conditions:\n"
            for instr in instructions:
                combined_information += f"- {instr}\n"
    else:
        combined_information = f"Question: {query}\nI couldn't find specific data matching your query."

    # Κλήση του OpenAI API με χρήση ChatCompletion
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that provides precise weather information. "
                    "When you detect conditions that indicate a high risk of fire (e.g., temperature above 30°C, humidity below 20%, "
                    "or specific wind directions), you should provide specific fire prevention instructions, such as recommending drone surveillance "
                    "in the direction of the wind."
                )
            },
            {"role": "user", "content": combined_information}
        ],
        max_tokens=300,
        temperature=0.7
    )

    answer = response.choices[0].message.content.strip()
    return answer


# Παράδειγμα χρήσης
if __name__ == "__main__":
    query = "What locations are covered in the dataset?"
    query = "On 2019-05-01 in which region had we the highest temperature: 'Dioni' or 'Anthousa'?"
    query = "Which locations have high wind levels on 2022-08-05?"
    query = "What are the weather conditions in Dioni on 2019-05-01?"
    query = "What are the fire prevention recommendations for Anthousa on 2021-08-05?"

    answer = generate_text(query)
    print("Απάντηση:")
    print(answer)
    









