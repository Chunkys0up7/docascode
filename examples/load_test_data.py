"""Load test data into the MCP service.

This script loads all example graphs and sample documents into the service
for testing and demonstration purposes.
"""

import asyncio
import shutil
from pathlib import Path

from loguru import logger

from mcp_server.config import settings
from mcp_server.tools import catalogue_document


async def load_graphs():
    """Copy example graphs to the graphs directory."""
    logger.info("Loading example graphs...")

    examples_dir = Path("examples")
    graphs_dir = settings.graphs_dir
    graphs_dir.mkdir(parents=True, exist_ok=True)

    graph_files = [
        "mortgage_graph.json",
        "it_onboarding_graph.json",
        "software_dev_graph.json",
        "compliance_graph.json",
    ]

    for graph_file in graph_files:
        source = examples_dir / graph_file
        if source.exists():
            dest = graphs_dir / graph_file
            shutil.copy(source, dest)
            logger.info(f"  ✓ Loaded: {graph_file}")
        else:
            logger.warning(f"  ✗ Not found: {graph_file}")

    logger.success(f"Loaded {len(graph_files)} graphs to {graphs_dir}")


async def load_documents():
    """Load sample documents and catalogue them."""
    logger.info("Loading and cataloguing sample documents...")

    documents = [
        {
            "file": "examples/sample_documents/security_policy.md",
            "title": "Information Security Policy",
            "metadata": {
                "author": "CISO",
                "tags": ["security", "policy", "compliance"],
                "description": "Comprehensive information security policy",
            },
        },
        {
            "file": "examples/sample_documents/developer_guide.md",
            "title": "Developer Onboarding Guide",
            "metadata": {
                "author": "Engineering Team",
                "tags": ["developer", "onboarding", "guide"],
                "description": "Complete guide for new developers",
            },
        },
        {
            "file": "examples/sample_documents/api_documentation.md",
            "title": "API Documentation",
            "metadata": {
                "author": "API Team",
                "tags": ["api", "documentation", "reference"],
                "description": "REST API reference documentation",
            },
        },
        {
            "file": "examples/sample_documents/gdpr_compliance.md",
            "title": "GDPR Compliance Guide",
            "metadata": {
                "author": "Data Privacy Officer",
                "tags": ["gdpr", "compliance", "privacy", "legal"],
                "description": "Guide to GDPR compliance requirements",
            },
        },
        {
            "file": "examples/sample_documents/incident_response.md",
            "title": "Incident Response Plan",
            "metadata": {
                "author": "CISO",
                "tags": ["security", "incident response", "procedures"],
                "description": "Comprehensive incident response procedures",
            },
        },
    ]

    catalogued = 0
    for doc in documents:
        file_path = Path(doc["file"])
        if not file_path.exists():
            logger.warning(f"  ✗ Not found: {doc['file']}")
            continue

        content = file_path.read_text(encoding="utf-8")

        result = await catalogue_document(
            content=content,
            title=doc["title"],
            format="markdown",
            metadata=doc["metadata"],
        )

        if result["success"]:
            logger.info(f"  ✓ Catalogued: {doc['title']} (ID: {result['document_id']})")
            catalogued += 1
        else:
            logger.error(f"  ✗ Failed: {doc['title']} - {result.get('error')}")

    logger.success(f"Catalogued {catalogued}/{len(documents)} documents")


async def load_templates():
    """Copy example templates to the templates directory."""
    logger.info("Loading example templates...")

    templates_src = Path("templates")
    templates_dest = settings.templates_dir
    templates_dest.mkdir(parents=True, exist_ok=True)

    if not templates_src.exists():
        logger.warning("Templates directory not found")
        return

    template_files = list(templates_src.glob("*.j2"))

    for template_file in template_files:
        dest = templates_dest / template_file.name
        if not dest.exists():
            shutil.copy(template_file, dest)
            logger.info(f"  ✓ Loaded: {template_file.name}")

    logger.success(f"Loaded {len(template_files)} templates to {templates_dest}")


async def main():
    """Load all test data."""
    logger.info("=" * 60)
    logger.info("Loading Test Data into DocAsCode MCP Service")
    logger.info("=" * 60)

    # Ensure directories exist
    settings.ensure_directories()

    # Load all data
    await load_graphs()
    await load_templates()
    await load_documents()

    logger.info("=" * 60)
    logger.success("Test data loaded successfully!")
    logger.info("=" * 60)

    # Print summary
    logger.info("\nLoaded Data Summary:")
    logger.info(f"  Graphs: {settings.graphs_dir}")
    logger.info(f"  Templates: {settings.templates_dir}")
    logger.info(f"  Documents: Indexed in ChromaDB")

    logger.info("\nNext Steps:")
    logger.info("  1. Run 'python examples/usage_demo.py' to see tools in action")
    logger.info("  2. Start MCP server: 'python -m mcp_server.server'")
    logger.info("  3. Use with Claude Desktop")


if __name__ == "__main__":
    asyncio.run(main())
