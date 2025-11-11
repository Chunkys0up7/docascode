"""Comprehensive test of all MCP tools with example data.

This script demonstrates all 8 tools working with the loaded test data.
"""

import asyncio
import json
from pathlib import Path

from loguru import logger

from mcp_server.config import settings
from mcp_server.tools import (
    catalogue_document,
    create_document,
    extract_entities,
    generate_procedure,
    query_graph,
    search_documents,
    transform_document,
    update_graph,
)


def print_section(title: str):
    """Print a section header."""
    logger.info("\n" + "=" * 70)
    logger.info(f"  {title}")
    logger.info("=" * 70 + "\n")


def print_result(result: dict):
    """Print a result dict nicely."""
    if result.get("success"):
        logger.success(f"✓ Success")
        # Print key fields
        for key in ["num_steps", "num_results", "document_id", "title", "format"]:
            if key in result:
                logger.info(f"  {key}: {result[key]}")
    else:
        logger.error(f"✗ Failed: {result.get('error', 'Unknown error')}")


async def test_all_graphs():
    """Test generate_procedure with all example graphs."""
    print_section("TEST 1: Generate Procedures from All Graphs")

    test_cases = [
        {
            "name": "Mortgage Underwriting (NM Rural)",
            "graph_file": "mortgage_underwriting.json",
            "start_node": "Loan Application",
            "filters": {"location": "New Mexico", "property_type": "rural"},
        },
        {
            "name": "IT Onboarding (Remote Developer)",
            "graph_file": "it_onboarding_graph.json",
            "start_node": "Employee Onboarding",
            "filters": {"role": "Developer", "location": "Remote"},
        },
        {
            "name": "Software Development (Backend + Production)",
            "graph_file": "software_dev_graph.json",
            "start_node": "Sprint Planning",
            "filters": {"feature_type": "Backend", "environment": "Production"},
        },
        {
            "name": "Compliance (GDPR Healthcare)",
            "graph_file": "compliance_graph.json",
            "start_node": "Risk Assessment",
            "filters": {"regulation": "GDPR", "industry": "Healthcare"},
        },
    ]

    for test in test_cases:
        logger.info(f"\n📋 {test['name']}")
        result = await generate_procedure(
            graph_file=test["graph_file"],
            start_node=test["start_node"],
            filters=test["filters"],
            output_format="markdown",
        )
        print_result(result)

        if result.get("success") and result.get("steps"):
            logger.info(f"\n  Generated Steps:")
            for step in result["steps"][:5]:  # Show first 5
                logger.info(f"    - {step['label']}")
            if len(result["steps"]) > 5:
                logger.info(f"    ... and {len(result['steps']) - 5} more")


async def test_document_search():
    """Test search_documents with various queries."""
    print_section("TEST 2: Search Catalogued Documents")

    queries = [
        ("security policy password requirements", {"tags": ["security"]}),
        ("API authentication endpoints", {"tags": ["api"]}),
        ("GDPR data subject rights", {"tags": ["gdpr"]}),
        ("incident response procedures", None),
        ("developer onboarding git workflow", None),
    ]

    for query, filters in queries:
        logger.info(f"\n🔍 Searching: '{query}'")
        if filters:
            logger.info(f"   Filters: {filters}")

        result = await search_documents(
            query=query, filters=filters, limit=3, min_score=0.2
        )
        print_result(result)

        if result.get("success") and result.get("results"):
            for idx, doc in enumerate(result["results"][:2], 1):
                logger.info(f"\n  Result {idx}:")
                logger.info(f"    Title: {doc['title']}")
                logger.info(f"    Score: {doc['score']}")
                logger.info(f"    Snippet: {doc['snippet'][:100]}...")


async def test_document_transforms():
    """Test transform_document with various conversions."""
    print_section("TEST 3: Document Format Transformations")

    markdown_sample = """# Sample Document

This is a **test document** with:

- Bullet point 1
- Bullet point 2

## Code Example

```python
def hello():
    print("Hello, world!")
```

[Link to docs](https://example.com)
"""

    transforms = [
        ("Markdown → HTML", "markdown", "html", {}),
        ("Markdown → JSON", "markdown", "json", {}),
        ("Markdown → Text", "markdown", "text", {}),
        (
            "Markdown → HTML (Full Doc)",
            "markdown",
            "html",
            {"full_document": True, "title": "Test Document"},
        ),
    ]

    for name, source, target, options in transforms:
        logger.info(f"\n🔄 {name}")
        result = await transform_document(
            content=markdown_sample,
            source_format=source,
            target_format=target,
            options=options,
        )
        print_result(result)

        if result.get("success"):
            preview = result["content"][:150]
            logger.info(f"  Preview: {preview}...")


async def test_create_documents():
    """Test create_document with various templates."""
    print_section("TEST 4: Create Documents from Templates")

    templates = [
        {
            "name": "Simple Document",
            "template": "simple_doc.md.j2",
            "context": {
                "title": "Test Report",
                "author": "Test User",
                "date": "2025-01-15",
                "content": "This is test content with **markdown**.",
                "tags": ["test", "demo"],
            },
        },
        {
            "name": "Procedure Document",
            "template": "procedure.md.j2",
            "context": {
                "title": "Deployment Procedure",
                "description": "Steps to deploy application",
                "context": {"environment": "production", "region": "us-east-1"},
                "steps": [
                    {
                        "name": "Build Application",
                        "description": "Compile and build the application",
                        "role": "DevOps Engineer",
                        "system": "CI/CD Pipeline",
                        "inputs": ["Source code", "Configuration"],
                        "outputs": ["Build artifacts"],
                    },
                    {
                        "name": "Run Tests",
                        "description": "Execute test suite",
                        "role": "QA Engineer",
                        "inputs": ["Build artifacts"],
                        "outputs": ["Test results"],
                    },
                ],
            },
        },
    ]

    for test in templates:
        logger.info(f"\n📝 {test['name']}")
        result = await create_document(
            template_name=test["template"],
            context=test["context"],
            output_format="markdown",
        )
        print_result(result)

        if result.get("success"):
            preview = result["content"][:200]
            logger.info(f"  Preview: {preview}...")


async def test_graph_queries():
    """Test query_graph with various operations."""
    print_section("TEST 5: Query Knowledge Graphs")

    queries = [
        {
            "name": "Get Statistics",
            "graph": "mortgage_underwriting.json",
            "operation": "get_statistics",
        },
        {
            "name": "Get Process Nodes",
            "graph": "it_onboarding_graph.json",
            "operation": "get_nodes_by_type",
            "node_type": "process",
        },
        {
            "name": "Find Path",
            "graph": "software_dev_graph.json",
            "operation": "find_path",
            "start_node": "Sprint Planning",
            "end_node": "Deploy to Production",
        },
        {
            "name": "Get Neighbors",
            "graph": "compliance_graph.json",
            "operation": "get_neighbors",
            "node_id": "Risk Assessment",
        },
    ]

    for test in queries:
        logger.info(f"\n🔍 {test['name']}")
        result = await query_graph(**{k: v for k, v in test.items() if k != "name"})
        print_result(result)

        if result.get("success"):
            # Show relevant info based on operation
            if "statistics" in result:
                stats = result["statistics"]
                logger.info(f"  Nodes: {stats['num_nodes']}, Edges: {stats['num_edges']}")
            elif "nodes" in result:
                logger.info(f"  Found {result['num_nodes']} nodes")
            elif "path" in result:
                path = [n["label"] for n in result["path"]]
                logger.info(f"  Path ({result['path_length']} steps): {' → '.join(path[:3])}...")
            elif "neighbors" in result:
                neighbors = [n["label"] for n in result["neighbors"][:3]]
                logger.info(f"  Neighbors: {', '.join(neighbors)}")


async def test_entity_extraction():
    """Test extract_entities on sample documents."""
    print_section("TEST 6: Extract Entities from Text")

    samples = [
        {
            "name": "Policy Document",
            "text": """
            The Chief Information Security Officer (CISO) reports to the Board of Directors.
            All employees must complete training by January 31, 2025.
            Contact the Security Operations Center (SOC) for incidents.
            This policy complies with ISO 27001 and SOC 2 Type II requirements.
            """,
        },
        {
            "name": "Project Description",
            "text": """
            John Smith from Acme Corporation is leading the API migration project.
            The team includes Mary Johnson (senior developer) and Bob Wilson (DevOps engineer).
            The project kicks off on February 1, 2025 in San Francisco.
            We'll be using AWS us-east-1 region for deployment.
            """,
        },
    ]

    for sample in samples:
        logger.info(f"\n🏷️  {sample['name']}")
        result = await extract_entities(
            content=sample["text"], entity_types=["PERSON", "ORG", "LOCATION", "DATE"]
        )
        print_result(result)

        if result.get("success") and result.get("entities"):
            logger.info(f"  Entities found:")
            for entity in result["entities"][:5]:
                logger.info(f"    - {entity['text']} ({entity['type']})")


async def main():
    """Run all tests."""
    logger.info("\n" + "=" * 70)
    logger.info("  DocAsCode MCP Service - Comprehensive Tool Testing")
    logger.info("=" * 70)

    # Ensure data is loaded
    settings.ensure_directories()

    # Run all tests
    await test_all_graphs()
    await test_document_search()
    await test_document_transforms()
    await test_create_documents()
    await test_graph_queries()
    await test_entity_extraction()

    logger.info("\n" + "=" * 70)
    logger.success("  All Tests Completed!")
    logger.info("=" * 70)

    logger.info(
        "\n💡 Next: Start the MCP server with 'python -m mcp_server.server' to use with Claude Desktop"
    )


if __name__ == "__main__":
    asyncio.run(main())
