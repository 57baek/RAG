import click
from setting_chroma_db.reset_chroma_database import reset_chroma_database


@click.group()
def cli():
    """CLI entry point for managing the vector database."""
    pass


@cli.command()
@click.option(
    "--reset", is_flag=True, help="Reset the database by clearing all stored vectors."
)
def create(reset):
    """Create or reset the vector database."""
    if reset:
        print("🧹 Clearing Database")
        reset_chroma_database()
    print("✅ Database created (or updated)")


@cli.command()
@click.option(
    "--reset", is_flag=True, help="Reset the database before generating fake data."
)
def fake(reset):
    """Simulate fake document creation."""
    if reset:
        print("🧹 Resetting before fake generation...")
        # clear_database()
    print("🚧 Not implemented yet — fake data generation coming soon!")
