from langchain_openai import ChatOpenAI


def get_chatting_model():
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        # Options: "gpt-4o-mini", "gpt-4o"
    )
