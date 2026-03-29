#Created by Luca Cottone on 3/28/26
'''Web app
Michigan residents can get legal help
    Renter's rights/property owners
    Small businesses
    Small Claims
    Injury
Made with Flask
Has chatbot interface as well
Attempting to win:
    best beginner
    best UI/UX
    Best use of Gemini API
'''
from flask import Flask, redirect, url_for, render_template, request, session, jsonify # type: ignore
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import os
from pymongo import MongoClient
import requests

def database_conn():
    # Load variables from .env
    load_dotenv()

    # Connect to MongoDB Atlas
    client = MongoClient(os.getenv("MONGO_URI"))

    # set variable db = the mangoDB hackathonDB database
    db = client["hackathonDB"]
    return db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

#Connect to Database and assign it to db
db = database_conn()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("WARNING: GOOGLE_API_KEY not found in .env file")

# Function to load Michigan laws context
def get_mi_context():
    """Read laws.json and return Michigan law context as a formatted string."""
    try:
        with open("laws.json", "r") as file:
            laws_data = json.load(file)
        
        # Format the laws data into a readable string
        context = "Michigan Legal Information:\n"
        for topic, details in laws_data.items():
            context += f"\n{topic.replace('_', ' ').title()}:\n"
            for key, value in details.items():
                if key != "jargon_definition":
                    context += f"  - {key.replace('_', ' ').title()}: {value}\n"
                else:
                    context += f"  - What it means: {value}\n"
        
        return context
    except Exception as e:
        return f"Error loading Michigan laws: {str(e)}"

def search_michigan_cases(query):
    """
    Search Michigan case law using CourtListener API v3.
    Returns top 2 most recent opinions with citations and snippets.
    
    Args:
        query (str): Search term for cases
    
    Returns:
        list: Top 2 cases with caseName, citation, date_filed, snippet, and url
    """
    try:
        # Get CourtListener API token from environment
        api_token = os.getenv("COURTLISTENER_API_TOKEN")
        if not api_token:
            return []
        
        # CourtListener v3 Search API endpoint
        url = "https://www.courtlistener.com/api/rest/v3/search/"
        
        # Set up headers with authentication
        headers = {
            "Authorization": f"Token {api_token}",
            "Accept": "application/json"
        }
        
        # Parameters: type='o' (opinions), court='mich' (Michigan)
        params = {
            "q": query,
            "type": "o",  # Opinions only
            "court": "mich",  # Michigan courts only
            "order_by": "-date_filed"  # Most recent first
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract top 2 cases
        cases = []
        for case_data in data.get("results", [])[:2]:
            case_info = {
                "caseName": case_data.get("case_name", "Unknown Case"),
                "citation": case_data.get("citation", [{}])[0].get("cite", "Unknown Citation") if case_data.get("citation") else "Unknown Citation",
                "date_filed": case_data.get("date_filed", "Unknown Date"),
                "snippet": case_data.get("snippet", "No summary available"),
                "url": case_data.get("absolute_url", ""),
                "court": case_data.get("court", "Michigan Court")
            }
            cases.append(case_info)
        
        return cases
    
    except requests.exceptions.RequestException as e:
        print(f"CourtListener API Error: {str(e)}")
        return []
    except Exception as e:
        print(f"Error searching cases: {str(e)}")
        return []

def format_cases_context(cases):
    """
    Format case data into a readable context string for the chatbot.
    
    Args:
        cases (list): List of case dictionaries
    
    Returns:
        str: Formatted context string
    """
    if not cases:
        return ""
    
    context = "\n\nRelevant Michigan Court Cases:\n"
    for i, case in enumerate(cases, 1):
        context += f"\n{i}. {case['caseName']}\n"
        context += f"   Citation: {case['citation']}\n"
        context += f"   Court: {case['court']}\n"
        context += f"   Date: {case['date_filed']}\n"
        context += f"   Summary: {case['snippet'][:300]}...\n"
    
    return context

@app.route("/") #root page
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Chatbot route that uses Gemini API with Michigan legal context."""
    try:
        # Get user message and zip code from request
        data = request.get_json()
        user_message = data.get("message", "")
        zip_code = data.get("zipCode", None)
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get Michigan laws context
        mi_context = get_mi_context()
        
        # Create system instruction
        system_instruction = f"""You are a Michigan legal helper. Use these facts: {mi_context}

Explain everything in 6th-grade English. If you use a legal word, explain it immediately in parentheses.
Answer the user's question clearly and helpfully."""
        
        # Check if user is asking about case law or precedents
        case_keywords = ["judge say", "judges say", "happened before", "case", "ruling", "precedent", "court decision", "what do lawyers"]
        is_case_question = any(keyword in user_message.lower() for keyword in case_keywords)
        
        # If asking about cases, fetch and include relevant case law
        if is_case_question:
            cases = search_michigan_cases(user_message)
            if cases:
                cases_context = format_cases_context(cases)
                system_instruction += cases_context
                system_instruction += "\n\nPlease include information about these Michigan court cases in your answer and explain them in simple terms."
        
        # Add zip code context if provided (for future local court mapping)
        if zip_code:
            system_instruction += f"\n\nUser's location: Michigan zip code {zip_code}"
        
        # Initialize Gemini model
        model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_instruction)
        
        # Send message to Gemini and get response
        response = model.generate_content(user_message)
        assistant_message = response.text
        
        # Return response to frontend
        return jsonify({"response": assistant_message}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

@app.route("/Renters_Rights")
def renters_rights():
    data1 = list(db.RentersRights.find())
    return render_template("RentersRights.html", data = data1)

@app.route("/Small_Businesses")
def small_businesses():
    return render_template("small_businesses.html")

@app.route("/Personal_Injury")
def personal_injury():
    return render_template("p_injury.html")

@app.route("/Small_Claims")
def small_claims():
    return render_template("s_claims.html")

@app.route("/resources")
def resources():
    """Display all available legal topics."""
    try:
        topics = list(db.legal_topics.find())
        return render_template("resources.html", topics=topics)
    except Exception as e:
        return f"Error loading resources: {str(e)}", 500

@app.route("/topic/<topic_id>")
def topic_page(topic_id):
    """Display detailed legal information for a topic."""
    try:
        topic = db.legal_topics.find_one({"id": topic_id})
        if not topic:
            return "Topic not found", 404
        return render_template("topic.html", topic=topic)
    except Exception as e:
        return f"Error loading topic: {str(e)}", 500

@app.route("/search-cases", methods=["GET", "POST"])
def search_cases():
    """Search for Michigan case law."""
    cases = []
    query = ""
    
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            cases = search_michigan_cases(query)
    elif request.method == "GET":
        query = request.args.get("q", "").strip()
        if query:
            cases = search_michigan_cases(query)
    
    return render_template("case_law.html", cases=cases, query=query)

if __name__ == "__main__":
    print("Starting Flask app on 0.0.0.0:5000 (all interfaces). Access via http://127.0.0.1:5000 locally")
    app.run(debug=True, host="0.0.0.0", port=5000)
