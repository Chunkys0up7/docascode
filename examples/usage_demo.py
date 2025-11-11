"""
Usage examples for DocAsCode MCP Service

This demonstrates how to use all 8 MCP tools programmatically.
Note: The MCP server typically runs as a service and is called by MCP clients.
"""

import asyncio
import json
from pathlib import Path

# Import all tools
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


async def demo_create_document():
    """Demo: Create a document from a template."""
    print("\n=== CREATE DOCUMENT ===")

    result = await create_document(
        template_name="simple_doc.md.j2",
        context={
            "title": "My First Document",
            "author": "John Doe",
            "date": "2025-01-15",
            "content": "This is the **main content** of my document.",
            "tags": ["demo", "example", "markdown"],
        },
        output_format="markdown",
    )

    print(json.dumps(result, indent=2))
    if result["success"]:
        print("\nGenerated content:")
        print(result["content"])


async def demo_transform_document():
    """Demo: Transform document between formats."""
    print("\n=== TRANSFORM DOCUMENT ===")

    markdown_content = """# Hello World

This is a **markdown** document with:

- Bullet points
- Multiple items
- Formatted text

## Code Example

```python
def hello():
    print("Hello, world!")
```
"""

    # Markdown to HTML
    result = await transform_document(
        content=markdown_content,
        source_format="markdown",
        target_format="html",
        options={"full_document": True, "title": "Hello World"},
    )

    print(json.dumps({k: v for k, v in result.items() if k != "content"}, indent=2))
    if result["success"]:
        print("\nFirst 500 chars of HTML:")
        print(result["content"][:500] + "...")


async def demo_catalogue_and_search():
    """Demo: Catalogue documents and search them."""
    print("\n=== CATALOGUE & SEARCH ===")

    # Catalogue a few documents
    documents = [
        {
            "title": "Mortgage Underwriting Guide",
            "content": "This guide covers the complete process of mortgage underwriting including credit verification, property appraisal, and regulatory compliance.",
            "metadata": {
                "author": "Jane Smith",
                "tags": ["mortgage", "underwriting", "compliance"],
                "description": "Comprehensive guide to mortgage underwriting procedures",
            },
        },
        {
            "title": "Rural Property Appraisal",
            "content": "Special considerations for appraising rural properties including unique comparables, zoning restrictions, and agricultural use.",
            "metadata": {
                "author": "Bob Jones",
                "tags": ["appraisal", "rural", "property"],
                "description": "Guide for rural property appraisals",
            },
        },
        {
            "title": "Credit Score Verification",
            "content": "Standard operating procedure for verifying applicant credit scores through bureau APIs and validating reports.",
            "metadata": {
                "author": "Jane Smith",
                "tags": ["credit", "verification", "underwriting"],
                "description": "Credit score verification procedures",
            },
        },
    ]

    print("Cataloguing documents...")
    for doc in documents:
        result = await catalogue_document(
            content=doc["content"],
            title=doc["title"],
            metadata=doc["metadata"],
        )
        if result["success"]:
            print(f"  ✓ Catalogued: {doc['title']} (ID: {result['document_id']})")

    # Search documents
    print("\nSearching for 'mortgage underwriting procedures'...")
    search_result = await search_documents(
        query="mortgage underwriting procedures", limit=5, min_score=0.3
    )

    if search_result["success"]:
        print(f"Found {search_result['num_results']} results:")
        for result in search_result["results"]:
            print(f"\n  {result['title']} (score: {result['score']})")
            print(f"  {result['snippet'][:100]}...")


async def demo_generate_procedure():
    """Demo: Generate context-aware procedure from knowledge graph."""
    print("\n=== GENERATE PROCEDURE ===")

    # Ensure graph file exists in data/graphs
    graph_file = "mortgage_underwriting.json"

    # Generate procedure for New Mexico rural property
    print(f"Generating procedure for NM rural property...")
    result = await generate_procedure(
        graph_file=graph_file,
        start_node="Loan Application",
        filters={"location": "New Mexico", "property_type": "rural"},
        output_format="markdown",
    )

    if result["success"]:
        print(f"\nGenerated {result['num_steps']} steps")
        print("\nProcedure content:")
        print(result["content"])
    else:
        print(f"Error: {result.get('error')}")


async def demo_query_graph():
    """Demo: Query knowledge graph."""
    print("\n=== QUERY GRAPH ===")

    graph_file = "mortgage_underwriting.json"

    # Get graph statistics
    print("Getting graph statistics...")
    result = await query_graph(graph_file=graph_file, operation="get_statistics")

    if result["success"]:
        print(json.dumps(result["statistics"], indent=2))

    # Get neighbors of a node
    print("\nGetting neighbors of 'Verify Credit Score'...")
    result = await query_graph(
        graph_file=graph_file,
        operation="get_neighbors",
        node_id="Verify Credit Score",
    )

    if result["success"]:
        print(f"Found {result['num_neighbors']} neighbors:")
        for neighbor in result["neighbors"]:
            print(f"  - {neighbor['label']} ({neighbor['type']})")

    # Find path between nodes
    print("\nFinding path from 'Loan Application' to 'Generate Approval Document'...")
    result = await query_graph(
        graph_file=graph_file,
        operation="find_path",
        start_node="Loan Application",
        end_node="Generate Approval Document",
    )

    if result["success"]:
        print(f"Path length: {result['path_length']}")
        print("Path:", " -> ".join(n["label"] for n in result["path"]))


async def demo_update_graph():
    """Demo: Update knowledge graph (add/remove nodes and edges)."""
    print("\n=== UPDATE GRAPH ===")

    graph_file = "mortgage_underwriting.json"

    # Add a new node
    print("Adding new process node 'Verify Income'...")
    result = await update_graph(
        graph_file=graph_file,
        operation="add_node",
        node={
            "id": "Verify Income",
            "label": "Verify Income",
            "type": "process",
            "properties": {"description": "Verify applicant income documentation"},
        },
    )

    if result["success"]:
        print(f"  ✓ {result['message']}")

    # Add edge connecting it
    print("Connecting 'Loan Application' -> 'Verify Income'...")
    result = await update_graph(
        graph_file=graph_file,
        operation="add_edge",
        edge={
            "source": "Loan Application",
            "target": "Verify Income",
            "relation": "requires",
        },
    )

    if result["success"]:
        print(f"  ✓ {result['message']}")


async def demo_extract_entities():
    """Demo: Extract named entities from text."""
    print("\n=== EXTRACT ENTITIES ===")

    text = """
    John Smith from Acme Corporation signed the contract with Wells Fargo Bank
    on January 15, 2024, for the property located in Santa Fe, New Mexico.
    The underwriter, Mary Johnson, approved the loan after reviewing the credit report.
    """

    result = await extract_entities(
        content=text, entity_types=["PERSON", "ORG", "LOCATION", "DATE"]
    )

    if result["success"]:
        print(f"Found {result['num_entities']} potential entities:")
        for entity in result["entities"]:
            print(f"  - {entity['text']} (type: {entity['type']})")
        print(f"\n{result.get('note', '')}")


async def main():
    """Run all demos."""
    print("=" * 60)
    print("DocAsCode MCP Service - Usage Demonstration")
    print("=" * 60)

    # Copy mortgage graph to data/graphs directory
    import shutil
    from mcp_server.config import settings

    settings.ensure_directories()

    source_graph = Path("examples/mortgage_graph.json")
    if source_graph.exists():
        target_graph = settings.graphs_dir / "mortgage_underwriting.json"
        shutil.copy(source_graph, target_graph)
        print(f"\n✓ Copied graph to {target_graph}")

    # Run demos
    await demo_create_document()
    await demo_transform_document()
    await demo_catalogue_and_search()
    await demo_generate_procedure()
    await demo_query_graph()
    await demo_update_graph()
    await demo_extract_entities()

    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
