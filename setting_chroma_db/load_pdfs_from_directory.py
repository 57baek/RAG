from langchain_community.document_loaders import PyPDFDirectoryLoader
from config.paths import DATA_PATH


def load_pdfs_from_directory():
    """Load all PDF documents from the specified directory."""
    loader = PyPDFDirectoryLoader(DATA_PATH)
    return loader.load()
