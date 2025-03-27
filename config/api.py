import os
from dotenv import load_dotenv
import openai

# Load the .env file for the API key
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
