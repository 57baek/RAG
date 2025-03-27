from langchain_openai import ChatOpenAI


def get_chatting_model():
    return ChatOpenAI(
        model="gpt-4o",
        # Options: "gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo",
    )
