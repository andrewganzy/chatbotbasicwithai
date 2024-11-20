(function() {
    console.log('Chat widget script loaded');
    // Wait for DOM to be fully loaded
    function initChatWidget() {
        console.log('Initializing chat widget');
        const chatWidget = document.createElement('div');
        chatWidget.innerHTML = `
            <div id="cc-chat-widget" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
                <div id="chat-container" style="display: none; width: 350px; height: 500px; background: white; border: 1px solid #ccc; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                    <div style="padding: 10px; background: #007bff; color: white; border-radius: 10px 10px 0 0; display: flex; justify-content: space-between;">
                        <span>CC With AI Assistant</span>
                        <button onclick="toggleChat()" style="background: none; border: none; color: white; cursor: pointer;">×</button>
                    </div>
                    <div id="messages" style="height: 380px; overflow-y: auto; padding: 10px;"></div>
                    <div style="padding: 10px; border-top: 1px solid #eee;">
                        <input type="text" id="message-input" placeholder="Type your message..." style="width: 80%; padding: 5px; border: 1px solid #ccc; border-radius: 3px;">
                        <button onclick="sendMessage()" style="width: 15%; padding: 5px; background: #007bff; color: white; border: none; border-radius: 3px; margin-left: 5px;">→</button>
                    </div>
                </div>
                <button onclick="toggleChat()" style="float: right; padding: 15px 25px; background: #007bff; color: white; border: none; border-radius: 25px; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    Chat with AI
                </button>
            </div>
        `;
        console.log('Appending chat widget to body');
        document.body.appendChild(chatWidget);
        console.log('Chat widget appended');

        window.toggleChat = function() {
            const container = document.getElementById('chat-container');
            container.style.display = container.style.display === 'none' ? 'block' : 'none';
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
            messageDiv.style.marginBottom = '10px';
            messageDiv.style.padding = '10px';
            messageDiv.style.borderRadius = '5px';
            
            if (role === 'user') {
                messageDiv.style.backgroundColor = '#007bff';
                messageDiv.style.color = 'white';
                messageDiv.style.marginLeft = '20%';
            } else {
                messageDiv.style.backgroundColor = '#f1f1f1';
                messageDiv.style.marginRight = '20%';
            }
            
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

    // Check if DOM is already loaded
    if (document.readyState === 'loading') {
        console.log('DOM not ready, adding event listener');
        document.addEventListener('DOMContentLoaded', initChatWidget);
    } else {
        console.log('DOM ready, initializing immediately');
        initChatWidget();
    }
})();
