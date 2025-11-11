"""MCP server implementation for DocAsCode service."""

import asyncio
from typing import Any

from loguru import logger
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

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

# Initialize server
app = Server(settings.server_name)


# Tool definitions
TOOLS = [
    Tool(
        name="create_document",
        description="Create a document from a template with context and optional graph data",
        inputSchema={
            "type": "object",
            "properties": {
                "template_name": {
                    "type": "string",
                    "description": "Name of the template file (e.g., 'procedure.md.j2')",
                },
                "context": {
                    "type": "object",
                    "description": "Template context variables",
                    "additionalProperties": True,
                },
                "output_format": {
                    "type": "string",
                    "enum": ["markdown", "html", "json", "text"],
                    "default": "markdown",
                    "description": "Output document format",
                },
                "graph_data": {
                    "type": "object",
                    "description": "Optional knowledge graph data (nodes and edges)",
                },
            },
            "required": ["template_name", "context"],
        },
    ),
    Tool(
        name="transform_document",
        description="Transform a document from one format to another (markdown, html, json, text, pdf, docx)",
        inputSchema={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Document content to transform",
                },
                "source_format": {
                    "type": "string",
                    "enum": ["markdown", "html", "json", "text", "pdf", "docx"],
                    "description": "Source format",
                },
                "target_format": {
                    "type": "string",
                    "enum": ["markdown", "html", "json", "text", "pdf", "docx"],
                    "description": "Target format",
                },
                "options": {
                    "type": "object",
                    "description": "Transformation options (e.g., {'full_document': true, 'title': 'My Doc'})",
                    "additionalProperties": True,
                },
            },
            "required": ["content", "source_format", "target_format"],
        },
    ),
    Tool(
        name="catalogue_document",
        description="Catalogue a document by indexing it with metadata and embeddings for search",
        inputSchema={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Document content to catalogue",
                },
                "title": {
                    "type": "string",
                    "description": "Document title",
                },
                "format": {
                    "type": "string",
                    "enum": ["markdown", "html", "json", "text"],
                    "default": "markdown",
                    "description": "Document format",
                },
                "metadata": {
                    "type": "object",
                    "description": "Optional metadata (author, tags, description, etc.)",
                    "additionalProperties": True,
                },
                "collection": {
                    "type": "string",
                    "default": "documents",
                    "description": "Collection name",
                },
            },
            "required": ["content", "title"],
        },
    ),
    Tool(
        name="search_documents",
        description="Search documents using semantic similarity and metadata filters",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string",
                },
                "collection": {
                    "type": "string",
                    "default": "documents",
                    "description": "Collection name to search in",
                },
                "filters": {
                    "type": "object",
                    "description": "Optional metadata filters (e.g., {'author': 'John', 'format': 'markdown'})",
                    "additionalProperties": True,
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum number of results",
                },
                "min_score": {
                    "type": "number",
                    "default": 0.0,
                    "description": "Minimum similarity score (0.0-1.0)",
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="generate_procedure",
        description="Generate a context-aware procedure from a knowledge graph using BFS traversal",
        inputSchema={
            "type": "object",
            "properties": {
                "graph_file": {
                    "type": "string",
                    "description": "Path to graph JSON file (e.g., 'mortgage_underwriting.json')",
                },
                "start_node": {
                    "type": "string",
                    "description": "Starting node ID for traversal",
                },
                "filters": {
                    "type": "object",
                    "description": "Context filters (e.g., {'location': 'Texas', 'property_type': 'rural'})",
                    "additionalProperties": True,
                },
                "max_depth": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum traversal depth",
                },
                "output_format": {
                    "type": "string",
                    "enum": ["list", "markdown", "json"],
                    "default": "list",
                    "description": "Output format",
                },
            },
            "required": ["graph_file", "start_node"],
        },
    ),
    Tool(
        name="query_graph",
        description="Query a knowledge graph for nodes, relationships, and paths",
        inputSchema={
            "type": "object",
            "properties": {
                "graph_file": {
                    "type": "string",
                    "description": "Path to graph JSON file",
                },
                "operation": {
                    "type": "string",
                    "enum": [
                        "get_node",
                        "get_neighbors",
                        "get_nodes_by_type",
                        "find_path",
                        "get_statistics",
                    ],
                    "description": "Query operation to perform",
                },
                "node_id": {
                    "type": "string",
                    "description": "Node ID (for get_node, get_neighbors)",
                },
                "node_type": {
                    "type": "string",
                    "enum": ["process", "system", "role", "regulation", "context", "document", "entity", "concept"],
                    "description": "Node type (for get_nodes_by_type)",
                },
                "relation": {
                    "type": "string",
                    "enum": ["requires", "performed_by", "applies_to", "conditional_on", "precedes", "references", "related_to", "contains"],
                    "description": "Edge relation filter (for get_neighbors)",
                },
                "start_node": {
                    "type": "string",
                    "description": "Start node (for find_path)",
                },
                "end_node": {
                    "type": "string",
                    "description": "End node (for find_path)",
                },
            },
            "required": ["graph_file", "operation"],
        },
    ),
    Tool(
        name="update_graph",
        description="Update a knowledge graph by adding or removing nodes and edges",
        inputSchema={
            "type": "object",
            "properties": {
                "graph_file": {
                    "type": "string",
                    "description": "Path to graph JSON file",
                },
                "operation": {
                    "type": "string",
                    "enum": ["add_node", "remove_node", "add_edge", "remove_edge"],
                    "description": "Update operation to perform",
                },
                "node": {
                    "type": "object",
                    "description": "Node data (id, label, type, properties) for add_node",
                    "properties": {
                        "id": {"type": "string"},
                        "label": {"type": "string"},
                        "type": {"type": "string"},
                        "properties": {"type": "object"},
                    },
                },
                "edge": {
                    "type": "object",
                    "description": "Edge data (source, target, relation, properties) for add_edge",
                    "properties": {
                        "source": {"type": "string"},
                        "target": {"type": "string"},
                        "relation": {"type": "string"},
                        "properties": {"type": "object"},
                    },
                },
                "node_id": {
                    "type": "string",
                    "description": "Node ID for remove_node",
                },
                "source": {
                    "type": "string",
                    "description": "Source node for remove_edge",
                },
                "target": {
                    "type": "string",
                    "description": "Target node for remove_edge",
                },
            },
            "required": ["graph_file", "operation"],
        },
    ),
    Tool(
        name="extract_entities",
        description="Extract named entities from text content (requires optional 'nlp' dependencies for full features)",
        inputSchema={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Text content to analyze",
                },
                "entity_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Entity types to extract (PERSON, ORG, LOCATION, DATE, etc.)",
                },
                "language": {
                    "type": "string",
                    "default": "en",
                    "description": "Language code",
                },
            },
            "required": ["content"],
        },
    ),
]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    logger.info("Listing tools")
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool execution."""
    logger.info(f"Tool called: {name}")

    try:
        # Route to appropriate tool function
        if name == "create_document":
            result = await create_document(**arguments)
        elif name == "transform_document":
            result = await transform_document(**arguments)
        elif name == "catalogue_document":
            result = await catalogue_document(**arguments)
        elif name == "search_documents":
            result = await search_documents(**arguments)
        elif name == "generate_procedure":
            result = await generate_procedure(**arguments)
        elif name == "query_graph":
            result = await query_graph(**arguments)
        elif name == "update_graph":
            result = await update_graph(**arguments)
        elif name == "extract_entities":
            result = await extract_entities(**arguments)
        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}

        # Format result as JSON string
        import json
        result_text = json.dumps(result, indent=2)

        return [TextContent(type="text", text=result_text)]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}", exc_info=True)
        import json
        error_result = {"success": False, "error": str(e), "tool": name}
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]


async def main() -> None:
    """Run the MCP server."""
    # Ensure directories exist
    settings.ensure_directories()

    logger.info(f"Starting {settings.server_name} v{settings.server_version}")
    logger.info(f"Data directory: {settings.data_dir}")
    logger.info(f"Templates directory: {settings.templates_dir}")

    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
