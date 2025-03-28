import os
import openai
from dotenv import load_dotenv

# Load the .env file for the API key
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
