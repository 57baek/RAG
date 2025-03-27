import click
import os
from config.paths import CHROMA_PATH
from pipeline.run_rag_pipeline import run_rag_pipeline
from pipeline.vectorization_pipeline import vectorization_pipeline
from pipeline.autoupdate_db import index_new_documents_to_chroma
from pipeline.feedback_pipeline import append_feedback
from pipeline import reset_db


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

    run_rag_pipeline(query_text)


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
        reset_db.reset_all_databases()
    elif em:
        reset_db.reset_embedding_database()
    elif fb:
        reset_db.reset_feedback_database()
    elif fi:
        reset_db.reset_fileindex_database()
    else:
        print("⚠️ Please specify what to reset. Use --all or a specific DB flag.")


if __name__ == "__main__":
    cli()
