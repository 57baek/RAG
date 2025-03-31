import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

from ..configs.paths import DATA_PATH
from ..configs.database import load_db


def load_pdfs_from_directory() -> list[Document]:
    """Load PDF documents from the data directory."""
    loader = PyPDFDirectoryLoader(DATA_PATH)
    return loader.load()


def split_documents_into_chunks(documents: list[Document]) -> list[Document]:
    """Split documents into smaller overlapping chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False,
    )
    return splitter.split_documents(documents)


def assign_unique_chunk_ids(chunks: list[Document]) -> list[Document]:
    """Assign unique metadata IDs to each chunk (source:page:index)."""
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"[Source: {os.path.basename(source)} || Page: {page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk.metadata["id"] = f"{current_page_id} || Index: {current_chunk_index}]"
        last_page_id = current_page_id

    return chunks


def add_and_vectorize_new_chunks_to_db(chunks: list[Document]):
    """Add new (non-duplicate) chunks to the vector database."""
    db = load_db()

    chunks = assign_unique_chunk_ids(chunks)
    existing_ids = set(db.get(include=[])["ids"])
    print(f"📦 Existing documents in DB: {len(existing_ids)}")

    new_chunks = [chunk for chunk in chunks if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        print(f"🆕 Adding {len(new_chunks)} new chunks...")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add.")


def vectorization_pipeline():
    documents = load_pdfs_from_directory()
    chunks = split_documents_into_chunks(documents)
    add_and_vectorize_new_chunks_to_db(chunks)
