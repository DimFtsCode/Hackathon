from pymongo import MongoClient
import os
import pandas as pd
import google.generativeai as palm
import re
import ast
import json

# MongoDB configuration
mongo_uri = "mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather"
mongo_client = MongoClient(mongo_uri)

# Access the Weather database and RAG_DATA collection
db = mongo_client["Weather"]
weather_collection = db["Combined_data"]

print("Connected to MongoDB successfully.")


# def format_results(results):
#     """
#     Converts MongoDB query results into a human-readable text format for the LLM.
#     """
#     try:
#         results = ast.literal_eval(results)
#     except Exception as e:
#         print(f"Error parsing results: {e}")
#         results = []   
         
#     formatted_results = []
#     for result in results:
#         formatted_results.append(
#             f"Location: {result.get('name', 'Unknown')},"
#             f"Date: {result.get('date', 'Unknown')},"
#             f"Time: {result.get('time', 'Unknown')},"
#             f"Temperature: {result.get('temperature', 'N/A')}°C,"
#             f"Wind Speed: {result.get('wind_speed', 'N/A')} km/h,"
#             f"Wind Direction: {result.get('wind_dir', 'N/A')}°,"
#             f"Humidity: {result.get('humidity', 'N/A')}%,"
#             f"Visibility: {result.get('visibility', 'N/A')} km,"
#             f"Fire: {'Yes' if result.get('fire', 0) == 1 else 'No'}"
#         )
#     return "\n\n".join(formatted_results)

def create_pipeline(response):
    raw_pipeline = response.text
    
    # Step 1: Remove triple backticks and 'json' prefix
    if raw_pipeline.startswith("```json"):
        raw_pipeline = raw_pipeline[7:]  # Remove the first '```json'
    if raw_pipeline.endswith("```\n"):
        raw_pipeline = raw_pipeline[:-4]  # Remove the last '```'
    
    # Step 1: Replace unquoted keys ($match, $group, etc.) with quoted keys
    cleaned_pipeline = re.sub(r'(\s*)(\$[a-zA-Z0-9_]+|[a-zA-Z0-9_]+):', r'\1"\2":', raw_pipeline)    
    
    try:
        pipeline = json.loads(cleaned_pipeline)
        print("Cleaned Pipeline:", pipeline)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")  
    return pipeline 

def generate_text(user_message, model):
    """
    Combines user query with retrieved results and uses the Gemini API to generate a response.
    """
    prompt = (
            f"You will receive a user query, and you will need to extract usefull information out of it. "
            f"You need to create a relevant query for a mongodb database that can extract the information that the user is asking for. "
            f"The database contains weather data about different locations and dates, and also a column about whether there was a fire or not"
            f"DATABASE DOCUMENT EXAMPLE: ('_id': ObjectId('673f3920759ebea332dfaec4'), 'name': 'Aigeirouses', 'latitude': 38.07, 'longitude': 23.159, 'date': '2020-01-01', 'time': 0, 'temperature': 5, 'wind_speed': 6, 'wind_dir': 360, 'humidity': 54, 'visibility': 10, 'fire': 0)"
            f"They can ask you questions about weather conditions of specific locations and dates. "
            f"Create a pipeline that I can use with the 'aggregate' function of mongodb to extract the information that the user is asking for. The pipeline should return the whole documents that match the query."
            f"DO NOT include 'javascript' or 'python' before you answer"
            f"If the query is irrelevant to the database purpose, answer with \"NO_DATA\" "
            f"USER QUERY: {user_message}\n"
            f"ANSWER:"
        )

    raw_pipeline = model.generate_content(prompt)
    print("Raw Pipeline: ",raw_pipeline.text)

    if "NO_DATA" in raw_pipeline.text:
        relevant_data = "NONE"
    else:
        pipeline = create_pipeline(model.generate_content(prompt))
        result = weather_collection.aggregate(pipeline)
        relevant_data = str([doc for doc in result])
        
    
    print("relevant_data: ",relevant_data)
        
    print("relevant_data type: ",type(relevant_data))
    #print("relevant data : ", format_results(relevant_data))
    prompt = (
        f"You are a helpful assistant in a government website that helps citizens take precautions against wildfires. "
        f"A user can ask you what measures to take in case of a wildfire or to prevent one. "
        f"They can ask you questions about weather conditions of specific locations and dates. "
        f"If the query does not contain a location from the results, do not use the results, just provide the answer."
        f"If the query is irrelevant to the website's purpose, advise the user to ask a different question. "
        f"If the relevant data is 'NONE', respond with a general but useful answer. "
        f"Provide the answer in a user-friendly markdown format. Do not create markdown tables."
        f"QUERY: {user_message}\n"
        f"RELEVANT DATA:\n{relevant_data}\n"
        f"ANSWER:"
    )
    
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