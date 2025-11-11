"""Generate procedure tool - context-aware procedure generation from graphs."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

from mcp_server.config import settings
from mcp_server.core.graph_engine import GraphEngine
from mcp_server.models.schemas import KnowledgeGraph, NodeType


async def generate_procedure(
    graph_file: str,
    start_node: str,
    filters: Optional[Dict[str, Any]] = None,
    max_depth: int = 10,
    output_format: str = "list",
) -> Dict[str, Any]:
    """Generate a context-aware procedure from a knowledge graph.

    Args:
        graph_file: Path to graph JSON file (relative to graphs directory)
        start_node: Starting node ID for traversal
        filters: Context filters (e.g., {"location": "Texas", "property_type": "rural"})
        max_depth: Maximum traversal depth
        output_format: Output format (list, markdown, json)

    Returns:
        Dict with generated procedure steps and metadata

    Example:
        ```python
        result = await generate_procedure(
            graph_file="mortgage_underwriting.json",
            start_node="Loan Application",
            filters={"location": "New Mexico", "property_type": "rural"},
            output_format="markdown"
        )
        ```
    """
    try:
        filters = filters or {}

        # Load graph
        graph_path = settings.graphs_dir / graph_file
        if not graph_path.exists():
            return {
                "success": False,
                "error": f"Graph file not found: {graph_file}",
            }

        graph = GraphEngine()
        graph.load_from_file(graph_path)

        # Validate start node
        if start_node not in graph.graph.nodes:
            return {
                "success": False,
                "error": f"Start node not found: {start_node}",
                "available_nodes": list(graph.graph.nodes)[:10],
            }

        # Traverse graph
        visited = graph.traverse_bfs(start_node, filters=filters, max_depth=max_depth)

        # Filter to process nodes only
        procedure_steps = [
            node_id for node_id in visited
            if graph.graph.nodes[node_id].get("type") == NodeType.PROCESS.value
        ]

        # Get metadata for each step
        steps_with_metadata = []
        for step in procedure_steps:
            node_data = graph.graph.nodes[step]
            metadata = {
                "id": step,
                "label": node_data.get("label", step),
                "type": node_data.get("type"),
            }

            # Get role and system
            for neighbor in graph.graph.successors(step):
                relation = graph.graph[step][neighbor].get("relation")
                neighbor_type = graph.graph.nodes[neighbor].get("type")

                if relation == "performed_by":
                    metadata["role"] = neighbor
                if relation == "requires" and neighbor_type == "system":
                    metadata["system"] = neighbor

            steps_with_metadata.append(metadata)

        # Format output
        if output_format == "markdown":
            lines = ["# Generated Procedure\n"]
            lines.append(f"**Context:** {', '.join(f'{k}={v}' for k, v in filters.items())}\n")
            lines.append("## Steps\n")
            for idx, step in enumerate(steps_with_metadata, 1):
                line = f"{idx}. **{step['label']}**"
                hints = []
                if step.get("role"):
                    hints.append(f"Role: {step['role']}")
                if step.get("system"):
                    hints.append(f"System: {step['system']}")
                if hints:
                    line += f" — {', '.join(hints)}"
                lines.append(line)
            content = "\n".join(lines)
        elif output_format == "json":
            import json
            content = json.dumps({
                "procedure": steps_with_metadata,
                "filters": filters,
                "start_node": start_node,
                "num_steps": len(procedure_steps),
            }, indent=2)
        else:  # list
            content = "\n".join(f"{idx}. {step['label']}" for idx, step in enumerate(steps_with_metadata, 1))

        logger.info(f"Generated procedure with {len(procedure_steps)} steps from {start_node}")

        return {
            "success": True,
            "num_steps": len(procedure_steps),
            "steps": steps_with_metadata,
            "content": content,
            "format": output_format,
            "filters_applied": filters,
            "start_node": start_node,
            "graph_stats": graph.get_statistics(),
        }

    except Exception as e:
        logger.error(f"Failed to generate procedure: {e}")
        return {
            "success": False,
            "error": str(e),
            "graph_file": graph_file,
        }
