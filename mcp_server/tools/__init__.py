"""MCP tools for document operations."""

from mcp_server.tools.catalogue import catalogue_document
from mcp_server.tools.create import create_document
from mcp_server.tools.extract import extract_entities
from mcp_server.tools.graph_query import query_graph
from mcp_server.tools.graph_update import update_graph
from mcp_server.tools.procedure import generate_procedure
from mcp_server.tools.search import search_documents
from mcp_server.tools.transform import transform_document

__all__ = [
    "create_document",
    "transform_document",
    "catalogue_document",
    "search_documents",
    "generate_procedure",
    "query_graph",
    "update_graph",
    "extract_entities",
]
