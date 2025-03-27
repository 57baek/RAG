import click
import os
from config.paths import CHROMA_PATH
from pipeline.run_rag_pipeline import run_rag_pipeline
from pipeline.vectorization_pipeline import vectorization_pipeline
from pipeline.feedback_pipeline import append_feedback
from pipeline import reset_db


@click.group()
def cli():
    """🧠 CLI entrypoint for the Medical RAG Chatbot."""
    pass


@cli.command()
@click.argument("feedback_text")
def feedback(feedback_text):
    """Store user feedback for improving future responses."""
    append_feedback(feedback_text)


@cli.command()
@click.argument("query_text")
def ask(query_text):
    """❓ Ask a question and get an AI-generated answer from medical papers."""
    if not os.path.exists(CHROMA_PATH):
        print("🚨 Chroma vector database not found. Running vectorization pipeline...")
        vectorization_pipeline()
    run_rag_pipeline(query_text)


@cli.command()
@click.option("--all", is_flag=True, help="Reset all databases.")
@click.option("--em", is_flag=True, help="Reset embedding vector DB.")
@click.option("--fb", is_flag=True, help="Reset feedback DB.")
def reset(all, em, fb):
    """♻️ Flexible reset: embedding DB, feedback DB, or both."""
    if all:
        reset_db.reset_all_databases()
    elif em:
        reset_db.reset_embedding_database()
    elif fb:
        reset_db.reset_feedback_database()
    else:
        print("⚠️ Please specify what to reset. Use --all or a specific DB flag.")
