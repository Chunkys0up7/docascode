"""CLI for DocAsCode MCP Service."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from loguru import logger

from mcp_server.config import settings
from mcp_server.server import main as server_main

app = typer.Typer(help="DocAsCode MCP Service CLI")


@app.command()
def serve():
    """Start the MCP server."""
    logger.info("Starting MCP server...")
    asyncio.run(server_main())


@app.command()
def demo():
    """Run usage demonstrations."""
    from examples.usage_demo import main as demo_main

    logger.info("Running usage demonstrations...")
    asyncio.run(demo_main())


@app.command()
def init(
    directory: Optional[Path] = typer.Argument(
        None, help="Directory to initialize (default: current)"
    )
):
    """Initialize a new DocAsCode project."""
    base_dir = directory or Path.cwd()

    logger.info(f"Initializing DocAsCode project in {base_dir}")

    # Create directory structure
    dirs = [
        base_dir / "data" / "documents",
        base_dir / "data" / "graphs",
        base_dir / "data" / "indices",
        base_dir / "templates",
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"  ✓ Created {dir_path}")

    # Copy example files
    examples_src = Path(__file__).parent.parent / "examples"
    templates_src = Path(__file__).parent.parent / "templates"

    if examples_src.exists():
        import shutil

        # Copy graph example
        graph_file = examples_src / "mortgage_graph.json"
        if graph_file.exists():
            shutil.copy(graph_file, base_dir / "data" / "graphs")
            logger.info("  ✓ Copied example graph: mortgage_graph.json")

    if templates_src.exists():
        import shutil

        for template in templates_src.glob("*.j2"):
            shutil.copy(template, base_dir / "templates")
            logger.info(f"  ✓ Copied template: {template.name}")

    # Create .env file
    env_file = base_dir / ".env"
    if not env_file.exists():
        env_example = Path(__file__).parent.parent / ".env.example"
        if env_example.exists():
            import shutil

            shutil.copy(env_example, env_file)
            logger.info("  ✓ Created .env file")

    logger.info("\n✅ Project initialized successfully!")
    logger.info(
        "\nNext steps:\n"
        "  1. Edit .env to configure your settings\n"
        "  2. Run 'docascode-mcp demo' to see examples\n"
        "  3. Run 'docascode-mcp serve' to start the server"
    )


@app.command()
def info():
    """Show configuration and system information."""
    from mcp_server import __version__

    typer.echo(f"DocAsCode MCP Service v{__version__}")
    typer.echo(f"\nServer: {settings.server_name} v{settings.server_version}")
    typer.echo(f"Data directory: {settings.data_dir}")
    typer.echo(f"Templates directory: {settings.templates_dir}")
    typer.echo(f"Graph backend: {settings.graph_backend}")
    typer.echo(f"Embedding model: {settings.embedding_model}")
    typer.echo(f"NLP enabled: {settings.enable_nlp}")

    # Check if directories exist
    typer.echo("\nDirectories:")
    for dir_name in ["data_dir", "documents_dir", "graphs_dir", "templates_dir"]:
        dir_path = getattr(settings, dir_name)
        exists = "✓" if dir_path.exists() else "✗"
        typer.echo(f"  {exists} {dir_name}: {dir_path}")


def main():
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    main()
