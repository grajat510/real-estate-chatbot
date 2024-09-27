from flask import Flask, render_template, request
import pandas as pd
import requests
from sentence_transformers import SentenceTransformer
import time
import logging
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load CSV data and log data loading status
try:
    listings_df = pd.read_csv('data/listings.csv')
    buildings_df = pd.read_csv('data/buildings.csv')
    buildings_amenities_df = pd.read_csv('data/buildingsamenities.csv')
    listings_amenities_df = pd.read_csv('data/listingamenities.csv')

    listings_df['description'] = listings_df['description'].fillna("")
    buildings_df['description'] = buildings_df['description'].fillna("")

    logging.info("CSV data loaded successfully and NaN descriptions handled.")
except Exception as e:
    logging.error(f"Error loading CSV files: {e}")

# Initialize the sentence embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Set your Hugging Face API key
api_key = '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'

# Function to call Hugging Face API for GPT-like responses
def gpt_chat(prompt):
    api_url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": prompt}

    for _ in range(3):
        response = requests.post(api_url, headers=headers, json=payload)
        logging.debug(f"API Response: {response.json()}")
        if response.status_code == 200:
            try:
                return response.json()[0]['generated_text']
            except (KeyError, IndexError):
                return "Error: Unable to retrieve the response."
        elif response.status_code == 503 and "is currently loading" in response.json().get('error', ''):
            time.sleep(5)
        else:
            return "Error: " + response.json().get("error", "Unknown error")
    return "Error: Model could not be loaded. Please try again later."

# Helper function to clean and normalize strings
def clean_string(text):
    return str(text).lower().strip() if isinstance(text, str) else ""

# Function to embed text using the model
def embed_text(text):
    return model.encode(text)

# Partial search mechanism using cosine similarity with filtering by listing type
def search_listings(user_input, listing_type=None):
    user_input_embedding = embed_text(user_input)
    listings_embeddings = listings_df['description'].apply(embed_text).tolist()
    similarities = cosine_similarity([user_input_embedding], listings_embeddings)[0]

    top_indices = np.argsort(similarities)[-5:][::-1]
    matches = listings_df.iloc[top_indices]

    # Filter by listing type if specified (rental or sale)
    if listing_type:
        matches = matches[matches['listing_type'] == listing_type]

    if not matches.empty:
        result = ""
        for i, (_, row) in enumerate(matches.iterrows(), 1):
            result += (f"Listing {i}: {row['street_address']}, {row['city']}, {row['state']}, "
                       f"{row['zip_code']} - {row['beds']} beds, {row['baths']} baths, "
                       f"{row['price']} USD, {row['square_feet']} sqft.\n")
        return result.strip()
    else:
        return "No listing available of this sort."

def search_buildings(user_input, listing_type=None):
    user_input_embedding = embed_text(user_input)
    buildings_embeddings = buildings_df['description'].apply(embed_text).tolist()
    similarities = cosine_similarity([user_input_embedding], buildings_embeddings)[0]

    top_indices = np.argsort(similarities)[-5:][::-1]
    matches = buildings_df.iloc[top_indices]

    if not matches.empty:
        result = ""
        for i, (_, row) in enumerate(matches.iterrows(), 1):
            result += (f"Building {i}: {row['name']} ({row['no_floors']} floors), {row['street_address']}, "
                       f"{row['borough']} - Built in {row['year_built']}.\n")
        return result.strip()
    else:
        return "No building available of this sort."

def search_amenities(user_input):
    user_input = clean_string(user_input)
    listing_amenities_matches = listings_amenities_df[
        listings_amenities_df['name'].str.contains(user_input, case=False, na=False)
    ]
    building_amenities_matches = buildings_amenities_df[
        buildings_amenities_df['name'].str.contains(user_input, case=False, na=False)
    ]

    response = ""
    if not listing_amenities_matches.empty:
        response += "Listing Amenities found: " + ", ".join(listing_amenities_matches['name'].tolist()) + "\n"
    if not building_amenities_matches.empty:
        response += "Building Amenities found: " + ", ".join(building_amenities_matches['name'].tolist()) + "\n"

    return response.strip() if response else "No amenities found for your query."

# Find relevant data based on user input and listing type
def find_relevant_data(user_input, listing_type=None):
    listing_result = search_listings(user_input, listing_type)
    building_result = search_buildings(user_input, listing_type)
    amenities_result = search_amenities(user_input)

    return f"{listing_result}\n\n{building_result}\n\n{amenities_result}".strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def chatbot_response():
    user_input = request.form['msg'].lower()

    # Determine if the user asks for rental, sale, or both listings
    listing_type = None
    if "rental" in user_input:
        listing_type = 10  # For rental listings
    elif "sale" in user_input or "to be sold" in user_input:
        listing_type = 20  # For sale listings

    relevant_data = find_relevant_data(user_input, listing_type)

    if "No listing available" in relevant_data and "No building available" in relevant_data and "No amenities found" in relevant_data:
        bot_response = gpt_chat(user_input)
    else:
        bot_response = "No further info needed from GPT."

    return f"{relevant_data}\n\nChatbot: {bot_response}"

if __name__ == '__main__':
    # Use the PORT environment variable for cloud deployment (Render, Heroku, etc.)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
