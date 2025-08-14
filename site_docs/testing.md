## UI Test Steps

Follow these UI-only steps to validate the end-to-end demo. No terminal commands required.

### 1) Open the apps
- Open Streamlit UI: `http://localhost:8501`
- Open Docs site: `http://localhost:8000`

### 2) Configure Docs base URL
- In Streamlit, set “Docs site base URL” to `http://localhost:8000`.

### 3) Free Text flow
- In “Input Mode”, select “Free Text”.
- Choose the example “Underwrite home loan for a first-time buyer in New Mexico with rural property”.
- Click “Generate Procedure”.
- Verify:
  - Context shows: Location: New Mexico; Property: Rural; First-time buyer: Yes; Veteran: No.
  - Steps include “Check NM Mortgage Rule 12” and “Rural Property Appraisal”.
  - Each step card shows Metadata, Inputs, KPIs, Outputs, and Business Guidance.
  - “Show Sub-steps” and “Show Sample API Call” expanders display content.

### 4) Role filter
- Use “Filter by role” to select a role (e.g., Underwriter).
- Verify only steps matching that role remain visible.
- Clear the filter; all steps return.

### 5) Graph View
- Open the “Graph View” tab.
- Toggle “Relevant only” and verify only the generated path (plus immediate neighbors) is visible and highlighted.
- Toggle back to “Full graph”.

### 6) Details & Traceability
- Open the “Details & Traceability” tab.
- Verify the “Query Used” matches your submission.
- For each step, verify:
  - Metadata chips (Role, System, Location/Property) are present.
  - “Open in Docs / HTML / Reference Index” links appear after export (before export, a hint to export is shown).
  - “📄 View Reference (in-app)” shows the step content after export.
  - “Sources” list appears where available.

### 7) Export & Docs integration
- Go to the “Export” tab.
- (Optional) Enable “Auto-export after generation”.
- Click “Export to MkDocs”.
- After success, verify:
  - In Streamlit, step cards now show working “Open in Docs” links.
  - In Docs (`http://localhost:8000`), the “Reference” section contains the generated step pages.
  - In Docs, “Generated” lists a new procedure entry; open it and check links within the page.

### 8) Borrower Sample flow
- Switch “Input Mode” to “Borrower Sample”.
- Pick a borrower (e.g., the first entry), then “Generate Procedure”.
- Verify:
  - Context reflects the borrower’s Location and Property.
  - Steps reflect the context (e.g., Texas → “Check TX Mortgage Rule 7”; NM → “Check NM Mortgage Rule 12”; Rural → “Rural Property Appraisal”).
- Export again and confirm a new entry appears in Docs → “Generated”.

### 9) Docs base URL variations
- Change “Docs site base URL” to `http://localhost:8000/` (with trailing slash) and confirm links still work.
- Change it back to `http://localhost:8000`.

### 10) Re-run with Auto-export
- Enable “Auto-export after generation”.
- Submit a slightly different Free Text query (e.g., change Location to Texas).
- Verify export happens automatically and Docs → “Generated” shows the new entry.

### Expected outcomes summary
- Free Text: NM + Rural produces NM rule and Rural appraisal steps.
- Borrower Sample: Steps adapt to borrower Location/Property and flags.
- Filters/Graph: Role filter narrows steps; “Relevant only” focuses the graph.
- Export: Reference pages and a Generated entry appear in Docs; in-app reference is viewable.


