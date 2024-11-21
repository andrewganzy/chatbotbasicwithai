from flask import Flask, request, send_from_directory, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
CORS(app)

def load_knowledge_base():
    try:
        with open('knowledge_base.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading knowledge base JSON: {e}")
        return None

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

class ConversationContext:
    def __init__(self):
        self.industry = None
        self.services_discussed = []
        self.last_service = None
        self.messages = []

    def to_dict(self):
        return {
            'industry': self.industry,
            'services_discussed': self.services_discussed,
            'last_service': self.last_service,
            'messages': self.messages
        }

    @classmethod
    def from_dict(cls, data):
        context = cls()
        context.industry = data.get('industry')
        context.services_discussed = data.get('services_discussed', [])
        context.last_service = data.get('last_service')
        context.messages = data.get('messages', [])
        return context

    def update(self, user_message, assistant_response):
        # Track messages
        self.messages.append({"role": "user", "content": user_message})
        self.messages.append({"role": "assistant", "content": assistant_response})

        # Track industry
        industries = {
            'recruitment': ['recruitment', 'recruiter', 'hiring', 'candidates'],
            'dental': ['dental', 'dentist', 'dentistry'],
            'retail': ['retail', 'shop', 'store', 'sales']
        }
        
        for industry, keywords in industries.items():
            if any(keyword in user_message.lower() for keyword in keywords):
                self.industry = industry
                break

        # Track services
        services = {
            'DBR': ['dbr', 'database reactivation', 'reactivation'],
            'Voice AI': ['voice', 'call', 'phone'],
            'chatbot': ['chatbot', 'chat', 'bot'],
            'workflow': ['workflow', 'custom', 'bespoke']
        }
        
        for service, keywords in services.items():
            if any(keyword in assistant_response.lower() for keyword in keywords):
                if service not in self.services_discussed:
                    self.services_discussed.append(service)
                self.last_service = service

    def get_response(self, user_message):
        # Price inquiries
        if any(word in user_message.lower() for word in ['cost', 'price', 'pricing', 'how much']):
            if not self.services_discussed:
                return """Our pricing varies by service:
- AI Chatbots start from £99
- DBR uses a 50/50 profit-sharing model
- Voice AI is priced based on call volume
Which service would you like specific pricing for?"""
            
            responses = []
            if 'DBR' in self.last_service or 'dbr' in user_message.lower():
                responses.append("For our DBR (Database Reactivation) service, we work on a 50/50 profit-sharing model - meaning no upfront costs. We only succeed when you do!")
            if 'Voice AI' in self.last_service or 'voice' in user_message.lower():
                responses.append("Our Voice AI solutions are priced based on your specific needs and call volume.")
            if 'chatbot' in self.last_service or 'chatbot' in user_message.lower():
                responses.append("Our AI chatbots start from £99 for the basic package, which includes setup and training.")
            
            return ' '.join(responses) if responses else None

        # Setup inquiries
        if any(phrase in user_message.lower() for phrase in ['set up', 'setup', 'get started', 'begin', 'book']):
            response = "Perfect! "
            if self.industry:
                response += f"For your {self.industry} business, "
            if self.services_discussed:
                services = ', '.join(self.services_discussed)
                response += f"based on your interest in {services}, "
            response += "I'll help you schedule a consultation. You can book a one-to-one through our contact form. Would you like me to explain anything else about the services we discussed?"
            return response

        # Service specific inquiries
        for service in ['DBR', 'Voice AI', 'chatbot']:
            if service.lower() in user_message.lower():
                if self.industry:
                    if self.industry == 'recruitment':
                        if service == 'DBR':
                            return """For recruitment agencies, our DBR service helps you:
- Re-engage with dormant candidates
- Automatically update candidate status
- Identify and reactive promising candidates
- Work on a 50/50 profit-share model
Would you like to know more about pricing or setup?"""
                    # Add more industry-specific responses here

        return None

def get_system_prompt(knowledge_base):
    context = """I'm Texas, CCwithAI's AI assistant. How can I help you today?

When asked about services, I should say:
"The main services we offer are:
1. Database Reactivation (DBR) - AI-powered customer re-engagement
2. Voice AI - Inbound and outbound call automation
3. AI Chatbots - Starting from £99
4. Custom workflows bespoke to your business

Would you like to discuss one in further detail? To help me provide relevant examples, may I ask what industry you're in?"

INDUSTRY-SPECIFIC RESPONSES:
For Dentists:
"For a dental practice, we could implement:
- AI-automated appointment reminders
- Booking/cancellation handling via phone, SMS, or WhatsApp
- Free up your reception staff for more important tasks
- Patient follow-up automation"

For Real Estate:
"For real estate, we could set up:
- Automated property viewing scheduling
- Lead qualification via AI calls
- 24/7 property inquiry handling
- Client follow-up automation"

For Retail:
"For retail businesses, we could implement:
- Automated order status updates
- Stock availability checks
- Customer service automation
- Returns/exchanges processing"

CLOSING THE CONVERSATION:
When user shows interest:
"You can schedule a one-to-one with our experts through the booking form in our contact section. Would you like me to explain anything else?"

When user is ready to end:
"Thank you for your interest. I'm here if you need any further information. Have a great day!"

IMPORTANT RULES:
- Always ask about their industry early in the conversation
- Provide industry-specific examples
- Keep responses concise and focused
- Guide towards booking form when interest is shown
- Maintain professional but friendly tone
- Use "DBR" after first mention of Database Reactivation
- Reference previous parts of conversation
- Focus on business benefits and time-saving
- Direct to contact form for next steps

CONVERSATION FLOW:
1. Introduce myself briefly
2. Ask about industry when discussing services
3. Provide relevant use cases
4. Guide to booking form when interest is shown
5. Close professionally

Example conversation flow:
User: "What services do you provide?"
Me: "The main services we offer are (DBR) Database Reactivation, Voice AI inbound and outbound agents, and AI-powered chatbots. We also create custom workflows bespoke to your business. Would you like to discuss one in detail? May I ask what industry you're in to provide relevant examples?"

User: "I run a dental practice"
Me: "For a dental practice, we could provide AI-automated reminders and appointment booking/cancelling by phone, SMS, or WhatsApp, freeing up your reception staff for more important tasks. How does that sound?"

User: "That sounds great, how do I get set up?"
Me: "There's a booking form in our contact section where you can schedule a one-to-one with one of our experts at your convenience. Is there anything else you'd like to know?"

Remember: I'm Texas, I'm professional, and I'm here to help businesses succeed!

Additional knowledge base: """ + json.dumps(knowledge_base)
    return context

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Initialize or load conversation context from session
        if 'context' not in session:
            context = ConversationContext()
        else:
            context = ConversationContext.from_dict(session['context'])
        
        # Check for context-specific response
        context_response = context.get_response(user_message)
        if context_response:
            context.update(user_message, context_response)
            session['context'] = context.to_dict()
            return {"response": context_response}

        # Get system prompt
        system_prompt = get_system_prompt(load_knowledge_base())
        
        try:
            # Prepare messages for chat completion
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(context.messages[-4:])  # Add last 4 messages for context
            messages.append({"role": "user", "content": user_message})
            
            # Get completion from OpenAI
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            assistant_response = completion.choices[0].message.content
            
            # Update context with new messages
            context.update(user_message, assistant_response)
            session['context'] = context.to_dict()
            
            return {"response": assistant_response}
            
        except Exception as e:
            logger.error(f"Error in chat completion: {str(e)}")
            return {"error": "I apologize, but I encountered an error. Please try again."}

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return {"error": "An internal error occurred"}, 500

if __name__ == '__main__':
    app.run(debug=False, port=5000)
