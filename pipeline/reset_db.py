import os
import shutil
from config.paths import CHROMA_PATH, FEEDBACK_DIR_PATH


def reset_all_databases():
    """
    Reset all databases by clearing both embedding and feedback databases.
    """
    reset_embedding_database()
    reset_feedback_database()
    print("🗑️ All databases cleared.")


def reset_embedding_database():
    """
    Delete the Chroma vector store directory if it exists.
    """
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("🗑️ Embedding Vector Database cleared.")
    else:
        print("❗️ No embedding database found. Skipping.")


def reset_feedback_database():
    """
    Delete the feedback database if implemented.
    (Currently placeholder for future logic.)
    """
    if os.path.exists(FEEDBACK_DIR_PATH):
        shutil.rmtree(FEEDBACK_DIR_PATH)
        print("🗑️ Feedback Database cleared.")
    else:
        print("❗️ No feedback database found. Skipping.")
