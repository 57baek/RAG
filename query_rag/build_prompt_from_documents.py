from langchain.prompts import ChatPromptTemplate
from config.prompts import PROMPT_TEMPLATE


def build_prompt_from_documents(results, query_text: str):
    """Format the retrieved documents and query into a prompt for the LLM."""
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    return prompt_template.format(context=context_text, question=query_text)
