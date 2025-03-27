from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document


def split_documents_into_chunks(documents: list[Document]):
    """Split loaded documents into smaller overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return splitter.split_documents(documents)
