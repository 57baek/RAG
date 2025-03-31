from langchain_chroma import Chroma

from ..configs.paths import CHROMA_PATH
from ..models.embedding_model import get_embedding_model


def load_db():
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_model(),
    )
