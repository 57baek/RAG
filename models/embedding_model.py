from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.ollama import OllamaEmbeddings


def get_embedding_model():
    return OpenAIEmbeddings(
        model="text-embedding-3-large"
        # Options: "text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"
    )


def get_local_embedding_model():
    return OllamaEmbeddings(model="nomic-embed-text")
