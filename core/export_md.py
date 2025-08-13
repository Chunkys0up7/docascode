from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, Tuple


GENERATED_DIR = Path("site_docs/generated")
REFERENCE_DIR = Path("site_docs/reference")


REFERENCE_CONTENT: dict[str, str] = {
	"verify-credit-score": (
		"# Verify Credit Score\n\n"
		"Purpose: Retrieve and validate applicant credit report.\n\n"
		"Role: Underwriter\n\n"
		"System: Credit Bureau API\n\n"
		"## Sub-steps\n"
		"1. Confirm applicant identity\n"
		"2. Query Credit Bureau API\n"
		"3. Validate report and score thresholds\n"
		"4. Record findings in case file\n"
	),
	"request-appraisal": (
		"# Request Appraisal\n\n"
		"Purpose: Initiate property appraisal request.\n\n"
		"Role: Appraiser\n\n"
		"System: Property Database API\n\n"
		"## Sub-steps\n"
		"1. Verify property address and parcel\n"
		"2. Submit appraisal order\n"
		"3. Track appraisal status\n"
	),
	"rural-property-appraisal": (
		"# Rural Property Appraisal\n\n"
		"Purpose: Additional appraisal checks for rural properties.\n\n"
		"Context: Rural Property\n\n"
		"Requires: Special Appraisal Form\n\n"
		"## Sub-steps\n"
		"1. Collect rural-specific comparables\n"
		"2. Complete special appraisal form\n"
		"3. Attach addendum to appraisal\n"
	),
	"check-nm-mortgage-rule-12": (
		"# Check NM Mortgage Rule 12\n\n"
		"Purpose: Ensure NM-specific disclosure compliance.\n\n"
		"Context: New Mexico\n\n"
		"System: Regulatory DB\n\n"
		"## Sub-steps\n"
		"1. Retrieve latest MR12 requirements\n"
		"2. Confirm disclosures present\n"
		"3. Record compliance evidence\n"
	),
	"generate-approval-document": (
		"# Generate Approval Document\n\n"
		"Purpose: Produce final approval document for borrower.\n\n"
		"Role: Loan Officer\n\n"
		"System: Document Gen API\n\n"
		"## Sub-steps\n"
		"1. Assemble case data\n"
		"2. Generate document via API\n"
		"3. QA review and send\n"
	),
}


def export_procedure_markdown(
	query_text: str,
	annotated_steps: Iterable[Tuple[str, str]],
	filename_slug: str | None = None,
) -> Path:
	"""Write a Markdown file under site_docs/generated/ with a timestamped or slugged name."""
	GENERATED_DIR.mkdir(parents=True, exist_ok=True)
	if filename_slug:
		stem = filename_slug
	else:
		stem = datetime.now().strftime("procedure-%Y%m%d-%H%M%S")

	outfile = GENERATED_DIR / f"{stem}.md"

	REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
	step_to_link: dict[str, str] = {}
	for step, _ in annotated_steps:
		slug = _slugify(step)
		ref_file = REFERENCE_DIR / f"{slug}.md"
		if not ref_file.exists():
			content = _build_reference_content(slug, step)
			ref_file.write_text(content, encoding="utf-8")
		step_to_link[step] = f"../reference/{slug}.md"

	lines = [
		"# Generated Procedure\n",
		"\n",
		f"Query: {query_text}\n",
		"\n",
		"## Steps\n",
	]
	for idx, (step, hint) in enumerate(annotated_steps, start=1):
		if hint:
			lines.append(f"{idx}. [{step}]({step_to_link[step]}) — {hint}\n")
		else:
			lines.append(f"{idx}. [{step}]({step_to_link[step]})\n")

	from .sources import STEP_SOURCES
	lines.append("\n## Sources\n")
	for step, _hint in annotated_steps:
		slug = _slugify(step)
		srcs = STEP_SOURCES.get(slug, [])
		if not srcs:
			continue
		lines.append(f"\n### {step}\n")
		for s in srcs:
			if s.get("path"):
				lines.append(f"- `{s['path']}`{(' '+s['lines']) if s.get('lines') else ''}\n")
			if s.get("url"):
				lines.append(f"  - {s['url']}\n")

	outfile.write_text("".join(lines), encoding="utf-8")
	_update_generated_index(stem)
	_refresh_reference_index()
	return outfile


def _update_generated_index(stem: str) -> None:
	"""Append a link to generated/index.md for the new file if it doesn't already exist."""
	index_file = GENERATED_DIR / "index.md"
	index_file.parent.mkdir(parents=True, exist_ok=True)
	if not index_file.exists():
		index_file.write_text("# Generated Procedures\n\n", encoding="utf-8")

	content = index_file.read_text(encoding="utf-8")
	link_line = f"- [{stem}]({stem}.md)\n"
	if link_line not in content:
		content = content + link_line
		index_file.write_text(content, encoding="utf-8")


def _refresh_reference_index() -> None:
	"""Generate a simple index listing of reference pages."""
	index_path = REFERENCE_DIR / "index.md"
	REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
	entries = []
	for md_file in sorted(REFERENCE_DIR.glob("*.md")):
		if md_file.name == "index.md":
			continue
		title = md_file.stem.replace("-", " ").title()
		entries.append(f"- [{title}]({md_file.stem}.md)\n")
	content = ["# Reference\n\n", "Browse reference pages for steps and entities.\n\n"] + entries
	index_path.write_text("".join(content), encoding="utf-8")


def _build_reference_content(slug: str, step: str) -> str:
	"""Compose initial reference page content including sources if available."""
	base = REFERENCE_CONTENT.get(slug, f"# {step}\n\nReference page for {step}.\n")
	# Append sources for traceability
	try:
		from .sources import STEP_SOURCES  # local import
		sources = STEP_SOURCES.get(slug, [])
		if sources:
			lines = [base.rstrip(), "\n\n## Sources\n"]
			for s in sources:
				if s.get("path"):
					lines.append(f"- `{s['path']}`{(' '+s['lines']) if s.get('lines') else ''}\n")
				if s.get("url"):
					lines.append(f"  - {s['url']}\n")
			return "".join(lines)
	except Exception:
		pass
	return base


def _slugify(text: str) -> str:
	out = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
	while "--" in out:
		out = out.replace("--", "-")
	return out.strip("-")

 
