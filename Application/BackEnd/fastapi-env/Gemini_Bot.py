from pymongo import MongoClient
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import google.generativeai as palm
import re

# MongoDB configuration
mongo_uri = "mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather"
mongo_client = MongoClient(mongo_uri)

# Access the Weather database and RAG_DATA collection
db = mongo_client["Weather"]
weather_collection = db["RAG_DATA"]

print("Connected to MongoDB successfully.")

# Initialize the embedding model
embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
print("Loaded SentenceTransformer model successfully.")

def get_embedding(text):
    if not text.strip():
        print("Attempted to get embedding for empty text.")
        return []
    embedding = embedding_model.encode(text)
    return embedding.tolist()


def extract_date_and_locations(query):
    """
    Extracts date and locations from the user query.
    """
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", query)
    date_filter = date_match.group(0) if date_match else None

    # Extract location names (simple example, can be enhanced)
    location_filters = re.findall(r"[A-Za-z]+", query)  # Modify for specific location patterns
    return date_filter, location_filters

def query_results(query):
    """
    Generates an embedding for the query and performs a vector similarity search in MongoDB
    using the Atlas Search feature.
    """
    # Create the query embedding
    query_embedding = get_embedding(query)
    #print(f"Query Embedding: {query_embedding}")

    # Extract date and locations from the query
    date_filter, location_filters = extract_date_and_locations(query)

    # Create filter conditions
    filter_conditions = {}
    if date_filter:
        filter_conditions['date'] = date_filter
    if location_filters:
        filter_conditions['name'] = {'$in': location_filters}
    print(f"Filter Conditions: {filter_conditions}")

    # Vector similarity search pipeline
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

    # Execute the aggregation pipeline
    results_cursor = db.Hackathon.aggregate(pipeline)
    
    # Convert the cursor to a list
    results = list(results_cursor)
    print(f"Query Results: {results}")
    return results

def format_results(results):
    """
    Converts MongoDB query results into a human-readable text format for the LLM.
    """
    formatted_results = []
    for result in results:
        formatted_results.append(
            f"Location: {result.get('name', 'Unknown')}\n"
            f"Date: {result.get('date', 'Unknown')}\n"
            f"Time: {result.get('time', 'Unknown')}\n"
            f"Temperature: {result.get('temperature', 'N/A')}°C\n"
            f"Wind Speed: {result.get('wind_speed', 'N/A')} km/h\n"
            f"Wind Direction: {result.get('wind_dir', 'N/A')}°\n"
            f"Humidity: {result.get('humidity', 'N/A')}%\n"
            f"Visibility: {result.get('visibility', 'N/A')} km\n"
            f"Fire: {'Yes' if result.get('fire', 0) == 1 else 'No'}"
        )
    return "\n\n".join(formatted_results)


def generate_text(user_message, model):
    """
    Combines user query with retrieved results and uses the Gemini API to generate a response.
    """
    results = query_results(user_message)
    print(f"Query Results: {results}")

    # Format results for LLM
    results_str = format_results(results)

    prompt = (
        f"You are a helpful assistant in a government website that helps citizens take precautions against wildfires. "
        f"A user can ask you what measures to take in case of a wildfire or to prevent one. "
        f"They can ask you questions about weather conditions of specific locations and dates. "
        f"If the query does not contain a location from the results, do not use the results, just provide the answer."
        f"If the query is irrelevant to the website's purpose, advise the user to ask a different question. "
        f"Provide the answer in a user-friendly markdown format. Do not create markdown tables."
        f"QUERY: {user_message}\n"
        f"RELEVANT DATA:\n{results_str}\n"
        f"ANSWER:"
    )
    
    print(results_str)
    response = model.generate_content(prompt)
    return response.text

def initialize_llm():
    # Set your Gemini API key
    os.environ['GOOGLE_API_KEY'] = 'AIzaSyCdF0puCdMW-s-9WmCNdSY4eLanHO9yJWQ'  # replace with your own key
    palm.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = palm.GenerativeModel('gemini-1.5-flash')
    return model

def llm_response(model, user_message):
    try:
        answer = generate_text(user_message, model)
        return answer
    except Exception as e:
        print(f"Error generating text: {e}")
        return "I'm sorry, I couldn't generate a response."