# Complete Guide: Building Your Own CCwithAI ChatGPT Integration

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setting Up Development Environment](#setting-up-development-environment)
3. [Setting Up PythonAnywhere](#setting-up-pythonanywhere)
4. [Project Setup](#project-setup)
5. [Building the Backend](#building-the-backend)
6. [Creating the Chat Widget](#creating-the-chat-widget)
7. [Deployment](#deployment)
8. [Customization](#customization)
9. [Troubleshooting](#troubleshooting)

## Prerequisites
- Basic understanding of Python and JavaScript
- OpenAI API key (from [OpenAI Platform](https://platform.openai.com))
- Text editor or IDE (VS Code recommended)
- Git installed on your computer
- Python 3.7+ installed

## Setting Up Development Environment

### 1. Install Windsurf
1. Download Windsurf from the official website
2. Install and open Windsurf
3. Create a new project directory:
```bash
mkdir ccwithai-chatbot
cd ccwithai-chatbot
```

### 2. Set Up Python Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Required Packages
Create a `requirements.txt` file with these dependencies:
```
flask==2.3.3
openai==0.28.0
python-dotenv==1.0.0
flask-cors==4.0.0
```

Install the packages:
```bash
pip install -r requirements.txt
```

## Setting Up PythonAnywhere

### 1. Create PythonAnywhere Account
1. Go to [PythonAnywhere](https://www.pythonanywhere.com)
2. Sign up for a free account
3. Note your username (you'll need it later)

### 2. Set Up Web App
1. Go to Web tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.8
5. Note the domain name: `yourusername.pythonanywhere.com`

## Project Setup

### 1. Create Project Structure
```
ccwithai-chatbot/
├── static/
│   ├── images/
│   │   └── logo_ccwith_ai.png
│   ├── chat-widget.js
│   └── index.html
├── app.py
├── .env
└── requirements.txt
```

### 2. Set Up Environment Variables
Create `.env` file:
```
OPENAI_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

## Building the Backend

### 1. Create Flask Application (app.py)
```python
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')
openai.api_key = os.getenv('OPENAI_API_KEY')

class ConversationContext:
    def __init__(self):
        self.industry = None
        self.services_discussed = set()
        self.conversation_history = []
        self.max_history = 4

    def to_dict(self):
        return {
            'industry': self.industry,
            'services_discussed': list(self.services_discussed),
            'conversation_history': self.conversation_history
        }

    @classmethod
    def from_dict(cls, data):
        context = cls()
        context.industry = data.get('industry')
        context.services_discussed = set(data.get('services_discussed', []))
        context.conversation_history = data.get('conversation_history', [])
        return context

    def add_message(self, role, content):
        self.conversation_history.append({'role': role, 'content': content})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Empty message'}), 400

        # Initialize or load conversation context
        context = ConversationContext.from_dict(session.get('context', {}))
        
        # Add user message to context
        context.add_message('user', message)
        
        # Prepare messages for OpenAI
        messages = [
            {'role': 'system', 'content': 'You are a helpful AI assistant for CCwithAI, a recruitment and business services company. Be professional, concise, and helpful.'}
        ]
        messages.extend(context.conversation_history)
        
        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message['content'].strip()
        
        # Add assistant response to context
        context.add_message('assistant', assistant_message)
        
        # Save context to session
        session['context'] = context.to_dict()
        
        return jsonify({'response': assistant_message})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

## Creating the Chat Widget

### 1. Create HTML Template (static/index.html)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CCwithAI ChatGPT Integration</title>
</head>
<body>
    <h1>CCwithAI ChatGPT Integration Test Page</h1>
    <script src="/static/chat-widget.js"></script>
</body>
</html>
```

### 2. Create Chat Widget (static/chat-widget.js)
```javascript
(function() {
    console.log('Chat widget script loaded');
    
    function initChatWidget() {
        console.log('Initializing chat widget');
        const chatWidget = document.createElement('div');
        chatWidget.innerHTML = `
            <div id="cc-chat-widget" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; font-family: Arial, sans-serif;">
                <div id="chat-container" style="display: none; width: 380px; height: 600px; background: white; border-radius: 15px; box-shadow: 0 5px 25px rgba(0,0,0,0.2); overflow: hidden;">
                    <div style="padding: 15px; background: linear-gradient(135deg, #004225, #015c34); color: white; display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <img src="https://yourusername.pythonanywhere.com/static/images/logo_ccwith_ai.png" alt="CCwithAi" style="width: 24px; height: 24px; border-radius: 50%; object-fit: cover;">
                            <span style="font-size: 18px; font-weight: bold;">CCwithAi ChatGPT</span>
                        </div>
                        <button onclick="toggleChat()" style="background: none; border: none; color: white; cursor: pointer; font-size: 24px; padding: 0 5px;">×</button>
                    </div>
                    <div id="messages" style="height: 480px; overflow-y: auto; padding: 20px; scroll-behavior: smooth;"></div>
                    <div style="padding: 15px; border-top: 1px solid #eee; background: #f8f9fa;">
                        <div style="display: flex; gap: 10px;">
                            <input type="text" id="message-input" placeholder="Type your message..." 
                                style="flex: 1; padding: 12px; border: 1px solid #dee2e6; border-radius: 25px; outline: none; font-size: 14px;">
                            <button onclick="sendMessage()" 
                                style="background: linear-gradient(135deg, #004225, #015c34); color: white; border: none; border-radius: 50%; width: 45px; height: 45px; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <line x1="22" y1="2" x2="11" y2="13"></line>
                                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
                <button onclick="toggleChat()" 
                    style="float: right; padding: 15px 25px; background: linear-gradient(135deg, #004225, #015c34); color: white; border: none; border-radius: 25px; cursor: pointer; box-shadow: 0 2px 15px rgba(0,0,0,0.1); font-size: 16px; font-weight: bold; display: flex; align-items: center; gap: 10px;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                    Chat with AI
                </button>
            </div>
        `;
        
        document.body.appendChild(chatWidget);

        window.toggleChat = function() {
            const container = document.getElementById('chat-container');
            const button = document.querySelector('#cc-chat-widget > button');
            if (container.style.display === 'none') {
                container.style.display = 'block';
                button.style.display = 'none';
            } else {
                container.style.display = 'none';
                button.style.display = 'block';
            }
        };

        window.sendMessage = async function() {
            const messageInput = document.getElementById('message-input');
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            messageInput.value = '';

            try {
                const response = await fetch('https://yourusername.pythonanywhere.com/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message })
                });
                const data = await response.json();
                addMessage(data.response, 'assistant');
            } catch (error) {
                console.error('Chat error:', error);
                addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
            }
        };

        function addMessage(text, role) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.style.cssText = `
                margin-bottom: 15px;
                padding: 12px 16px;
                border-radius: 15px;
                max-width: 85%;
                word-wrap: break-word;
                line-height: 1.4;
                font-size: 14px;
                ${role === 'user' ? 
                    'background: linear-gradient(135deg, #004225, #015c34); color: white; margin-left: auto;' : 
                    'background: #f1f3f5; color: #343a40; margin-right: auto;'}
            `;
            
            messageDiv.textContent = text;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        // Add initial message
        addMessage("Hello! I am the CC With AI Assistant. How can I help you today?", 'assistant');

        // Add Enter key support
        document.getElementById('message-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatWidget);
    } else {
        initChatWidget();
    }
})();
```

## Deployment

### 1. Upload Files to PythonAnywhere
1. Go to Files tab in PythonAnywhere
2. Create directory structure matching local setup
3. Upload all files to corresponding locations
4. Make sure to update the logo URL in chat-widget.js to match your PythonAnywhere username

### 2. Configure Web App
1. Go to Web tab
2. Under "Code" section, set:
   - Source code: /home/yourusername/ccwithai-chatbot
   - Working directory: /home/yourusername/ccwithai-chatbot
3. Under "WSGI configuration file", click and edit:
```python
import sys
path = '/home/yourusername/ccwithai-chatbot'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### 3. Set Environment Variables
1. Go to Web tab
2. Under "Environment variables", add:
   - OPENAI_API_KEY
   - FLASK_SECRET_KEY

### 4. Install Requirements
In PythonAnywhere bash console:
```bash
cd ccwithai-chatbot
pip3 install --user -r requirements.txt
```

### 5. Reload Web App
Click the green "Reload" button in the Web tab

## Customization

### 1. Styling
- British Racing Green colors used: #004225 (dark) and #015c34 (light)
- Modify gradients and colors in chat-widget.js
- Adjust widget size and positioning

### 2. Behavior
- Modify max_history in ConversationContext class
- Adjust OpenAI parameters (temperature, max_tokens)
- Customize system prompt

### 3. Features
- Add typing indicators
- Implement message persistence
- Add support for attachments

## Troubleshooting

### Common Issues:
1. **Widget Not Loading**
   - Check browser console for errors
   - Verify file paths and permissions
   - Check if JavaScript is enabled

2. **API Errors**
   - Verify OpenAI API key
   - Check PythonAnywhere error logs
   - Verify CORS settings

3. **Styling Issues**
   - Clear browser cache
   - Check CSS syntax
   - Verify image paths

### Debug Tips:
1. Use browser developer tools
2. Check PythonAnywhere error logs
3. Test API endpoints using Postman
4. Verify environment variables

## Next Steps
1. Add authentication
2. Implement rate limiting
3. Add analytics
4. Enhance error handling
5. Add more interactive features

Remember to replace `yourusername` with your actual PythonAnywhere username throughout the code.
