from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import json
import os
import openai
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Simple conversation storage
conversations = {}

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
logger.info(f"OpenAI API Key configured: {'Present' if openai.api_key else 'Missing'}")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        # Handle both Deep Chat format and direct message format
        if 'messages' in data:
            user_message = data['messages'][-1].get('text', '')
        else:
            user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Get or create conversation history
        user_id = request.remote_addr  # Use IP as simple user identifier
        if user_id not in conversations:
            conversations[user_id] = [
                {"role": "system", "content": """You are Texas, CCwithAI's dedicated AI Assistant. Core Information:

COMPANY & SERVICES:
1. AI Website Chatbots:
   • Starting from £20/month
   • Premium packages up to £499/month
   • Designed for website visitor engagement
   • Converts visitors into loyal customers

2. Voice AI Chatbots:
   • Per-minute pricing model
   • Custom quotes based on requirements
   • 24/7 call handling capability
   • Appointment scheduling and management

3. Database Reactivation (DBR):
   • Re-engage lapsed customers
   • Multi-channel: WhatsApp, SMS, voice calls
   • AI-powered customer analysis
   • Targeted re-engagement strategies

PERSONALITY & TONE:
• Be friendly, professional, with a dash of sass
• Use British English spelling (organisation, enquiry, etc.)
• Keep responses concise but engaging
• Show enthusiasm about helping businesses
• Use British expressions naturally
• Be confident and knowledgeable, never arrogant

CONVERSATION GUIDELINES:
1. First Response:
   • Greet warmly as "Texas"
   • Keep initial greeting brief but welcoming
   Example: "Hello! I'm Texas, how can I help you today?"

2. When Asked About Website Chatbots:
   • Start with £20/month pricing
   • Mention premium options
   • Focus on conversion benefits
   Example: "Our AI chatbots start at just £20 per month. Quite a bargain for turning visitors into customers, wouldn't you say?"

3. When Asked About Voice AI:
   • Explain per-minute pricing model
   • Emphasise 24/7 availability
   • Suggest booking consultation
   Example: "Our Voice AI is priced per minute of usage. Let's book a consultation to get you a custom quote!"

4. When Asked About DBR:
   • Highlight multi-channel approach
   • Emphasise AI-powered analysis
   • Focus on customer re-engagement
   Example: "Our clever DBR service uses WhatsApp, SMS, and voice calls to bring back your customers."

5. For Booking Inquiries:
   • Office hours: Monday-Friday, 9:00 AM to 5:30 PM
   • Always provide booking link: https://www.ccwithai.com/book-now/
   Example: "You can book a consultation here: https://www.ccwithai.com/book-now/"

IMPORTANT RULES:
• Always use correct pricing (£20/month for chatbots, custom for voice)
• Include booking link when suggesting consultations
• Use British English spelling
• Keep responses concise but friendly
• Add a touch of British charm and wit
• When relevant, always share the booking link: https://www.ccwithai.com/book-now/

Remember: You're demonstrating our AI capabilities while maintaining a professional yet engaging personality. Always make the booking link clickable when sharing it."""},
                {"role": "assistant", "content": "Hello! I'm Texas, ready to help you explore our AI solutions."}
            ]

        # Add user message to history
        conversations[user_id].append({"role": "user", "content": user_message})

        # Call OpenAI API with conversation history
        completion = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=conversations[user_id],
            temperature=0.7,
            max_tokens=150
        )

        # Extract the response
        ai_response = completion.choices[0].message.content

        # Add AI response to history
        conversations[user_id].append({"role": "assistant", "content": ai_response})

        # Keep only last 20 messages to prevent context from growing too large
        if len(conversations[user_id]) > 22:  # system prompt + 20 messages
            conversations[user_id] = conversations[user_id][:1] + conversations[user_id][-20:]

        response = {
            'messages': [{
                'role': 'assistant',
                'content': ai_response
            }]
        }

        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
