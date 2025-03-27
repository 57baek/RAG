from langchain_chroma import Chroma
from models.embedding_model import get_embedding_model
from setting_chroma_db.assign_unique_chunk_ids import assign_unique_chunk_ids
from langchain.schema.document import Document
from config.paths import CHROMA_PATH


def add_chunks_to_chroma_db(chunks: list[Document]):
    """Add new document chunks to the Chroma vector database."""
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_model())

    chunks_with_ids = assign_unique_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"📦 Existing documents in DB: {len(existing_ids)}")

    new_chunks = [
        chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids
    ]

    if new_chunks:
        print(f"🆕 Adding {len(new_chunks)} new chunks to DB...")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add.")
