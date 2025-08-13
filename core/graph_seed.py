from __future__ import annotations

import networkx as nx


def build_sample_graph() -> nx.DiGraph:
	"""Create the underwriting sample knowledge graph in memory.

	Node types: process, system, role, regulation, context
	Edge relations: requires, performed_by, applies_to, conditional_on, precedes
	"""
	graph: nx.DiGraph = nx.DiGraph()

	# Nodes
	nodes = [
		("Loan Application", "process"),
		("Verify Credit Score", "process"),
		("Credit Bureau API", "system"),
		("Underwriter", "role"),
		("Request Appraisal", "process"),
		("Property Database API", "system"),
		("Appraiser", "role"),
		("Rural Property Appraisal", "process"),
		("Rural Property", "context"),
		("Special Appraisal Form", "system"),
		("Check NM Mortgage Rule 12", "process"),
		("New Mexico", "context"),
		("Regulatory DB", "system"),
		("Generate Approval Document", "process"),
		("Document Gen API", "system"),
		("Loan Officer", "role"),
	]
	for name, node_type in nodes:
		graph.add_node(name, type=node_type)

	# Edges
	edges = [
		("Loan Application", "Verify Credit Score", "requires"),
		("Verify Credit Score", "Credit Bureau API", "requires"),
		("Verify Credit Score", "Underwriter", "performed_by"),
		("Verify Credit Score", "Request Appraisal", "precedes"),
		("Request Appraisal", "Property Database API", "requires"),
		("Request Appraisal", "Appraiser", "performed_by"),
		("Request Appraisal", "Rural Property Appraisal", "conditional_on"),
		("Rural Property Appraisal", "Rural Property", "applies_to"),
		("Rural Property Appraisal", "Special Appraisal Form", "requires"),
		("Loan Application", "Check NM Mortgage Rule 12", "requires"),
		("Check NM Mortgage Rule 12", "New Mexico", "applies_to"),
		("Check NM Mortgage Rule 12", "Regulatory DB", "requires"),
		("Loan Application", "Generate Approval Document", "precedes"),
		("Generate Approval Document", "Document Gen API", "requires"),
		("Generate Approval Document", "Loan Officer", "performed_by"),
	]
	for source, target, relation in edges:
		graph.add_edge(source, target, relation=relation)

	return graph


