from __future__ import annotations

from typing import List, Tuple
import networkx as nx


def generate_procedure(
	graph: nx.DiGraph,
	location: str | None,
	property_type: str | None,
) -> List[str]:
	"""Traverses from 'Loan Application' and includes only relevant steps.

	Rules:
	- conditional_on edges from "Request Appraisal" to "Rural Property Appraisal" only fire for rural.
	- applies_to edges must match the location if present.
	- The output is ordered by a BFS traversal and filtered to node type == process.
	"""
	if "Loan Application" not in graph:
		return []

	visited: list[str] = []
	queue: list[str] = ["Loan Application"]

	while queue:
		current = queue.pop(0)
		if current in visited:
			continue
		visited.append(current)

		for neighbor in graph.successors(current):
			relation = graph[current][neighbor].get("relation")

			if relation == "conditional_on" and property_type != "rural":
				continue
			if relation == "applies_to" and location and location not in neighbor:
				# Only include the location node if it matches; otherwise skip
				continue

			# If we are about to enqueue a process node, enforce its applies_to constraints
			if graph.nodes[neighbor].get("type") == "process":
				# Gather all applies_to context nodes from this process
				context_targets: list[str] = []
				for nxt in graph.successors(neighbor):
					if graph[neighbor][nxt].get("relation") == "applies_to":
						context_targets.append(nxt)
				# If process has context constraints, require a match with provided context
				if context_targets:
					matches = False
					for ctx_name in context_targets:
						lc = ctx_name.lower()
						if location and location.lower() in lc:
							matches = True
						if property_type and property_type.lower() in lc:
							matches = True
					if not matches:
						# Skip this process entirely if none of its contexts match
						continue

			queue.append(neighbor)

	procedure = [
		node for node in visited if graph.nodes[node].get("type") == "process"
	]
	return procedure


def annotate_steps_with_metadata(
	graph: nx.DiGraph, steps: List[str]
) -> List[Tuple[str, str]]:
	"""Attach lightweight metadata (role/system hints) for display.

	Returns list of (step, hint) tuples.
	"""
	annotated: list[tuple[str, str]] = []
	for step in steps:
		role = None
		system = None
		for neighbor in graph.successors(step):
			rel = graph[step][neighbor].get("relation")
			if rel == "performed_by":
				role = neighbor
			elif rel == "requires" and graph.nodes[neighbor].get("type") == "system":
				system = neighbor
		hint_parts = []
		if role:
			hint_parts.append(role)
		if system:
			hint_parts.append(f"via {system}")
		hint = " — ".join(hint_parts) if hint_parts else ""
		annotated.append((step, hint))
	return annotated


