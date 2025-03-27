from langchain_chroma import Chroma
from config.paths import CHROMA_PATH
from models.embedding_model import get_embedding_model


def retrieve_relevant_documents(query_text: str):
    """Search the vector DB and return top-K relevant documents based on query."""
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_model())
    results = db.similarity_search_with_score(query_text, k=3)

    if len(results) == 0 or results[0][1] < 0.7:
        print("❌ No sufficiently relevant results found.")
        return None

    return results
