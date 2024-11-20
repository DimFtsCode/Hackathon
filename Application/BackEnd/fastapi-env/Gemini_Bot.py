## initialize the LLM
# local way to set the api key
import google.generativeai as palm
import os

# load the database
import pandas as pd
weather_data = pd.read_csv('filtered_weather_data_with_embeddings.csv')
print("Loaded weather data successfully.")


from sentence_transformers import SentenceTransformer


# Initialize the embedding model
embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
print("Loaded SentenceTransformer model successfully.")

def get_embedding(text):
    if not text.strip():
        print("Attempted to get embedding for empty text.")
        return []
    embedding = embedding_model.encode(text)
    return embedding



from sklearn.neighbors import NearestNeighbors
import numpy as np
import ast
import re

# Prepare the embeddings array
weather_data['embedding'] = weather_data['embedding'].apply(ast.literal_eval)
weather_embeddings = np.array(weather_data['embedding'].tolist())

# Build the NearestNeighbors model
nn_model = NearestNeighbors(n_neighbors=5, metric='cosine')
nn_model.fit(weather_embeddings)
print("NearestNeighbors model built successfully.")



def extract_date(query):
    # Εξαγωγή ημερομηνίας με χρήση regex
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", query)
    date = date_match.group(0) if date_match else None
    return date


def query_results(query):
    query_embedding = get_embedding(query)
    
    distances, indices = nn_model.kneighbors([query_embedding])
    results = weather_data.iloc[indices[0]].drop(columns=['embedding'])
    return results


# Συνάρτηση για την παραγωγή απάντησης με χρήση του OpenAI API
def generate_text(user_message, model):
    """
    Συνδυάζει την ερώτηση του χρήστη με τα αποτελέσματα της αναζήτησης,
    αναλύει τις συνθήκες και χρησιμοποιεί το GEmini API για να παράγει την τελική απάντηση.
    """
    # Λήψη των αποτελεσμάτων της αναζήτησης και των ακατέργαστων δεδομένων
    results = query_results(user_message)
    print(f"Query Results: {results}")

    # Convert results to a readable format
    results_str = results.to_string(index=False)

    prompt = (
        f"You are a helpful assistant in a government website that helps citizens take precautions against wildfires. "
        f"A user can ask you what measures to take in case of a wildfire or to prevent one. "
        f"They can ask you questions about weather conditions of specific locations and dates. "
        f"If the query does not contain a location from the results, do not use the results, just provide the answer."
        f"If the query is irrevelant to the website's purpose, advise the user to ask a different question. "
        f"Provide the answer in a user friendly markdown format. Do not create markdown tables."
        f"QUERY: {user_message}\n"
        f"RELEVANT DATA:\n{results_str}\n"
        f"ANSWER:"
        )

    # answer = response.choices[0].message.content.strip()
    response = model.generate_content(prompt)
    answer = response.text
    return answer


def initialize_llm():
    # Set your Gemini API key
    os.environ['GOOGLE_API_KEY']='AIzaSyCdF0puCdMW-s-9WmCNdSY4eLanHO9yJWQ' # replace with your own key
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