# Implementation Plan — From POC to Production

This plan operationalizes the document "MkDocs-Powered Development Plan: From POC to Production" for the Dynamic Docs POC you are using.

## Phase 0: Stabilize (Now)
- Default Graph View to "Relevant only"; ensure context filtering removes non‑relevant steps
- Keep export creating per-step reference pages and a refreshed reference index
- Persist Docs base URL; default `http://127.0.0.1:8000`

## Phase 1: POC Hardening (2–3 days)
- MkDocs Material theme + plugins: search, git-authors, revision-date, macros
- Add site metadata, repo links, improved navigation and search
- Streamlit: optional Auto-export after generation; copyable deep links to reference pages

## Phase 2: Conversion & Traceability (Week 1–2)
- `scripts/ingest.py` to convert PDFs/DOCs in `Docs/` → `site_docs/source/converted/*.md` with front matter
- Link steps to converted sources in the Sources section
- CI: build MkDocs and run link checks; deploy to Pages or preview

## Phase 3: MVP Features (Week 3–6)
- Expand contexts/regulations across multiple states; add role/system depth
- Streamlit filters (e.g., role-only view) and export bundle option
- Logging/metrics; cached ingestion

## Phase 4: Enhanced (Week 7–12)
- Material theme refinements, macros usage
- Optional Neo4j POC; externalize graph

## Phase 5: Production (Week 13–20)
- Containerized deployment, auth, monitoring, backups, content freshness policy

## Immediate Next Actions
- Install MkDocs plugins and switch theme to Material
- Add ingestion script scaffold
- Enrich graph with TX/veteran/urban contexts
- Enable Auto-export toggle and anchors in Details tab

> This plan evolves as we iterate — see `Docs/DEVLOG.md` for frequent updates.
