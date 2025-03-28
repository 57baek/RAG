import os
import shutil
from config.paths import CHROMA_PATH, FEEDBACK_PATH, FILEINDEX_PATH


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
    reset_embedding_database()
    reset_feedback_database()
    reset_fileindex_database()
    print("🧹 All databases cleared.")
