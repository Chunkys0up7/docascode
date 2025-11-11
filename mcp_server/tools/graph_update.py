"""Update graph tool - modify knowledge graph structure."""

from typing import Any, Dict, List, Optional

from loguru import logger

from mcp_server.config import settings
from mcp_server.core.graph_engine import GraphEngine
from mcp_server.models.schemas import EdgeRelation, GraphEdge, GraphNode, NodeType


async def update_graph(
    graph_file: str,
    operation: str,
    node: Optional[Dict[str, Any]] = None,
    edge: Optional[Dict[str, Any]] = None,
    node_id: Optional[str] = None,
    source: Optional[str] = None,
    target: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a knowledge graph by adding, removing, or modifying nodes and edges.

    Operations:
    - add_node: Add a new node (requires node dict with id, label, type)
    - remove_node: Remove a node (requires node_id)
    - add_edge: Add a new edge (requires edge dict with source, target, relation)
    - remove_edge: Remove an edge (requires source, target)

    Args:
        graph_file: Path to graph JSON file
        operation: Operation to perform
        node: Node data dict (id, label, type, properties)
        edge: Edge data dict (source, target, relation, properties)
        node_id: Node ID for removal
        source: Source node ID for edge removal
        target: Target node ID for edge removal

    Returns:
        Dict with operation result

    Example:
        ```python
        # Add node
        result = await update_graph(
            graph_file="mortgage.json",
            operation="add_node",
            node={
                "id": "New Process",
                "label": "New Process Step",
                "type": "process",
                "properties": {"priority": "high"}
            }
        )

        # Add edge
        result = await update_graph(
            graph_file="mortgage.json",
            operation="add_edge",
            edge={
                "source": "Loan Application",
                "target": "New Process",
                "relation": "requires"
            }
        )
        ```
    """
    try:
        # Load graph
        graph_path = settings.graphs_dir / graph_file
        if not graph_path.exists():
            return {
                "success": False,
                "error": f"Graph file not found: {graph_file}",
            }

        graph = GraphEngine()
        graph.load_from_file(graph_path)

        # Execute operation
        if operation == "add_node":
            if not node:
                return {"success": False, "error": "node required for add_node"}

            # Validate node data
            if "id" not in node or "label" not in node or "type" not in node:
                return {
                    "success": False,
                    "error": "node must have id, label, and type fields",
                }

            graph_node = GraphNode(
                id=node["id"],
                label=node["label"],
                type=NodeType(node["type"]),
                properties=node.get("properties", {}),
            )

            graph.add_node(graph_node)
            graph.save_to_file(graph_path)

            return {
                "success": True,
                "operation": operation,
                "node_id": node["id"],
                "message": f"Added node: {node['id']}",
            }

        elif operation == "remove_node":
            if not node_id:
                return {"success": False, "error": "node_id required for remove_node"}

            if node_id not in graph.graph.nodes:
                return {"success": False, "error": f"Node not found: {node_id}"}

            graph.remove_node(node_id)
            graph.save_to_file(graph_path)

            return {
                "success": True,
                "operation": operation,
                "node_id": node_id,
                "message": f"Removed node: {node_id}",
            }

        elif operation == "add_edge":
            if not edge:
                return {"success": False, "error": "edge required for add_edge"}

            # Validate edge data
            if "source" not in edge or "target" not in edge or "relation" not in edge:
                return {
                    "success": False,
                    "error": "edge must have source, target, and relation fields",
                }

            # Validate nodes exist
            if edge["source"] not in graph.graph.nodes:
                return {"success": False, "error": f"Source node not found: {edge['source']}"}
            if edge["target"] not in graph.graph.nodes:
                return {"success": False, "error": f"Target node not found: {edge['target']}"}

            graph_edge = GraphEdge(
                source=edge["source"],
                target=edge["target"],
                relation=EdgeRelation(edge["relation"]),
                properties=edge.get("properties", {}),
            )

            graph.add_edge(graph_edge)
            graph.save_to_file(graph_path)

            return {
                "success": True,
                "operation": operation,
                "edge": f"{edge['source']} --[{edge['relation']}]--> {edge['target']}",
                "message": "Added edge",
            }

        elif operation == "remove_edge":
            if not source or not target:
                return {"success": False, "error": "source and target required for remove_edge"}

            if not graph.graph.has_edge(source, target):
                return {
                    "success": False,
                    "error": f"Edge not found: {source} --> {target}",
                }

            graph.remove_edge(source, target)
            graph.save_to_file(graph_path)

            return {
                "success": True,
                "operation": operation,
                "edge": f"{source} --> {target}",
                "message": "Removed edge",
            }

        else:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}",
                "valid_operations": ["add_node", "remove_node", "add_edge", "remove_edge"],
            }

    except Exception as e:
        logger.error(f"Failed to update graph: {e}")
        return {
            "success": False,
            "error": str(e),
            "graph_file": graph_file,
            "operation": operation,
        }
