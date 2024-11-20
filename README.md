# CC With AI Chatbot

A custom AI-powered chatbot for www.ccwithai.com that uses ChatGPT to provide responses based on stored knowledge.

## Features

- AI-powered responses using ChatGPT
- Custom knowledge base integration
- Modern chat interface using Deep Chat
- API endpoints for chat and knowledge base management

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Adding Knowledge

To add information to the knowledge base, send a POST request to `/api/add-knowledge` with JSON data:

```json
{
    "content": "Your knowledge content here"
}
```

## Usage

1. Access the chat interface at `http://localhost:5000`
2. Type your questions in the chat interface
3. The AI will respond based on the stored knowledge base

## Production Deployment

For production deployment:

1. Use a proper database instead of file-based storage
2. Implement proper security measures
3. Use a production-grade server like Gunicorn
4. Set up SSL/TLS for HTTPS
5. Implement proper error handling and logging
6. Add rate limiting and API key validation

## License

MIT License
