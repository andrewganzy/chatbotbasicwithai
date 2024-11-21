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
                            <img src="https://ganzyistheone.pythonanywhere.com/static/images/logo_ccwith_ai.png" alt="CCwithAi" style="width: 24px; height: 24px; border-radius: 50%; object-fit: cover;">
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
                const response = await fetch('https://ganzyistheone.pythonanywhere.com/api/chat', {
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
