"""Tests for graph engine."""

import pytest

from mcp_server.core.graph_engine import GraphEngine
from mcp_server.models.schemas import EdgeRelation, GraphEdge, GraphNode, NodeType


def test_add_node(sample_graph):
    """Test adding nodes to graph."""
    assert "Start" in sample_graph.graph.nodes
    assert sample_graph.graph.nodes["Start"]["type"] == NodeType.PROCESS.value


def test_add_edge(sample_graph):
    """Test adding edges to graph."""
    assert sample_graph.graph.has_edge("Start", "Step1")
    assert sample_graph.graph["Start"]["Step1"]["relation"] == EdgeRelation.REQUIRES.value


def test_get_node(sample_graph):
    """Test getting node by ID."""
    node = sample_graph.get_node("Start")
    assert node is not None
    assert node.id == "Start"
    assert node.type == NodeType.PROCESS


def test_get_neighbors(sample_graph):
    """Test getting neighbors."""
    neighbors = sample_graph.get_neighbors("Step1")
    assert "Step2" in neighbors
    assert "System1" in neighbors


def test_get_neighbors_filtered(sample_graph):
    """Test getting neighbors with relation filter."""
    neighbors = sample_graph.get_neighbors("Step1", relation=EdgeRelation.REQUIRES)
    assert "System1" in neighbors
    assert "Step2" not in neighbors  # precedes, not requires


def test_find_path(sample_graph):
    """Test finding path between nodes."""
    path = sample_graph.find_path("Start", "Step2")
    assert path is not None
    assert path == ["Start", "Step1", "Step2"]


def test_traverse_bfs(sample_graph):
    """Test BFS traversal."""
    visited = sample_graph.traverse_bfs("Start")
    assert "Start" in visited
    assert "Step1" in visited
    assert "Step2" in visited


def test_get_nodes_by_type(sample_graph):
    """Test getting nodes by type."""
    processes = sample_graph.get_nodes_by_type(NodeType.PROCESS)
    assert len(processes) == 3
    assert all(n.type == NodeType.PROCESS for n in processes)


def test_remove_node(sample_graph):
    """Test removing nodes."""
    sample_graph.remove_node("Step2")
    assert "Step2" not in sample_graph.graph.nodes


def test_remove_edge(sample_graph):
    """Test removing edges."""
    sample_graph.remove_edge("Start", "Step1")
    assert not sample_graph.graph.has_edge("Start", "Step1")


def test_export_import(sample_graph, temp_dir):
    """Test exporting and importing graph."""
    # Export
    file_path = temp_dir / "test_graph.json"
    sample_graph.save_to_file(file_path)
    assert file_path.exists()

    # Import
    new_graph = GraphEngine()
    new_graph.load_from_file(file_path)

    assert new_graph.graph.number_of_nodes() == sample_graph.graph.number_of_nodes()
    assert new_graph.graph.number_of_edges() == sample_graph.graph.number_of_edges()


def test_statistics(sample_graph):
    """Test graph statistics."""
    stats = sample_graph.get_statistics()
    assert stats["num_nodes"] == 6
    assert stats["num_edges"] == 5
    assert stats["is_directed"] is True
