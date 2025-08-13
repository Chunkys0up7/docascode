from __future__ import annotations

from typing import Dict, List, TypedDict


class SourceItem(TypedDict, total=False):
	title: str
	path: str  # relative repository path like Docs/...
	url: str   # optional external URL
	lines: str # optional line-range hint e.g., "L10-L45"


# Map step slugs to sources for traceability (line of sight)
STEP_SOURCES: Dict[str, List[SourceItem]] = {
	"verify-credit-score": [
		{"title": "Plan notes", "path": "Docs/GPTPlan.txt"},
		{"title": "Project overview", "path": "Docs/ProjectOverview"},
	],
	"request-appraisal": [
		{"title": "Plan notes", "path": "Docs/GPTPlan.txt"},
	],
	"rural-property-appraisal": [
		{"title": "Plan notes", "path": "Docs/GPTPlan.txt"},
	],
	"check-nm-mortgage-rule-12": [
		{"title": "Plan notes", "path": "Docs/GPTPlan.txt"},
	],
	"generate-approval-document": [
		{"title": "Plan notes", "path": "Docs/GPTPlan.txt"},
	],
}


