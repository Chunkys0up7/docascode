# Procedure Generation

We generate steps via graph traversal (BFS) with context rules:

1. Seed from top-level processes
2. Apply `conditional_on` filters (e.g., location, property_type)
3. Respect `precedes` to order steps
4. Annotate with role/system hints

Outputs are enriched with dummy business data and exported to Markdown.
