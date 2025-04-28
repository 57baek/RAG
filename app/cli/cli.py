import click
import os

from ..configs.paths import CHROMA_PATH
from ..configs.paths import DATA_PATH
from ..core.pubmed_fetcher import (
    rewrite_pubmed_query,
    fetch_top_k_pmc_papers,
    download_xml,
)
from ..core.rag import rag_pipeline
from ..core.preprocessing import vectorization_pipeline
from ..services.auto_update import index_new_documents_to_chroma
from ..services.feedback import append_feedback
from ..services import reset_database


@click.group()
def cli():
    """🧠 CLI entrypoint for the Medical RAG Chatbot."""
    pass


@cli.command()
@click.argument("query_text")
def query(query_text):
    cleaned_query = rewrite_pubmed_query(query_text)

    pmcid_list = fetch_top_k_pmc_papers(cleaned_query)

    download_xml(pmcid_list)


@cli.command()
@click.argument("ask_text")
def ask(ask_text):
    """
    🙋 Ask a question and get an AI-generated answer from medical papers.

    First, it checks whether the Chroma vector DB exists.
    - If not, it runs the full vectorization pipeline.
    - Otherwise, it checks for new/updated PDFs and indexes them.

    Then it runs the full RAG pipeline.
    """

    if not os.path.exists(CHROMA_PATH):
        print("🚨 Chroma vector database not found. Running initial vectorization...")
        vectorization_pipeline()
    else:
        print("🔄 Checking for new or updated PDFs...")
        index_new_documents_to_chroma()

    rag_pipeline(ask_text)


@cli.command()
@click.argument("feedback_text")
def feedback(feedback_text):
    """📚 Store user feedback for improving future responses."""
    append_feedback(feedback_text)


@cli.command()
@click.option("--all", is_flag=True, help="Reset all databases.")
@click.option("--db", is_flag=True, help="Reset data DB.")
@click.option("--em", is_flag=True, help="Reset embedding vector DB.")
@click.option("--fb", is_flag=True, help="Reset feedback DB.")
@click.option("--fi", is_flag=True, help="Reset file index database.")
def reset(all, db, em, fb, fi):
    """🧹 Flexible reset: embedding DB, feedback DB, or file index."""
    if all:
        reset_database.reset_all_databases()
    elif db:
        reset_database.reset_data_database()
    elif em:
        reset_database.reset_embedding_database()
    elif fb:
        reset_database.reset_feedback_database()
    elif fi:
        reset_database.reset_fileindex_database()
    else:
        print(
            "⚠️ Please specify what to reset. Use --all or a specific DB flag (db, em, fb, fi)."
        )
