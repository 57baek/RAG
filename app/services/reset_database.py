import os
import shutil
from pathlib import Path

from ..configs.paths import DATA_PATH, CHROMA_PATH, FEEDBACK_PATH, FILEINDEX_PATH


def reset_data_database():
    """
    Delete all files in the paper DB directory except '.gitkeep'.
    """
    data_dir = Path(DATA_PATH)

    if not data_dir.exists():
        print("❗️ Paper DB directory does not exist. Skipping.")
        return

    deleted_any = False

    for file in data_dir.iterdir():
        if file.name != ".gitkeep" and file.is_file():
            file.unlink()
            print(f"🗑️ Deleted {file.name}")
            deleted_any = True

    if not deleted_any:
        print("✅ Paper DB was already clean.")
    else:
        print("🧹 Paper DB cleaned successfully.")


def reset_embedding_database():
    """
    Delete the Chroma vector store directory if it exists.
    """
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("🧹 Embedding Vector Database cleared.")
    else:
        print("❗️ No embedding database found. Skipping.")


def reset_feedback_database():
    """
    Delete the feedback database if implemented.
    """
    if os.path.exists(os.path.dirname(FEEDBACK_PATH)):
        shutil.rmtree(os.path.dirname(FEEDBACK_PATH))
        print("🧹 Feedback Database cleared.")
    else:
        print("❗️ No feedback database found. Skipping.")


def reset_fileindex_database():
    """
    Delete the fileindex for auto-update vector database if implemented.
    """
    if os.path.exists(os.path.dirname(FILEINDEX_PATH)):
        shutil.rmtree(os.path.dirname(FILEINDEX_PATH))
        print("🧹 Fileindex Database cleared.")
    else:
        print("❗️ No fileindex database found. Skipping.")


def reset_all_databases():
    """
    Reset all databases by clearing both embedding and feedback databases.
    """
    reset_data_database()
    reset_embedding_database()
    reset_feedback_database()
    reset_fileindex_database()
    print("🧹 All databases cleared.")
