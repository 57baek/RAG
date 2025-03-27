import os
import shutil
from config.paths import CHROMA_PATH


def reset_chroma_database():
    """Delete the existing Chroma database directory if it exists."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("🗑️ Database cleared.")
