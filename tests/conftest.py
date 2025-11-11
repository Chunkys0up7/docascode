"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest

from mcp_server.config import Settings
from mcp_server.core.graph_engine import GraphEngine
from mcp_server.models.schemas import EdgeRelation, GraphEdge, GraphNode, NodeType


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def test_settings(temp_dir):
    """Create test settings with temporary directories."""
    settings = Settings(
        data_dir=temp_dir / "data",
        documents_dir=temp_dir / "data/documents",
        graphs_dir=temp_dir / "data/graphs",
        indices_dir=temp_dir / "data/indices",
        templates_dir=temp_dir / "templates",
        chromadb_path=temp_dir / "data/indices/chroma",
        log_level="DEBUG",
    )
    settings.ensure_directories()
    return settings


@pytest.fixture
def sample_graph():
    """Create a sample knowledge graph for testing."""
    graph = GraphEngine()

    # Add nodes
    nodes = [
        GraphNode(id="Start", label="Start Process", type=NodeType.PROCESS),
        GraphNode(id="Step1", label="Step 1", type=NodeType.PROCESS),
        GraphNode(id="Step2", label="Step 2", type=NodeType.PROCESS),
        GraphNode(id="System1", label="System 1", type=NodeType.SYSTEM),
        GraphNode(id="Role1", label="Role 1", type=NodeType.ROLE),
        GraphNode(id="Context1", label="Context 1", type=NodeType.CONTEXT),
    ]

    for node in nodes:
        graph.add_node(node)

    # Add edges
    edges = [
        GraphEdge(source="Start", target="Step1", relation=EdgeRelation.REQUIRES),
        GraphEdge(source="Step1", target="Step2", relation=EdgeRelation.PRECEDES),
        GraphEdge(source="Step1", target="System1", relation=EdgeRelation.REQUIRES),
        GraphEdge(source="Step1", target="Role1", relation=EdgeRelation.PERFORMED_BY),
        GraphEdge(source="Step2", target="Context1", relation=EdgeRelation.APPLIES_TO),
    ]

    for edge in edges:
        graph.add_edge(edge)

    return graph
