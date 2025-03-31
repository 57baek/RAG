from langchain_chroma import Chroma

from .paths import CHROMA_PATH
from ..models.embedding_model import get_embedding_model_openai


def load_db_chroma():
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_model_openai(),
    )
