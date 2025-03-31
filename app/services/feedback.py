import os
import json

from ..configs.paths import FEEDBACK_PATH


def ensure_feedback_file_exists():
    """Ensure that the feedback directory and file exist."""
    os.makedirs(os.path.dirname(FEEDBACK_PATH), exist_ok=True)
    if not os.path.exists(FEEDBACK_PATH):
        with open(FEEDBACK_PATH, "w") as f:
            json.dump([], f)


def append_feedback(feedback_text: str) -> None:
    """Append new feedback to the feedback file."""
    ensure_feedback_file_exists()
    with open(FEEDBACK_PATH, "r") as f:
        feedback_list = json.load(f)
    feedback_list.append(feedback_text)
    with open(FEEDBACK_PATH, "w") as f:
        json.dump(feedback_list, f, indent=2)
    print("📖 Feedback saved.")


def load_all_feedback() -> str:
    """Load all feedback and return them as a concatenated string."""
    ensure_feedback_file_exists()
    with open(FEEDBACK_PATH, "r") as f:
        feedback_list = json.load(f)
    return "\n".join(feedback_list)
