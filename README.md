## Dynamic Docs POC (Graph-Based Dynamic Procedures)

This proof-of-concept demonstrates a lightweight, end-to-end flow for graph-based, dynamic procedure generation using a simple stack:

- Python for core logic and sample data
- Streamlit for an interactive UI
- NetworkX for an in-memory knowledge graph
- PyVis for graph visualization
- MkDocs for static documentation export of generated procedures

### What it does

- Builds a small underwriting knowledge graph (processes, roles, systems, regulations, contexts)
- Parses a natural-language query or loads a sample borrower profile
- Traverses the graph to generate a context-aware procedure
- Visualizes the traversal
- Exports the generated steps to Markdown so it can appear in a MkDocs site

### Project structure

```
app/
  streamlit_app.py
core/
  __init__.py
  export_md.py
  graph_seed.py
  nlp.py
  procedure.py
  visualize.py
data/
  borrowers.csv
  regulations.csv
  systems.csv
site_docs/
  index.md
  generated/.gitkeep
mkdocs.yml
requirements.txt
```

### Quickstart

1) Create a virtual environment and install deps

```
python -m venv .venv
.venv/Scripts/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

2) Run the Streamlit app

```
streamlit run app/streamlit_app.py
```

3) Generate a procedure

- Enter a query like: "Underwrite home loan for a first-time buyer in New Mexico with rural property"; or select a borrower from the sample data.

4) Export to docs

- Click "Export to MkDocs" to write a Markdown file under `site_docs/generated/`.
- In another terminal, serve the docs:

```
mkdocs serve
```

Open the local server URL shown by MkDocs and navigate to Generated.

### Notes

- The PoC uses simple heuristics for parsing and traversal to stay lightweight. It is intentionally minimal but structured for extension (e.g., swap in spaCy/LLM parsing, or Neo4j in place of NetworkX).
- The repository already contains a `Docs/` folder with prior notes. MkDocs is configured to use `site_docs/` to avoid conflicts on Windows.


