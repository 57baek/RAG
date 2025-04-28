import os
import json
import hashlib

from ..configs.paths import DATA_PATH, FILEINDEX_PATH
from ..services.XMLDirectoryLoader import XMLDirectoryLoader
from ..core import preprocessing


def generate_file_hash(filepath: str) -> str:
    """Generate an MD5 hash for the contents of a file."""
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def get_new_or_updated_xmls() -> list[str]:
    """
    Compare current XML files in DATA_PATH with previously indexed ones.
    Returns a list of new or modified XML filenames.
    """
    # Ensure the directory for the record file exists
    os.makedirs(os.path.dirname(FILEINDEX_PATH), exist_ok=True)

    if os.path.exists(FILEINDEX_PATH):
        with open(FILEINDEX_PATH, "r") as f:
            indexed_files = json.load(f)
    else:
        indexed_files = {}

    current_files = {}
    modified_files = []

    for filename in os.listdir(DATA_PATH):
        if not filename.endswith(".xml"):
            continue
        full_path = os.path.join(DATA_PATH, filename)
        file_hash = generate_file_hash(full_path)
        current_files[filename] = file_hash

        if filename not in indexed_files or indexed_files[filename] != file_hash:
            modified_files.append(filename)

    # Save updated hash map to record file
    with open(FILEINDEX_PATH, "w") as f:
        json.dump(current_files, f, indent=2)

    return modified_files


def index_new_documents_to_chroma():
    """
    Check for new or updated XMLs, and index only those into Chroma.
    """
    updated_files = get_new_or_updated_xmls()

    if not updated_files:
        print("✅ No new or modified XMLs found.")
        return

    print(f"📂 XMLs to index: {updated_files}")

    # Load all docs, but keep only new/updated ones
    loader = XMLDirectoryLoader(DATA_PATH)
    all_documents = loader.load()

    filtered_docs = [
        doc
        for doc in all_documents
        if os.path.basename(doc.metadata.get("source", "")) in updated_files
    ]

    if not filtered_docs:
        print("⚠️ No valid content found in the changed documents.")
        return

    chunks = preprocessing.split_documents_into_chunks(filtered_docs)
    preprocessing.add_and_vectorize_new_chunks_to_db(chunks)

    print("✅ Successfully added new documents to Chroma vector database.")
