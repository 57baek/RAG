import click
import os
from config.paths import CHROMA_PATH
from pipeline.rag_pipeline import rag_pipeline
from pipeline.vectorization_pipeline import vectorization_pipeline
from pipeline.autoupdate_database import index_new_documents_to_chroma
from pipeline.feedback_pipeline import append_feedback
from pipeline import reset_database


@click.group()
def cli():
    """🧠 CLI entrypoint for the Medical RAG Chatbot."""
    pass


@cli.command()
@click.argument("query_text")
def ask(query_text):
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

    rag_pipeline(query_text)


@cli.command()
@click.argument("feedback_text")
def feedback(feedback_text):
    """📚 Store user feedback for improving future responses."""
    append_feedback(feedback_text)


@cli.command()
@click.option("--all", is_flag=True, help="Reset all databases.")
@click.option("--em", is_flag=True, help="Reset embedding vector DB.")
@click.option("--fb", is_flag=True, help="Reset feedback DB.")
@click.option("--fi", is_flag=True, help="Reset file index database.")
def reset(all, em, fb, fi):
    """🧹 Flexible reset: embedding DB, feedback DB, or file index."""
    if all:
        reset_database.reset_all_databases()
    elif em:
        reset_database.reset_embedding_database()
    elif fb:
        reset_database.reset_feedback_database()
    elif fi:
        reset_database.reset_fileindex_database()
    else:
        print("⚠️ Please specify what to reset. Use --all or a specific DB flag.")
