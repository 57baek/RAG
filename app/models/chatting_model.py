from langchain_openai import ChatOpenAI


def get_chatting_model_openai():
    return ChatOpenAI(
        model="gpt-4o-mini",
        # Options: "gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"
    )
