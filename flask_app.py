from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS
import os
from openai import OpenAI
import json
from config import Config

# ------------------ SETUP ------------------

# Initialize OpenAI client with API key from config
client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Set up static folder path
STATIC_FOLDER = '/home/ganzyistheone/mysite/static'

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/static')
CORS(app, origins=['https://www.ccwithai.com', 'http://www.ccwithai.com', 'https://ccwithai.com', 'http://ccwithai.com'],
     allow_headers=['Content-Type'],
     methods=['GET', 'POST', 'OPTIONS'])

# ------------------ EXCEPTION HANDLERS ------------------

@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return {"error": str(e)}, 500

# ------------------ KNOWLEDGE BASE ------------------

def load_knowledge_base():
    try:
        with open('/home/ganzyistheone/mysite/knowledge_base.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_knowledge_base(data):
    with open('/home/ganzyistheone/mysite/knowledge_base.json', 'w') as f:
        json.dump(data, f, indent=2)

# ------------------ ROUTES ------------------

@app.route('/')
def index():
    return send_from_directory(STATIC_FOLDER, 'index.html')

@app.route('/manage')
def manage():
    return send_from_directory(STATIC_FOLDER, 'manage.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    print(f"Attempting to serve static file: {filename}")  # Debug print
    try:
        return send_from_directory(STATIC_FOLDER, filename)
    except Exception as e:
        print(f"Error serving static file {filename}: {str(e)}")  # Debug print
        return str(e), 404

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        body = request.json
        user_message = body.get('message', '')
        
        # Load knowledge base
        knowledge_base = load_knowledge_base()
        context = "You are a helpful AI assistant for CC With AI. Use this knowledge base to assist users: "
        context += json.dumps(knowledge_base)
        
        # Create chat completion with new API format
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        # Extract assistant's response with new API format
        assistant_message = response.choices[0].message.content
        
        return {"response": assistant_message}
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return {"error": str(e)}, 500

@app.route('/api/knowledge', methods=['GET', 'POST'])
def manage_knowledge():
    if request.method == 'GET':
        knowledge_base = load_knowledge_base()
        return knowledge_base
    elif request.method == 'POST':
        new_data = request.json
        knowledge_base = load_knowledge_base()
        knowledge_base.append(new_data)
        save_knowledge_base(knowledge_base)
        return {"status": "success", "message": "Knowledge base updated"}
