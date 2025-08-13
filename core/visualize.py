from __future__ import annotations

from typing import Iterable, Set
import networkx as nx
from pyvis.network import Network


def build_graphviz_dot(
	graph: nx.DiGraph,
	highlight_path: Iterable[str] | None = None,
	visible_nodes: Set[str] | None = None,
) -> str:
	"""Build a Graphviz DOT string for the given graph.

	Nodes are color-coded by type. Nodes on highlight_path are bold with thicker border.
	"""
	highlight = set(highlight_path) if highlight_path else set()
	lines = ["digraph G {"]
	lines.append("  rankdir=LR;")
	lines.append("  node [shape=box, style=filled, fontname=Helvetica, fontsize=10];")

	for node, attrs in graph.nodes(data=True):
		if visible_nodes is not None and node not in visible_nodes:
			continue
		node_type = attrs.get("type", "process")
		color = TYPE_TO_COLOR.get(node_type, "#999999")
		penwidth = "2" if node in highlight else "1"
		style = "filled,bold" if node in highlight else "filled"
		# Escape quotes
		label = node.replace("\"", "'")
		lines.append(f"  \"{label}\" [fillcolor=\"{color}\", color=\"#374151\", penwidth={penwidth}, style=\"{style}\"];")

	for source, target, attrs in graph.edges(data=True):
		if visible_nodes is not None and (source not in visible_nodes or target not in visible_nodes):
			continue
		relation = attrs.get("relation", "")
		edge_label = relation.replace("\"", "'")
		src = source.replace("\"", "'")
		tgt = target.replace("\"", "'")
		lines.append(f"  \"{src}\" -> \"{tgt}\" [label=\"{edge_label}\", fontname=Helvetica, fontsize=9, color=\"#9CA3AF\"];")

	lines.append("}")
	return "\n".join(lines)


TYPE_TO_COLOR = {
	"process": "#4C78A8",
	"system": "#F58518",
	"role": "#54A24B",
	"regulation": "#E45756",
	"context": "#72B7B2",
}


def build_pyvis_graph(
	graph: nx.DiGraph, highlight_path: Iterable[str] | None = None
) -> Network:
	"""Convert the NetworkX graph to a PyVis network with type-based coloring.

	If highlight_path is provided, those nodes will be given a larger size and a border.
	"""
	net = Network(height="600px", width="100%", directed=True, notebook=False)
	net.barnes_hut()

	highlight_set = set(highlight_path) if highlight_path else set()

	for node, attrs in graph.nodes(data=True):
		node_type = attrs.get("type", "process")
		color = TYPE_TO_COLOR.get(node_type, "#999999")
		size = 18 if node in highlight_set else 12
		border_width = 3 if node in highlight_set else 1
		net.add_node(
			node,
			label=node,
			color=color,
			size=size,
			borderWidth=border_width,
		)

	for source, target, attrs in graph.edges(data=True):
		relation = attrs.get("relation", "")
		net.add_edge(source, target, label=relation)

	return net


