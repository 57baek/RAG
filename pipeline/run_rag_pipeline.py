from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from models.chatting_model import get_chatting_model
from models.embedding_model import get_embedding_model
from config.prompts import PROMPT_TEMPLATE
from config.paths import CHROMA_PATH


def run_rag_pipeline(query_text: str) -> str:
    """Run the full RAG (Retrieval-Augmented Generation) pipeline on a user query."""

    # Step 1: Load the Chroma vector DB and perform similarity search
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_model())

    results = db.similarity_search_with_score(query_text, k=3)

    if not results or results[0][1] < 0.7:
        print("⚠️ No sufficiently relevant documents found.")
        return ""

    # Step 2: Construct prompt from retrieved documents
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Step 3: Generate answer with Ollama LLM
    llm = get_chatting_model()
    response = llm.invoke(prompt)
    response = response.content


    # Step 4: Print formatted response and source info
    sources = [doc.metadata.get("id", "N/A") for doc, _ in results]
    print("\n🧠 Prompt:\n", prompt)
    print("\n📜 Response:\n", response)
    print("\n🔗 Sources:", sources)

    return response
