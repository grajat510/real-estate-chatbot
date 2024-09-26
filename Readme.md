```bash

# Real Estate Chatbot

This project is a real estate chatbot built with Flask. The chatbot provides information on listings, buildings, and amenities from CSV data files and integrates with the Hugging Face API to generate additional responses if necessary. The chatbot is embedded into a simple web interface, where users can input queries and receive responses about real estate listings.

## Project Structure

real-estate-chatbot/
│
├── app.py               # Flask backend for the chatbot
├── requirements.txt     # Python dependencies
├── data/                # Folder containing the CSV files
│   ├── listings.csv
│   ├── buildings.csv
│   ├── buildingsamenities.csv
│   └── listingamenities.csv
├── templates/
│   └── index.html       # Frontend UI for the chatbot
└── static/
    └── styles.css       # Stylesheet for the chatbot interface


# Features
1. Searches and filters real estate listings based on user input.
2. Provides building information such as the number of floors and construction year.
3. Searches for amenities available in listings and buildings.
4. Calls Hugging Face GPT API for additional responses when no data is found.
5. Simple web interface for interacting with the chatbot.

# Requirements
1. Python 3.8 or later
2. Flask
3. Pandas
4. FAISS
5. Sentence Transformers
6. Hugging Face Transformers
The dependencies can be installed via the requirements.txt file.

# Installation and Setup
1. Clone the Repository
git clone https://github.com/your-username/real-estate-chatbot.git
cd real-estate-chatbot
            OR
Extract the zip file if you have received it.


2. Create a Virtual Environment
It is recommended to create a virtual environment to avoid dependency conflicts.
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

# Install Dependencies
Install the necessary Python packages from requirements.txt:
pip install -r requirements.txt

# Add Hugging Face API Key
In the app.py file, set your Hugging Face API key in the api_key variable:
api_key = 'your_huggingface_api_key'
You can get an API key by creating an account at Hugging Face and generating one in your profile settings.

# Prepare the CSV Data
Ensure the CSV files (listings.csv, buildings.csv, buildingsamenities.csv, listingamenities.csv) are placed in the data/ folder as per the project structure.

# Run the Application
Start the Flask development server by running the following command:
python app.py
The app will be available at http://127.0.0.1:5000/.

# Usage
Once the application is running, open a web browser and navigate to http://127.0.0.1:5000/. You can interact with the chatbot by typing a query in the input box, such as:

"Show me listings in New York."
"What buildings have gyms?"
"Any buildings with more than 20 floors?"
The chatbot will search the CSV data and return relevant listings, buildings, or amenities based on your query.

If no matching data is found, the chatbot will generate a response using the Hugging Face GPT API.

# Known Issues
1. The search functionality is currently based on partial matches and cosine similarity of the text.
2. GPT responses are only called when no relevant data is found in the CSV files.
Contributing
3. Feel free to fork this repository, submit issues, or create pull requests to contribute to this project.

# License
This project is licensed under the MIT License.

# Key Points Covered in the README:
1. Project overview and structure
2. Step-by-step installation guide
3. Details on dependencies and environment setup
4. Instructions on how to run the application
5. Usage examples and chatbot interaction
6. Information about known issues and contribution guidelines

# How to Generate a Hugging Face API Key (Free)
To use the GPT-like fallback model, you'll need an API key from Hugging Face. Follow these steps to obtain your key:
1. Go to the Hugging Face website.
2. Sign up for a free account or log in if you already have one.
3. Once logged in, navigate to your profile and go to Settings.
4. In the API Tokens section, click New Token.
5. Give your token a name (e.g., real-estate-chatbot) and click Create Token.
6. Copy the generated API token and replace the value of api_key in your app.py file.