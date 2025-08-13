# Getting Started

Follow these steps to explore the POC:

1. Start the app: `python -m streamlit run app/streamlit_app.py`
2. Enter a request or select a borrower sample and click "Generate Procedure".
3. Click "Export to MkDocs" to write generated pages under `site_docs/`.
4. Start docs: `mkdocs serve -a 127.0.0.1:8000`
5. In the app, set "Docs site base URL" to `http://127.0.0.1:8000`.
6. Use "Open in Docs" links from the app or browse the site navigation.

Tip: Regenerate procedures with different contexts (location, property type) to see dynamic paths.
