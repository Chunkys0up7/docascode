# Dev Log — Dynamic Docs POC

This log tracks implementation tasks and progress for the full demo.

## 2025-08-13

- [x] Review `Docs/GPTPlan.txt` and `Docs/ProjectOverview` and extract requirements
- [x] Create project scaffold (core modules, app, data, docs, config)
- [x] Implement graph seed (`core/graph_seed.py`)
- [x] Implement lightweight parser (`core/nlp.py`)
- [x] Implement traversal and metadata (`core/procedure.py`)
- [x] Implement PyVis visualization wrapper (`core/visualize.py`)
- [x] Implement Markdown export and generated index auto-update (`core/export_md.py`)
- [x] Build Streamlit UI (`app/streamlit_app.py`)
- [x] Add MkDocs site and navigation (`mkdocs.yml`, `site_docs/`)
- [x] Add sample data (`data/*.csv`)
- [x] Add README with quickstart

Environment & run:

- [x] Set up virtual environment and installed dependencies
- [x] Launched Streamlit app via `python -m streamlit run app/streamlit_app.py`
- [x] Started MkDocs dev server via `python -m mkdocs serve`

Fixes:

- [x] Resolved Streamlit crash: fixed stray `\t` in `core/graph_seed.py` causing SyntaxError
- [x] Resolved PyVis rendering error by switching to `net.write_html(..., open_browser=False)` and embedding HTML manually

Next tasks:

- [ ] Enrich rules: first-time buyer and veteran examples affecting steps
- [ ] Add additional contexts and regulations for a second state (e.g., Texas)
- [ ] Improve ordering semantics (weights/priorities beyond BFS)
- [ ] Add "What changed?" comparison between two runs
- [ ] Add basic unit tests for parsing and traversal
- [ ] Optional: parameterize export filenames and include metadata header

UI/UX improvements:

- [x] Sidebar form with examples and single CTA
- [x] Context chips and tabs (Procedure, Graph, Details)
- [x] Graph legend and larger embed
- [x] Robust graph rendering using Streamlit Graphviz instead of PyVis for reliability

Docs integration:

- [x] Exported steps now link to per-step reference pages under `site_docs/reference/`
- [x] Auto-create missing reference stubs; added Reference section to MkDocs nav
- [x] Enriched reference stubs for known steps with sub-steps and purpose
- [x] Added inline reference preview in Streamlit under each step
- [x] Added per-step source mapping (`core/sources.py`) and render Sources section in MkDocs export and in-app Details tab

UX polish:

- [x] Introduced card UI for steps with clear sections and spacing
- [x] Forced light theme via `.streamlit/config.toml`; updated copy to be business-friendly
- [ ] Typography and spacing tuning for tables (next)

Dummy data and input UX:

- [x] Added `core/dummy_data.py` and show per-step sample data in expanders
- [x] Moved input form to main content with larger text area and clearer layout
- [x] Enriched generic fallback dummy data with structured inputs/outputs, sub-steps, and mock API
- [x] Replaced raw JSON expander with card layout showing inputs, KPIs, outputs, sub-steps, and API snippet per step


