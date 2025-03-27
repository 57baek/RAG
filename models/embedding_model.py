from langchain_openai import OpenAIEmbeddings


def get_embedding_model():
    return OpenAIEmbeddings(
        model="text-embedding-3-small"
        # Options: "text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"
    )


"""
from langchain_community.embeddings.ollama import OllamaEmbeddings


def get_embedding_function():
    embeddings = OllamaEmbeddings(
        model = "nomic-embed-text"
    )
    return embeddings
"""
