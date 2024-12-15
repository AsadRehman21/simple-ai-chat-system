import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """ Configuration class for loading environment variables """

    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")