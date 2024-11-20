import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Basic Flask config
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # OpenAI config
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # CORS settings - replace with your actual domain
    CORS_ORIGINS = [
        'http://localhost:5000',
        'https://www.ccwithai.com',
        'https://ccwithai.com'
    ]
    
    # ChatGPT settings
    CHATGPT_MODEL = 'gpt-3.5-turbo'
    CHATGPT_TEMPERATURE = 0.7
    CHATGPT_MAX_TOKENS = 500
    
    # Production settings
    PRODUCTION_URL = 'https://www.ccwithai.com'
