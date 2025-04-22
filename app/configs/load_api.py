import os
from dotenv import load_dotenv
import openai
from Bio import Entrez

load_dotenv()

# OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in environment")

# NCBI Entrez
Entrez.email = os.getenv("NCBI_EMAIL")
if not Entrez.email:
    raise RuntimeError(
        "❌ Missing NCBI_EMAIL in environment. "
        "Set NCBI_EMAIL=your.email@institution.edu in your .env"
    )

Entrez.api_key = os.getenv("NCBI_API_KEY")
if not Entrez.api_key:
    print("⚠️  No NCBI_API_KEY provided; continuing with low rate limits.")
