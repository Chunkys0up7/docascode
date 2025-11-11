"""Query graph tool - explore knowledge graph relationships."""

from typing import Any, Dict, List, Optional

from loguru import logger

from mcp_server.config import settings
from mcp_server.core.graph_engine import GraphEngine
from mcp_server.models.schemas import EdgeRelation, NodeType


async def query_graph(
    graph_file: str,
    operation: str,
    node_id: Optional[str] = None,
    node_type: Optional[str] = None,
    relation: Optional[str] = None,
    start_node: Optional[str] = None,
    end_node: Optional[str] = None,
) -> Dict[str, Any]:
    """Query a knowledge graph for nodes, relationships, and paths.

    Operations:
    - get_node: Get node by ID
    - get_neighbors: Get neighboring nodes (requires node_id, optional relation)
    - get_nodes_by_type: Get all nodes of type (requires node_type)
    - find_path: Find path between nodes (requires start_node, end_node)
    - get_statistics: Get graph statistics

    Args:
        graph_file: Path to graph JSON file
        operation: Operation to perform
        node_id: Node ID for node operations
        node_type: Node type filter (process, system, role, regulation, context, etc.)
        relation: Edge relation filter (requires, performed_by, applies_to, etc.)
        start_node: Start node for path finding
        end_node: End node for path finding

    Returns:
        Dict with query results

    Example:
        ```python
        # Get neighbors
        result = await query_graph(
            graph_file="mortgage.json",
            operation="get_neighbors",
            node_id="Verify Credit Score",
            relation="requires"
        )

        # Find path
        result = await query_graph(
            graph_file="mortgage.json",
            operation="find_path",
            start_node="Loan Application",
            end_node="Generate Approval Document"
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
        if operation == "get_node":
            if not node_id:
                return {"success": False, "error": "node_id required for get_node"}

            node = graph.get_node(node_id)
            if not node:
                return {"success": False, "error": f"Node not found: {node_id}"}

            return {
                "success": True,
                "operation": operation,
                "node": {
                    "id": node.id,
                    "label": node.label,
                    "type": node.type.value,
                    "properties": node.properties,
                },
            }

        elif operation == "get_neighbors":
            if not node_id:
                return {"success": False, "error": "node_id required for get_neighbors"}

            rel = EdgeRelation(relation) if relation else None
            neighbors = graph.get_neighbors(node_id, relation=rel, direction="out")

            neighbor_data = []
            for nid in neighbors:
                node = graph.get_node(nid)
                if node:
                    neighbor_data.append({
                        "id": node.id,
                        "label": node.label,
                        "type": node.type.value,
                    })

            return {
                "success": True,
                "operation": operation,
                "node_id": node_id,
                "relation_filter": relation,
                "num_neighbors": len(neighbors),
                "neighbors": neighbor_data,
            }

        elif operation == "get_nodes_by_type":
            if not node_type:
                return {"success": False, "error": "node_type required for get_nodes_by_type"}

            ntype = NodeType(node_type)
            nodes = graph.get_nodes_by_type(ntype)

            nodes_data = [
                {"id": n.id, "label": n.label, "type": n.type.value, "properties": n.properties}
                for n in nodes
            ]

            return {
                "success": True,
                "operation": operation,
                "node_type": node_type,
                "num_nodes": len(nodes),
                "nodes": nodes_data,
            }

        elif operation == "find_path":
            if not start_node or not end_node:
                return {"success": False, "error": "start_node and end_node required for find_path"}

            path = graph.find_path(start_node, end_node)
            if not path:
                return {
                    "success": False,
                    "error": f"No path found between {start_node} and {end_node}",
                }

            path_data = []
            for nid in path:
                node = graph.get_node(nid)
                if node:
                    path_data.append({
                        "id": node.id,
                        "label": node.label,
                        "type": node.type.value,
                    })

            return {
                "success": True,
                "operation": operation,
                "start_node": start_node,
                "end_node": end_node,
                "path_length": len(path),
                "path": path_data,
            }

        elif operation == "get_statistics":
            stats = graph.get_statistics()
            return {
                "success": True,
                "operation": operation,
                "statistics": stats,
            }

        else:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}",
                "valid_operations": [
                    "get_node",
                    "get_neighbors",
                    "get_nodes_by_type",
                    "find_path",
                    "get_statistics",
                ],
            }

    except Exception as e:
        logger.error(f"Failed to query graph: {e}")
        return {
            "success": False,
            "error": str(e),
            "graph_file": graph_file,
            "operation": operation,
        }
