from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from models.chatting_model import get_chatting_model
from models.embedding_model import get_embedding_model
from pipeline.feedback_pipeline import load_all_feedback
from config.prompts import PROMPT_TEMPLATE
from config.paths import CHROMA_PATH


def run_rag_pipeline(query_text: str) -> str:
    """Run the full Retrieval-Augmented Generation (RAG) pipeline on the query."""
    results = load_relevant_documents_with_top_k(query_text)

    if not results or results[0][1] < 1.0:
        print("⚠️ No sufficiently relevant documents found.")
        return

    prompt = format_prompt_from_documents(results, query_text)
    response = generate_llm_response(prompt)
    print_response_with_sources(prompt, results, response)

    return response


def load_relevant_documents_with_top_k(query_text: str, k: int = 3):
    """Search Chroma vector DB for top-k relevant documents based on the query."""
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_model())
    results = db.similarity_search_with_score(query_text, k=k)
    return results


def format_prompt_from_documents(results, query_text: str) -> str:
    """Construct a formatted prompt from the retrieved documents."""
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    feedback_text = load_all_feedback()
    prompt = prompt_template.format(
        context=context_text, question=query_text, feedback=feedback_text
    )
    return prompt


def generate_llm_response(prompt: str) -> str:
    """Invoke the LLM with the generated prompt and return its response."""
    model = get_chatting_model()
    response = model.invoke(prompt)
    return response.content


def print_response_with_sources(prompt, results, response: str) -> None:
    """Display the final response and source document identifiers."""
    sources = [doc.metadata.get("id", "N/A") for doc, _ in results]
    print("\n🧠 Prompt:\n", prompt)
    print("\n📜 Response:\n", response)
    print("\n🔗 Sources:", sources)
