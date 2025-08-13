from __future__ import annotations

from typing import Dict, Any
from datetime import datetime

try:
	import networkx as nx  # type: ignore
except Exception:  # pragma: no cover
	# keep optional import to avoid hard dependency in contexts where not needed
	nx = None


def get_step_dummy_data(step_name: str, graph: Any | None = None, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
	"""Return rich demo data payloads per step for display.

	- Derives role/system from the graph if provided
	- Uses provided context (location, property_type, flags)
	- Always returns structured fields (no empty placeholders)
	"""
	name = step_name.lower()
	ctx = context or {}
	role = None
	system = None
	regulation = None

	if graph is not None and hasattr(graph, "successors") and step_name in getattr(graph, "nodes", {}):
		for neighbor in graph.successors(step_name):
			rel = graph[step_name][neighbor].get("relation")
			ntype = graph.nodes[neighbor].get("type")
			if rel == "performed_by":
				role = neighbor
			if rel == "requires" and ntype == "system":
				system = neighbor
			if rel == "applies_to":
				regulation = neighbor
	if "verify credit score" in name:
		return {
			"metadata": {"role": role or "Underwriter", "system": system or "Credit Bureau API", "context": ctx},
			"request": {"ssn": "123-45-6789", "name": ctx.get("borrower", "Alice Smith")},
			"response": {"score": 742, "delinquencies": 0, "report_id": "CR-001"},
			"kpis": {"min_score_required": 700, "measured_score": 742},
			"duration_estimate_minutes": 3,
			"timestamp": datetime.now().isoformat(),
		}
	if "request appraisal" in name:
		return {
			"metadata": {"role": role or "Appraiser", "system": system or "Property Database API", "context": ctx},
			"order": {"address": ctx.get("address", "100 Main St"), "state": ctx.get("location", "New Mexico"), "parcel": "NM-12345", "rush": False},
			"status": {"state": "ordered", "eta_days": 5},
			"duration_estimate_minutes": 10,
			"timestamp": datetime.now().isoformat(),
		}
	if "rural property appraisal" in name:
		return {
			"metadata": {"role": role or "Appraiser", "system": system or "Special Appraisal Form", "context": ctx},
			"checklist": ["rural comps collected", "special form attached", "addendum ready"],
			"risks": ["insufficient rural comps", "outlier valuation"],
			"duration_estimate_minutes": 15,
			"timestamp": datetime.now().isoformat(),
		}
	if "check nm mortgage rule 12" in name:
		return {
			"metadata": {"role": role or "Underwriter", "system": system or "Regulatory DB", "context": ctx},
			"rule": "NM-MR12",
			"requirements": ["Disclosure A", "Disclosure B"],
			"compliant": True,
			"duration_estimate_minutes": 4,
			"timestamp": datetime.now().isoformat(),
		}
	if "generate approval document" in name:
		return {
			"metadata": {"role": role or "Loan Officer", "system": system or "Document Gen API", "context": ctx},
			"inputs": {"borrower": ctx.get("borrower", "Alice Smith"), "loan_type": ctx.get("loan_type", "home_loan")},
			"document": {"id": "DOC-1001", "url": "/mock/docgen/DOC-1001"},
			"duration_estimate_minutes": 2,
			"timestamp": datetime.now().isoformat(),
		}

	# Generic fallback with derived metadata
	return {
		"metadata": {"role": role or "Actor", "system": system or "System", "context": ctx, "applies_to": regulation},
		"inputs": {"case_id": "CASE-0001", "location": ctx.get("location", "Unknown"), "property_type": ctx.get("property_type", "Unknown")},
		"outputs": {"status": "completed", "artifacts": [f"{step_name} result"]},
		"sub_steps": [f"Plan {step_name}", f"Execute {step_name}", f"Validate {step_name}"],
		"sample_api": {
			"endpoint": f"/mock/{step_name.lower().replace(' ', '-')}",
			"request": {"payload": {"step": step_name, "context": ctx}},
			"response": {"ok": True, "step": step_name, "timestamp": datetime.now().isoformat()},
		},
		"duration_estimate_minutes": 5,
		"timestamp": datetime.now().isoformat(),
	}


