from __future__ import annotations

import os
import sys
from pathlib import Path
import pandas as pd
import time
import streamlit as st

# Ensure project root is importable when Streamlit sets CWD to app/
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
	sys.path.insert(0, str(_ROOT))

from core.graph_seed import build_sample_graph
from core.nlp import parse_free_text_query
from core.procedure import generate_procedure, annotate_steps_with_metadata
from core.visualize import build_pyvis_graph, build_graphviz_dot, TYPE_TO_COLOR
from core.export_md import export_procedure_markdown
from core.dummy_data import get_step_dummy_data
from core.sources import STEP_SOURCES


def _business_guidance_for_step(step: str) -> list[str]:
	"""Provides sample business guidance for specific steps."""
	name = step.lower()
	if "verify credit score" in name:
		return [
			"Confirm identity before retrieving credit data",
			"Proceed only if score meets program threshold",
			"Record rationale for any exceptions",
		]
	if "request appraisal" in name:
		return [
			"Validate property address and parcel",
			"Communicate expected turnaround to borrower",
		]
	if "rural property appraisal" in name:
		return [
			"Use rural comparables where available",
			"Attach special appraisal form to case file",
		]
	if "check nm mortgage rule 12" in name:
		return [
			"Ensure NM disclosures are included",
			"Capture evidence for audit",
		]
	if "generate approval document" in name:
		return [
			"Verify borrower details and terms",
			"Send for QA prior to issuance",
		]
	return ["Follow standard operating procedure for this step"]


st.set_page_config(page_title="Dynamic Docs POC", layout="wide", initial_sidebar_state="collapsed")
st.title("Dynamic Docs POC — Graph-Based Dynamic Procedures")
st.caption("Interactive procedure generator — concise, business-friendly outputs")

# --- Centralized Styling for Improved Maintainability & Aesthetics ---
st.markdown(
	"""
	<style>
	/* Global Streamlit Overrides */
	h1 { margin-top: 0; padding-top: 0; }
	h2 { margin-top: 1.5rem; }
	h3 { margin-top: 1rem; }

	/* Card Styling */
	.card {
		border: 1px solid #e5e7eb;
		border-radius: 10px;
		padding: 18px 20px;
		margin: 15px 0;
		background: #ffffff;
		box-shadow: 0 1px 3px rgba(0,0,0,0.05);
	}
	.card h4 {
		margin: 0 0 10px 0;
		font-size: 1.25rem;
		color: #1a202c;
	}

	/* Section Headers within Cards */
	.section {
		margin-top: 16px;
		margin-bottom: 8px;
		font-weight: 600;
		color: #4a5568;
	}

	/* Key-Value Pair Display (inputs, outputs, KPIs) */
	.kv {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		margin-bottom: 10px;
	}
	.kv .item {
		background: #f0f4f8;
		border: 1px solid #dce2e8;
		border-radius: 6px;
		padding: 6px 10px;
		font-size: 0.9rem;
		color: #2d3748;
	}
	.kv .item strong {
		color: #1a202c;
	}

	/* Pills (Context, Metadata) */
	.pill {
		display: inline-block;
		margin: 0 6px 6px 0;
		padding: 6px 12px;
		border-radius: 999px;
		background: #e0e7ff;
		color: #312e81;
		font-size: 0.85rem;
		font-weight: 500;
	}
	.pill strong {
		color: #2b1f83;
	}

	/* Hints */
	.hint {
		color: #6b7280;
		font-size: 0.9rem;
		margin-left: 0;
		margin-bottom: 12px;
		font-style: italic;
	}

	/* Legend */
	.legend-item {
		display: inline-flex;
		align-items: center;
		margin-right: 18px;
		margin-bottom: 8px;
		font-size: 0.9rem;
		color: #4a5568;
	}
	.legend-swatch {
		width: 12px;
		height: 12px;
		border-radius: 3px;
		margin-right: 8px;
		border: 1px solid #cbd5e0;
	}
	</style>
	""",
	unsafe_allow_html=True,
)


@st.cache_resource
def get_graph():
	return build_sample_graph()


@st.cache_data
def load_borrowers() -> pd.DataFrame:
	return pd.read_csv("data/borrowers.csv")


graph = get_graph()
borrowers_df = load_borrowers()

# --- Request Parameters Section ---
st.subheader("Request Parameters")
st.markdown("Define the context for the procedure generation.")

# Initialize session state for docs_base_url and form inputs
if "docs_base_url" not in st.session_state:
	st.session_state["docs_base_url"] = "http://localhost:8000"
if "query_text_form" not in st.session_state:
	st.session_state["query_text_form"] = "Underwrite home loan for a first-time buyer in New Mexico with rural property"
if "selected_borrower_form" not in st.session_state:
	st.session_state["selected_borrower_form"] = borrowers_df["name"].tolist()[0]
if "run_procedure" not in st.session_state:
	st.session_state["run_procedure"] = False


col_cfg1, col_cfg2 = st.columns([3, 2])
with col_cfg2:
	st.session_state["docs_base_url"] = st.text_input(
		"Docs site base URL",
		value=st.session_state["docs_base_url"],
		help="Used for external links to the MkDocs site (e.g., `http://localhost:8000`)",
		key="docs_base_url_input",
	)
with col_cfg1:
	st.write(" ")

with st.form("inputs_form", clear_on_submit=False):
	mode = st.radio("Input Mode", ["Free Text", "Borrower Sample"], index=0, horizontal=True, key="input_mode_radio")

	query_text = ""
	selected_borrower = None

	if mode == "Free Text":
		examples = [
			"Underwrite home loan for a first-time buyer in New Mexico with rural property",
			"Underwrite home loan for a veteran in Texas with urban property",
		]
		col_e1, col_e2 = st.columns([2, 5])
		with col_e1:
			example_choice = st.selectbox(
				"Choose an example query",
				options=["(Type your own)"] + examples,
				index=0,
				key="example_choice_select",
			)

		with col_e2:
			current_query_value = example_choice if example_choice != "(Type your own)" else st.session_state["query_text_form"]
			query_text = st.text_area(
				"Describe the task or refine example",
				value=current_query_value,
				height=120,
				key="query_text_input",
			)
			if query_text != st.session_state["query_text_form"] and example_choice == "(Type your own)":
				st.session_state["query_text_form"] = query_text

	else:
		borrower_names = borrowers_df["name"].tolist()
		selected_borrower_index = borrower_names.index(st.session_state["selected_borrower_form"]) if st.session_state["selected_borrower_form"] in borrower_names else 0
		selected_borrower = st.selectbox(
			"Choose a borrower profile",
			borrower_names,
			key="borrower_select",
			index=selected_borrower_index,
		)
		st.session_state["selected_borrower_form"] = selected_borrower

	submitted = st.form_submit_button("Generate Procedure", use_container_width=True, type="primary")
	if submitted:
		st.session_state["run_procedure"] = True
		st.session_state["mode"] = mode
		st.session_state["query_text_for_proc"] = query_text if mode == "Free Text" else ""
		st.session_state["borrower_name_for_proc"] = selected_borrower if mode == "Borrower Sample" else ""


def derive_context_from_borrower(df: pd.DataFrame, name: str):
	"""Derives context dictionary from borrower DataFrame row."""
	row = df.loc[df["name"] == name].iloc[0]
	return {
		"loan_type": "home_loan",
		"location": row["location"],
		"property_type": row["property_type"],
		"is_first_time_buyer": str(row["first_time_buyer"]).lower().startswith("y"),
		"is_veteran": str(row["veteran"]).lower().startswith("y"),
	}


# --- Main Application Logic & Display ---
run_procedure = st.session_state.get("run_procedure", False)

if not run_procedure:
	if "exported_docs" in st.session_state:
		del st.session_state["exported_docs"]
	st.info("💡 Enter a query or select a borrower above, then click 'Generate Procedure' to see the dynamic steps.")
else:
	mode = st.session_state.get("mode")
	query_text_display = ""
	ctx_display = {}
	location = None
	property_type = None

	if mode == "Free Text":
		query_text = st.session_state.get("query_text_for_proc", "")
		parsed = parse_free_text_query(query_text)
		location = parsed.location
		property_type = parsed.property_type
		ctx_display = {
			"Location": location or "—",
			"Property": property_type or "—",
			"First-time buyer": "Yes" if parsed.is_first_time_buyer else "No",
			"Veteran": "Yes" if parsed.is_veteran else "No",
		}
		query_text_display = query_text
	else:
		borrower_name = st.session_state.get("borrower_name_for_proc")
		ctx = derive_context_from_borrowers(borrowers_df, borrower_name) if False else derive_context_from_borrower(borrowers_df, borrower_name)
		query_text_display = f"Underwrite {ctx['loan_type']} for {borrower_name} in {ctx['location']} with {ctx['property_type']} property"
		location = ctx["location"]
		property_type = ctx["property_type"]
		ctx_display = {
			"Borrower": borrower_name,
			"Location": location,
			"Property": property_type,
			"First-time buyer": "Yes" if ctx["is_first_time_buyer"] else "No",
			"Veteran": "Yes" if ctx["is_veteran"] else "No",
		}

	# --- Generation with Loading Feedback ---
	steps = []
	annotated = []
	with st.spinner("Analyzing request and generating procedure..."):
		# time.sleep(1)
		steps = generate_procedure(graph, location=location, property_type=property_type)
		annotated = annotate_steps_with_metadata(graph, steps)

	# --- Context Chips Display ---
	st.subheader("Context")
	chips = []
	for label, value in ctx_display.items():
		if value and value != '—':
			chips.append(f"<span class='pill'><strong>{label}:</strong> {value}</span>")

	if chips:
		st.markdown(" ".join(chips), unsafe_allow_html=True)
	else:
		st.info("No specific context derived for this query. The procedure is based on general rules.")

	# Optional role filter derived from step metadata
	_available_roles: list[str] = []
	try:
		for step, _ in annotated:
			md = get_step_dummy_data(step, graph=graph, context={
				"location": location,
				"property_type": property_type,
				"borrower": st.session_state.get("borrower_name_for_proc", "Alice Smith"),
				"loan_type": "home_loan",
			}).get("metadata", {})
			role_name = md.get("role")
			if role_name and role_name not in _available_roles:
				_available_roles.append(role_name)
	except Exception:
		pass
	role_filter = st.multiselect("Filter by role", options=sorted(_available_roles), default=[])

	def _matches_role(step_name: str) -> bool:
		if not role_filter:
			return True
		md = get_step_dummy_data(step_name, graph=graph, context={
			"location": location,
			"property_type": property_type,
			"borrower": st.session_state.get("borrower_name_for_proc", "Alice Smith"),
			"loan_type": "home_loan",
		}).get("metadata", {})
		return md.get("role") in set(role_filter)

	annotated_display = [(s, h) for (s, h) in annotated if _matches_role(s)]
	steps_display = [s for (s, _h) in annotated_display]

	tab_steps, tab_graph, tab_details, tab_export = st.tabs(["Procedure Steps", "Graph View", "Details & Traceability", "Export"])

	with tab_steps:
		st.subheader("Generated Steps")
		for idx, (step, hint) in enumerate(annotated_display, start=1):
			slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in step).strip("-")
			docs_base_url = st.session_state.get("docs_base_url", "http://localhost:8000")
			link_dir = f"{docs_base_url.rstrip('/')}/reference/{slug}/"
			link_html = f"{docs_base_url.rstrip('/')}/reference/{slug}.html"

			st.markdown(f"<div class='card'>", unsafe_allow_html=True)
			st.markdown(f"<h4>{idx}. {step}</h4>", unsafe_allow_html=True)
			if hint:
				st.markdown(f"<div class='hint'>{hint}</div>", unsafe_allow_html=True)

			# Dummy data to enrich step display
			demo = get_step_dummy_data(step, graph=graph, context={
				"location": location,
				"property_type": property_type,
				"borrower": st.session_state.get("borrower_name_for_proc", "Alice Smith"),
				"loan_type": "home_loan",
			})

			# Use columns for overall layout within the card for main content
			col_left_card, col_right_card = st.columns([3, 2])

			with col_left_card:
				# Metadata chips
				meta = demo.get("metadata", {})
				chips = []
				if meta.get("role"): chips.append(f"<span class='pill'><strong>Role:</strong> {meta['role']}</span>")
				if meta.get("system"): chips.append(f"<span class='pill'><strong>System:</strong> {meta['system']}</span>")

				loc_meta = (meta.get("context") or {}).get("location") or ""
				ptype_meta = (meta.get("context") or {}).get("property_type") or ""
				if loc_meta: chips.append(f"<span class='pill'><strong>Location:</strong> {loc_meta}</span>")
				if ptype_meta: chips.append(f"<span class='pill'><strong>Property:</strong> {ptype_meta}</span>")

				if chips:
					st.markdown("<div class='section'>Metadata</div>", unsafe_allow_html=True)
					st.markdown(" ".join(chips), unsafe_allow_html=True)

				# Inputs - using the custom KV display
				inputs = demo.get("inputs") or {}
				if inputs:
					st.markdown("<div class='section'>Inputs</div>", unsafe_allow_html=True)
					st.markdown("<div class='kv'>", unsafe_allow_html=True)
					for k, v in inputs.items():
						st.markdown(f"<div class='item'><strong>{k}:</strong> {v}</div>", unsafe_allow_html=True)
					st.markdown("</div>", unsafe_allow_html=True)

				# KPIs - using the custom KV display
				kpis = demo.get("kpis") or {}
				if kpis:
					st.markdown("<div class='section'>KPIs</div>", unsafe_allow_html=True)
					st.markdown("<div class='kv'>", unsafe_allow_html=True)
					for k, v in kpis.items():
						st.markdown(f"<div class='item'><strong>{k}:</strong> {v}</div>", unsafe_allow_html=True)
					st.markdown("</div>", unsafe_allow_html=True)
					
			with col_right_card:
				# Outputs - using the custom KV display
				outputs = demo.get("outputs") or {}
				if outputs:
					st.markdown("<div class='section'>Outputs</div>", unsafe_allow_html=True)
					st.markdown("<div class='kv'>", unsafe_allow_html=True)
					for k, v in outputs.items():
						st.markdown(f"<div class='item'><strong>{k}:</strong> {v}</div>", unsafe_allow_html=True)
					st.markdown("</div>", unsafe_allow_html=True)

				# Business guidance
				st.markdown("<div class='section'>Business Guidance</div>", unsafe_allow_html=True)
				bullets = _business_guidance_for_step(step)
				for b in bullets:
					st.markdown(f"- {b}")

				# Sub-steps (hidden in expander for less clutter)
				sub_steps = demo.get("sub_steps") or []
				if sub_steps:
					with st.expander("Show Sub-steps"):
						for s in sub_steps:
							st.markdown(f"- {s}")

				# Sample API (hidden in expander)
				sample_api = demo.get("sample_api") or {}
				if sample_api:
					with st.expander("Show Sample API Call"):
						st.json(sample_api)

			# Footer row with timing + reference link
			dur = demo.get("duration_estimate_minutes")
			ts = demo.get("timestamp")
			
			footer_cols = st.columns([1, 1, 1])
			with footer_cols[0]:
				footer_text_items = []
				if dur:
					footer_text_items.append(f"⏱ {dur} min")
				if ts:
					footer_text_items.append(f"⏰ {ts}")
				if footer_text_items:
					st.caption(" | ".join(footer_text_items))
			
			with footer_cols[1]:
				ref_md_path = f"site_docs/reference/{slug}.md"
				if os.path.exists(ref_md_path):
					st.markdown(f"📖 [Open in Docs]({link_dir})  ·  [HTML]({link_html})")
				else:
					st.caption("Export to MkDocs to enable Docs link")

			with footer_cols[2]:
				# In-app reference: refined feedback and cached content
				if st.session_state.get("exported_docs", {}).get(slug):
					with st.expander("📄 View Reference (in-app)"):
						st.markdown(st.session_state["exported_docs"][slug])
				else:
					with st.expander("📄 View Reference (in-app)"):
						st.info("Reference content will appear here after you 'Export to MkDocs'.")
			
			st.markdown("</div>", unsafe_allow_html=True)

	with tab_graph:
		st.subheader("Graph View")
		view_mode = st.radio("View", ["Full graph", "Relevant only"], index=1, horizontal=True, key="graph_view_mode")
		# Legend
		legend_items = []
		for t, color in TYPE_TO_COLOR.items():
			legend_items.append(f"<span class='legend-item'><span class='legend-swatch' style='background:{color}'></span>{t.title()}</span>")
		st.markdown(" ".join(legend_items), unsafe_allow_html=True)
		
		visible_nodes = None
		if view_mode == "Relevant only":
			visible_nodes = set(steps)
			# include immediate neighbors for context
			for n in list(visible_nodes):
				for succ in graph.successors(n):
					visible_nodes.add(succ)
				for pred in graph.predecessors(n):
					visible_nodes.add(pred)
		# Robust Graphviz rendering with backward-compat for older signature
		highlight = steps_display if role_filter else steps
		try:
			dot = build_graphviz_dot(graph, highlight_path=highlight, visible_nodes=visible_nodes)
		except TypeError:
			dot = build_graphviz_dot(graph, highlight_path=highlight)
		st.graphviz_chart(dot, use_container_width=True)

	with tab_details:
		st.subheader("Details & Traceability")
		st.write("Query Used:")
		st.code(query_text_display)
		
		st.markdown("---")
		st.write("Per-step details, links, and sources:")
		docs_base_url = st.session_state.get("docs_base_url", "http://localhost:8000")
		for idx, (step, hint) in enumerate(annotated_display, start=1):
			slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in step).strip("-")
			link_dir = f"{docs_base_url.rstrip('/')}/reference/{slug}/"
			link_html = f"{docs_base_url.rstrip('/')}/reference/{slug}.html"
			
			# Header with optional hint
			st.markdown(f"#### {idx}. {step}")
			if hint:
				st.markdown(f"<span class='hint'>{hint}</span>", unsafe_allow_html=True)
			
			# Metadata and links side-by-side
			colA, colB = st.columns([2, 1])
			with colA:
				# Derive lightweight metadata for traceability view
				demo_meta = get_step_dummy_data(step, graph=graph, context={
					"location": location,
					"property_type": property_type,
					"borrower": st.session_state.get("borrower_name_for_proc", "Alice Smith"),
					"loan_type": "home_loan",
				}).get("metadata", {})
				chips = []
				if demo_meta.get("role"):
					chips.append(f"<span class='pill'><strong>Role:</strong> {demo_meta['role']}</span>")
				if demo_meta.get("system"):
					chips.append(f"<span class='pill'><strong>System:</strong> {demo_meta['system']}</span>")
				loc_meta = (demo_meta.get("context") or {}).get("location") or ""
				ptype_meta = (demo_meta.get("context") or {}).get("property_type") or ""
				if loc_meta:
					chips.append(f"<span class='pill'><strong>Location:</strong> {loc_meta}</span>")
				if ptype_meta:
					chips.append(f"<span class='pill'><strong>Property:</strong> {ptype_meta}</span>")
				if chips:
					st.markdown(" ".join(chips), unsafe_allow_html=True)
			with colB:
				ref_md_path = f"site_docs/reference/{slug}.md"
				if os.path.exists(ref_md_path):
					st.markdown(f"📖 [Open in Docs]({link_dir})  ·  [HTML]({link_html})  ·  [Reference Index]({docs_base_url.rstrip('/')}/reference/)")
				else:
					st.caption("Export to MkDocs to enable Docs link")
				if st.session_state.get("exported_docs", {}).get(slug):
					with st.expander("📄 View Reference (in-app)"):
						st.markdown(st.session_state["exported_docs"][slug])
				else:
					with st.expander("📄 View Reference (in-app)"):
						st.info("Reference content will appear here after you 'Export to MkDocs'.")
			
			# Sources list
			srcs = STEP_SOURCES.get(slug, [])
			if srcs:
				st.markdown("<div class='section'>Sources</div>", unsafe_allow_html=True)
				for s in srcs:
					title = s.get("title") or "Source"
					if s.get("path"):
						lines_note = f" ({s['lines']})" if s.get("lines") else ""
						st.markdown(f"- `{s['path']}`{lines_note}")
					if s.get("url"):
						st.markdown(f"  - [Link]({s['url']})")
			st.markdown("---")

	with tab_export:
		st.subheader("Export & Links")
		colA, colB = st.columns([1, 3])
		with colA:
			auto_export = st.toggle("Auto-export after generation", value=False, help="When enabled, exporting runs automatically after generating steps.")
			if st.button("Export to MkDocs", use_container_width=True, type="primary") or auto_export:
				# Initialize or clear exported_docs cache before export
				st.session_state["exported_docs"] = {}
				with st.spinner("Exporting procedure to Markdown..."):
					outfile = export_procedure_markdown(st.session_state["query_text_for_proc"], annotated)
					
					# After successful export, read the generated markdown files into session state
					for idx, (step, hint) in enumerate(annotated, start=1):
						slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in step).strip("-")
						ref_file_path = f"site_docs/reference/{slug}.md"
						if os.path.exists(ref_file_path):
							try:
								with open(ref_file_path, "r", encoding="utf-8") as rf:
									st.session_state["exported_docs"][slug] = rf.read()
							except Exception as e:
								st.session_state["exported_docs"][slug] = f"Error reading file: {e}"
						else:
							st.session_state["exported_docs"][slug] = "*(Content not found after export. File may not have been generated.)*"
					
					st.success(f"Procedure exported to: `{outfile}`")
					st.rerun()

		with colB:
			st.info("Run `mkdocs serve` in your terminal to view the docs site. Exported files appear under the 'Generated' section.")
