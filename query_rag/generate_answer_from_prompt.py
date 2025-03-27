from models.chatting_model import get_chatting_model


def generate_answer_from_prompt(results, prompt):
    """Generate an LLM response using the prompt, and print source metadata."""
    model = get_chatting_model()
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"🧠 Response:\n{response_text}\n\n📚 Sources: {sources}"
    print(formatted_response)

    return response_text
