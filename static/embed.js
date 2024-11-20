class CCWithAIChat {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || 'https://your-api-url.com';
        this.position = options.position || 'right';
        this.createChatWidget();
    }

    createChatWidget() {
        // Create chat button
        const button = document.createElement('div');
        button.innerHTML = `
            <div id="cc-chat-button" style="
                position: fixed;
                bottom: 20px;
                ${this.position}: 20px;
                background-color: #007bff;
                color: white;
                padding: 15px;
                border-radius: 50%;
                cursor: pointer;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                z-index: 1000;
                width: 60px;
                height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
            </div>
        `;

        // Create chat window
        const chatWindow = document.createElement('div');
        chatWindow.innerHTML = `
            <div id="cc-chat-window" style="
                display: none;
                position: fixed;
                bottom: 100px;
                ${this.position}: 20px;
                width: 380px;
                height: 600px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.15);
                z-index: 1000;
                overflow: hidden;
            ">
                <iframe 
                    src="${this.apiUrl}"
                    style="
                        width: 100%;
                        height: 100%;
                        border: none;
                    "
                ></iframe>
            </div>
        `;

        document.body.appendChild(button);
        document.body.appendChild(chatWindow);

        // Add click handler
        const chatBtn = document.getElementById('cc-chat-button');
        const chatWin = document.getElementById('cc-chat-window');
        
        chatBtn.addEventListener('click', () => {
            if (chatWin.style.display === 'none') {
                chatWin.style.display = 'block';
                chatBtn.style.backgroundColor = '#0056b3';
            } else {
                chatWin.style.display = 'none';
                chatBtn.style.backgroundColor = '#007bff';
            }
        });
    }
}

// Usage example:
// new CCWithAIChat({
//     apiUrl: 'https://your-chatbot-url.com',
//     position: 'right' // or 'left'
// });
