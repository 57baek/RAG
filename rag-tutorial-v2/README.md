# rag-tutorial-v2


import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']



from langchain_community.llms import Ollama
llm = Ollama(model = "deepseek-r1:7b")
result = llm.invoke("What is the capital of France?")
print(result)