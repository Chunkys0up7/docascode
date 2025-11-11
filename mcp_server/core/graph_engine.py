"""Generic knowledge graph engine with NetworkX backend."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx
from loguru import logger

from mcp_server.models.schemas import EdgeRelation, GraphEdge, GraphNode, KnowledgeGraph, NodeType


class GraphEngine:
    """Generic knowledge graph operations using NetworkX."""

    def __init__(self) -> None:
        """Initialize empty directed graph."""
        self.graph: nx.DiGraph = nx.DiGraph()

    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph."""
        self.graph.add_node(node.id, label=node.label, type=node.type.value, **node.properties)
        logger.debug(f"Added node: {node.id} ({node.type.value})")

    def add_edge(self, edge: GraphEdge) -> None:
        """Add an edge to the graph."""
        self.graph.add_edge(
            edge.source, edge.target, relation=edge.relation.value, **edge.properties
        )
        logger.debug(f"Added edge: {edge.source} --[{edge.relation.value}]--> {edge.target}")

    def remove_node(self, node_id: str) -> None:
        """Remove a node and its edges."""
        if node_id in self.graph:
            self.graph.remove_node(node_id)
            logger.debug(f"Removed node: {node_id}")

    def remove_edge(self, source: str, target: str) -> None:
        """Remove an edge."""
        if self.graph.has_edge(source, target):
            self.graph.remove_edge(source, target)
            logger.debug(f"Removed edge: {source} --> {target}")

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by ID."""
        if node_id not in self.graph:
            return None

        data = self.graph.nodes[node_id]
        return GraphNode(
            id=node_id,
            label=data.get("label", node_id),
            type=NodeType(data.get("type", "concept")),
            properties={k: v for k, v in data.items() if k not in ["label", "type"]},
        )

    def get_neighbors(
        self, node_id: str, relation: Optional[EdgeRelation] = None, direction: str = "out"
    ) -> List[str]:
        """Get neighboring nodes, optionally filtered by relation and direction."""
        if node_id not in self.graph:
            return []

        if direction == "out":
            neighbors = list(self.graph.successors(node_id))
            if relation:
                neighbors = [
                    n
                    for n in neighbors
                    if self.graph[node_id][n].get("relation") == relation.value
                ]
        elif direction == "in":
            neighbors = list(self.graph.predecessors(node_id))
            if relation:
                neighbors = [
                    n
                    for n in neighbors
                    if self.graph[n][node_id].get("relation") == relation.value
                ]
        else:  # both
            out_neighbors = set(self.graph.successors(node_id))
            in_neighbors = set(self.graph.predecessors(node_id))
            neighbors = list(out_neighbors | in_neighbors)
            if relation:
                filtered = []
                for n in neighbors:
                    if n in out_neighbors and self.graph[node_id][n].get("relation") == relation.value:
                        filtered.append(n)
                    elif n in in_neighbors and self.graph[n][node_id].get("relation") == relation.value:
                        filtered.append(n)
                neighbors = filtered

        return neighbors

    def find_path(
        self, start: str, end: str, max_depth: int = 10
    ) -> Optional[List[str]]:
        """Find shortest path between two nodes."""
        try:
            path = nx.shortest_path(self.graph, start, end)
            if len(path) <= max_depth + 1:
                return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            pass
        return None

    def traverse_bfs(
        self,
        start: str,
        filters: Optional[Dict[str, Any]] = None,
        max_depth: int = 10,
    ) -> List[str]:
        """Breadth-first traversal with context-aware filtering.

        Args:
            start: Starting node ID
            filters: Dictionary of filter conditions (e.g., {"location": "Texas", "property_type": "rural"})
            max_depth: Maximum traversal depth

        Returns:
            List of visited node IDs in BFS order
        """
        if start not in self.graph:
            return []

        filters = filters or {}
        visited: List[str] = []
        queue: List[Tuple[str, int]] = [(start, 0)]
        seen: Set[str] = {start}

        while queue:
            current, depth = queue.pop(0)

            if depth > max_depth:
                continue

            visited.append(current)

            for neighbor in self.graph.successors(current):
                if neighbor in seen:
                    continue

                edge_data = self.graph[current][neighbor]
                relation = edge_data.get("relation")

                # Apply filtering logic
                if not self._should_include_node(neighbor, relation, filters):
                    continue

                seen.add(neighbor)
                queue.append((neighbor, depth + 1))

        return visited

    def _should_include_node(
        self, node_id: str, relation: Optional[str], filters: Dict[str, Any]
    ) -> bool:
        """Determine if a node should be included based on filters."""
        if not filters:
            return True

        node_data = self.graph.nodes[node_id]

        # Conditional filtering
        if relation == "conditional_on":
            # Check if node label matches conditional criteria
            node_label = node_data.get("label", "").lower()
            for key, value in filters.items():
                if value and str(value).lower() in node_label:
                    return True
            return False

        # Context filtering (applies_to)
        if relation == "applies_to":
            node_label = node_data.get("label", "").lower()
            for key, value in filters.items():
                if value and str(value).lower() in node_label:
                    return True
            return False

        # For process nodes, check their context constraints
        if node_data.get("type") == "process":
            context_nodes = [
                n
                for n in self.graph.successors(node_id)
                if self.graph[node_id][n].get("relation") == "applies_to"
            ]

            if context_nodes:
                # Must match at least one context
                for ctx_node in context_nodes:
                    ctx_label = self.graph.nodes[ctx_node].get("label", "").lower()
                    for key, value in filters.items():
                        if value and str(value).lower() in ctx_label:
                            return True
                return False

        return True

    def get_nodes_by_type(self, node_type: NodeType) -> List[GraphNode]:
        """Get all nodes of a specific type."""
        nodes = []
        for node_id, data in self.graph.nodes(data=True):
            if data.get("type") == node_type.value:
                nodes.append(
                    GraphNode(
                        id=node_id,
                        label=data.get("label", node_id),
                        type=node_type,
                        properties={k: v for k, v in data.items() if k not in ["label", "type"]},
                    )
                )
        return nodes

    def export_to_model(self) -> KnowledgeGraph:
        """Export graph to KnowledgeGraph model."""
        nodes = []
        for node_id, data in self.graph.nodes(data=True):
            nodes.append(
                GraphNode(
                    id=node_id,
                    label=data.get("label", node_id),
                    type=NodeType(data.get("type", "concept")),
                    properties={k: v for k, v in data.items() if k not in ["label", "type"]},
                )
            )

        edges = []
        for source, target, data in self.graph.edges(data=True):
            edges.append(
                GraphEdge(
                    source=source,
                    target=target,
                    relation=EdgeRelation(data.get("relation", "related_to")),
                    properties={k: v for k, v in data.items() if k != "relation"},
                )
            )

        return KnowledgeGraph(nodes=nodes, edges=edges)

    def load_from_model(self, knowledge_graph: KnowledgeGraph) -> None:
        """Load graph from KnowledgeGraph model."""
        self.graph.clear()
        for node in knowledge_graph.nodes:
            self.add_node(node)
        for edge in knowledge_graph.edges:
            self.add_edge(edge)
        logger.info(
            f"Loaded graph with {len(knowledge_graph.nodes)} nodes and {len(knowledge_graph.edges)} edges"
        )

    def save_to_file(self, file_path: Path) -> None:
        """Save graph to JSON file."""
        kg = self.export_to_model()
        data = {
            "nodes": [n.model_dump() for n in kg.nodes],
            "edges": [e.model_dump() for e in kg.edges],
            "metadata": kg.metadata,
        }
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved graph to {file_path}")

    def load_from_file(self, file_path: Path) -> None:
        """Load graph from JSON file."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        nodes = [GraphNode(**n) for n in data.get("nodes", [])]
        edges = [GraphEdge(**e) for e in data.get("edges", [])]
        kg = KnowledgeGraph(nodes=nodes, edges=edges, metadata=data.get("metadata", {}))

        self.load_from_model(kg)
        logger.info(f"Loaded graph from {file_path}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics."""
        return {
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "node_types": {
                node_type.value: len(self.get_nodes_by_type(node_type))
                for node_type in NodeType
            },
            "is_directed": self.graph.is_directed(),
            "is_connected": nx.is_weakly_connected(self.graph) if self.graph.number_of_nodes() > 0 else False,
        }
