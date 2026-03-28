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
from datetime import timedelta
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

#Delete this key from gemini account as soon as competition ends
genai.configure(api_key="AIzaSyBFX0cY1AqUX2u6rcjbxKw32W1Z2Z0nEuc")

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found in .env file")

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
    return render_template("RentersRights.html")

@app.route("/Small_Businesses")
def small_businesses():
    return render_template("small_businesses.html")

@app.route("/Personal_Injury")
def personal_injury():
    return render_template("p_injury.html")

@app.route("/small_Claims")
def small_claims():
    return render_template("s_claims.html")

if __name__ == "__main__":
    app.run(debug = True)
