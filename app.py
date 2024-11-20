from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai
import json

# ------------------ SETUP ------------------

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# ------------------ EXCEPTION HANDLERS ------------------

@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return {"error": str(e)}, 500

# ------------------ KNOWLEDGE BASE ------------------

def load_knowledge_base():
    try:
        with open('knowledge_base.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"data": []}

def save_knowledge_base(data):
    with open('knowledge_base.json', 'w') as f:
        json.dump(data, f, indent=2)

# ------------------ ROUTES ------------------

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/manage')
def manage():
    return send_from_directory('static', 'manage.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        body = request.json
        user_message = body.get('message', '')
        
        # Load knowledge base
        knowledge_base = load_knowledge_base()
        context = "You are a helpful AI assistant for CC With AI. Use this knowledge base to assist users: "
        context += json.dumps(knowledge_base)  # knowledge base is already a list
        
        # Create chat completion
        response = openai.ChatCompletion.create(
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
        
        # Extract assistant's response
        assistant_message = response['choices'][0]['message']['content']
        
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
        knowledge_base['data'].append(new_data)
        save_knowledge_base(knowledge_base)
        return {"status": "success", "message": "Knowledge base updated"}

# ------------------ START SERVER ------------------

if __name__ == '__main__':
    app.run(debug=True, port=5000)
