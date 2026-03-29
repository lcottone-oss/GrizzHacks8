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
import sys
print(sys.executable)
#from bson import ObjectId
import anthropic
import chromadb
from flask import Flask, redirect, url_for, render_template, request, session, jsonify # type: ignore
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import os
from openai import OpenAI
from pymongo import MongoClient
import requests

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt
import uuid
from datetime import datetime

chroma_client = chromadb.PersistentClient(path="./mcl_chroma_db")
collection = chroma_client.get_collection(
    name="michigan_laws",
    # metadata={"hnsw:space": "cosine"}
)

# SERVICE = "openai"
SERVICE = "gemini"
# SERVICE = "claude"
openai_client = OpenAI()
claude_client = anthropic.Anthropic()

# GEMINI_MODEL = "gemini-3.1-flash-lite-preview"
GEMINI_MODEL = "gemini-2.5-flash-lite"

OPENAI_MODEL = "gpt-4o-mini"

CLAUDE_MODEL = "claude-sonnet-4-6"



def database_conn():
    # Load variables from .env
    load_dotenv()
    #print("ENV loaded:", os.path.exists(".env"), "MONGO_URL:", bool(os.getenv("MONGO_URL")))

    # Connect to MongoDB Atlas
    client = MongoClient(os.getenv("MONGO_URL"))

    # set variable db = the mangoDB HackathonDB database
    db = client["HackathonDB"]
    return db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
"""
And the DB models + user loader somewhere before your routes (the `User`, `Conversation`, `Message` classes and `load_user` function from Chunk 1).

And in your `.env`, add:
"""
SECRET_KEY="some-random-string-here"

#Connect to Database and assign it to db
mongo_db = database_conn()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("WARNING: GOOGLE_API_KEY not found in .env file")

def get_embeddings(texts:str):
    response = openai_client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    return [e.embedding for e in response.data]

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

def ask_gpt(query, current_chat_logs = None, system_instruction="", service=SERVICE):
    # Only keep valid conversational roles for all services
    messages = []
    reply = ""
    if current_chat_logs:
        for log in current_chat_logs:
            role = str(log.get("role"))
            content = log.get("content")
            if role in ("user", "assistant"):
                messages.append({"role": role, "content": content})
    else:
        current_chat_logs = []
    messages.append({"role": "user", "content": query})

    if service == "gemini":
        role_map = {"assistant": "model", "user": "user"}
        gemini_messages = [
            {"role": role_map.get(msg["role"], msg["role"]), "parts": [{"text": msg["content"]}]}
            for msg in messages
        ]
        model = genai.GenerativeModel(GEMINI_MODEL, system_instruction=system_instruction)
        response = model.generate_content(gemini_messages)
        reply = response.text

    elif service == "openai":
        openai_messages = []
        if system_instruction:
            openai_messages.append({"role": "system", "content": system_instruction})
        openai_messages += messages
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=openai_messages
        )
        reply = response.choices[0].message.content

    elif service == "claude":
        message = claude_client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=system_instruction,
            messages=messages,
        )
        reply = message.content[0].text

    return reply

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

class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password      = db.Column(db.String(200), nullable=False)
    conversations = db.relationship("Conversation", backref="user", lazy=True)


class Conversation(db.Model):
    id         = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id    = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title      = db.Column(db.String(200), default="New Conversation")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages   = db.relationship("Message", backref="conversation", lazy=True, order_by="Message.timestamp")


class Message(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(36), db.ForeignKey("conversation.id"), nullable=False)
    role            = db.Column(db.String(10), nullable=False)
    content         = db.Column(db.Text, nullable=False)
    timestamp       = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()

@app.route("/") #root page
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
# def chat():
#     """Chatbot route that uses Gemini API with Michigan legal context."""
#     try:
#         # Get user message and zip code from request
#         data = request.get_json()
#         user_message = data.get("message", "")
#         zip_code = data.get("zipCode", None)
        
#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400
        
#         # Get Michigan laws context
#         mi_context = get_mi_context()
        
#         # Create system instruction
#         system_instruction = f"""You are a Michigan legal helper. Use these facts: {mi_context}

# Explain everything in 6th-grade English. If you use a legal word, explain it immediately in parentheses.
# Answer the user's question clearly and helpfully."""
        
#         # Check if user is asking about case law or precedents
#         case_keywords = ["judge say", "judges say", "happened before", "case", "ruling", "precedent", "court decision", "what do lawyers"]
#         is_case_question = any(keyword in user_message.lower() for keyword in case_keywords)
        
#         # If asking about cases, fetch and include relevant case law
#         if is_case_question:
#             cases = search_michigan_cases(user_message)
#             if cases:
#                 cases_context = format_cases_context(cases)
#                 system_instruction += cases_context
#                 system_instruction += "\n\nPlease include information about these Michigan court cases in your answer and explain them in simple terms."
        
#         # Add zip code context if provided (for future local court mapping)
#         if zip_code:
#             system_instruction += f"\n\nUser's location: Michigan zip code {zip_code}"
        
#         # Initialize Gemini model
#         model = genai.GenerativeModel(GEMINI_MODEL, system_instruction=system_instruction)
        
#         # Send message to Gemini and get response
#         response = model.generate_content(user_message)
#         assistant_message = response.text
        
#         # Return response to frontend
#         return jsonify({"response": assistant_message}), 200
    
#     except Exception as e:
#         return jsonify({"error": f"Error processing request: {str(e)}"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data         = request.get_json()
        user_message = data.get("message", "")
        zip_code     = data.get("zipCode", None)
        conv_id      = data.get("conversation_id")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400


        conv = None
        if current_user.is_authenticated:
            if conv_id:
                conv = Conversation.query.filter_by(id=conv_id, user_id=current_user.id).first()
            if not conv:
                conv = Conversation(user_id=current_user.id, title=user_message[:60])
                db.session.add(conv)
                db.session.flush()


        if conv:
            current_chat_logs = [
                {"role": m.role, "content": m.content}
                for m in conv.messages
            ]
        else:
            # Guest: history comes from frontend, not DB
            current_chat_logs = data.get("history", [])


        rag_query = ""
        if current_chat_logs:
            for log in current_chat_logs:
                if log["role"] == "user":
                    rag_query += f"{log['content']}\n"
            rag_query += f"\n\n{user_message}\n"
        else:
            rag_query = user_message

        summarize_instruction = '''Rewrite a concise summarized version of the user's message.
        This summary will be used to retrieve relevant Michigan laws, so include key details and context that would help identify applicable statutes.
        Do not include any information that is not directly relevant to the legal issue at hand.
        Do not include any information not provided by the user.
        The summary should be clear and focused on the user's legal problem.
        If there are multiple disjoint cases, keep ONLY the latest one.'''
        rag_summary = ask_gpt(rag_query, system_instruction=summarize_instruction)

        with open("chat_logs.txt", "w") as log_file:
            log_file.write(f"\n\nrag_query:\n{rag_summary}\n\n")

        query_embedding = get_embeddings(rag_summary)[0]

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=20,
            include=["documents", "metadatas", "distances"]
        )

        docs      = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]

        candidates = [
            (doc, meta, dist)
            for doc, meta, dist in zip(docs, metadatas, distances)
            if dist <= 0.70
        ]

        MIN_RESULTS = 5
        MAX_RESULTS = 15
        if candidates:
            filtered = [candidates[0]]
            for i in range(1, len(candidates)):
                if i >= MIN_RESULTS:
                    if candidates[i][2] - candidates[i-1][2] > 0.07 or i >= MAX_RESULTS:
                        break
                filtered.append(candidates[i])
        else:
            filtered = []

        mcl_context = ""
        retrieved_sections = []
        if filtered:
            for doc, meta, dist in filtered:
                mcl_context += (
                    f"MCL {meta['mcl_number']} — {meta['title']} (Chapter {meta['chapter']}):\n"
                    f"{doc}\n\n"
                )
                retrieved_sections.append({
                    "mcl_number": meta['mcl_number'],
                    "title":      meta['title'],
                    "distance":   round(dist, 4)
                })

        case_keywords = ["judge say", "judges say", "happened before", "case", "ruling",
                         "precedent", "court decision", "what do lawyers"]
        is_case_question = any(kw in user_message.lower() for kw in case_keywords)

        cases_context = ""
        if is_case_question:
            cases = search_michigan_cases(user_message)
            if cases:
                cases_context = format_cases_context(cases)

        system_instruction = (
            "You are a Michigan legal helper. "
            "Explain everything in 6th-grade English. "
            "If you use a legal word, explain it immediately in parentheses. "
            "Always cite the specific MCL number when referencing a law. "
            "If an MCL section is irrelevant to the user's question, ignore it. "
            "Answer the user's question clearly and helpfully."
        )

        if zip_code:
            if (int(zip_code) >= 48001 and int(zip_code) <= 49971):
                system_instruction += f"\n\nUser's location: Michigan zip code {zip_code}."
            else:
                system_instruction += f"\n\nUser's location: Michigan (invalid zip code {zip_code} provided)."

        if mcl_context:
            system_instruction += f"\n\nUse these relevant Michigan laws to answer:\n\n{mcl_context}"
            with open("chat_logs.txt", "a") as log_file:
                log_file.write(f"\n\nmcl_context:\n{mcl_context}\n\n")

        if cases_context:
            system_instruction += f"\n\n{cases_context}\nInclude information about these Michigan court cases and explain them in simple terms."


        response = ask_gpt(user_message, current_chat_logs=current_chat_logs, system_instruction=system_instruction)


        if conv:
            db.session.add(Message(conversation_id=conv.id, role="user",      content=user_message))
            db.session.add(Message(conversation_id=conv.id, role="assistant", content=response))
            db.session.commit()

        return jsonify({
            "response":           response,
            "retrieved_sections": retrieved_sections,
            "conversation_id":    conv.id if conv else None,
            "title":              conv.title if conv else None
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500
@app.route("/Renters_Rights")
def renters_rights():
    data1 = list(mongo_db.RentersRights.find())
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
        topics = list(mongo_db.legal_topics.find())
        return render_template("resources.html", topics=topics)
    except Exception as e:
        return f"Error loading resources: {str(e)}", 500

@app.route("/topic/<topic_id>")
def topic_page(topic_id):
    """Display detailed legal information for a topic."""
    try:
        topic = mongo_db.legal_topics.find_one({"id": topic_id})
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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            return render_template("register.html", error="Username and password required.")
        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already taken.")
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User(username=username, password=hashed.decode())
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            login_user(user)
            return redirect(url_for("home"))
        return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/conversation/new", methods=["POST"])
@login_required
def new_conversation():
    conv = Conversation(user_id=current_user.id)
    db.session.add(conv)
    db.session.commit()
    return jsonify({"id": conv.id})

@app.route("/conversation/<conv_id>")
@login_required
def get_conversation(conv_id):
    conv = Conversation.query.filter_by(id=conv_id, user_id=current_user.id).first_or_404()
    messages = [{"role": m.role, "content": m.content} for m in conv.messages]
    return jsonify({"id": conv.id, "title": conv.title, "messages": messages})

@app.route("/conversations")
@login_required
def get_conversations():
    convs = Conversation.query.filter_by(user_id=current_user.id)\
                .order_by(Conversation.created_at.desc()).all()
    return jsonify([{"id": c.id, "title": c.title, "created_at": c.created_at.strftime("%b %d")} for c in convs])

@app.route("/conversation/<conv_id>/delete", methods=["POST"])
@login_required
def delete_conversation(conv_id):
    conv = Conversation.query.filter_by(id=conv_id, user_id=current_user.id).first_or_404()
    Message.query.filter_by(conversation_id=conv.id).delete()
    db.session.delete(conv)
    db.session.commit()
    return jsonify({"success": True})

if __name__ == "__main__":
    print("Starting Flask app on 0.0.0.0:5000 (all interfaces). Access via http://127.0.0.1:5000 locally")
    app.run(debug=True, host="0.0.0.0", port=5000)
