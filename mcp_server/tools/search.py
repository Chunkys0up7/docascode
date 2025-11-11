"""Search documents tool - semantic and keyword search."""

from typing import Any, Dict, List, Optional

from loguru import logger

from mcp_server.core.indexer import DocumentIndexer


async def search_documents(
    query: str,
    collection: str = "documents",
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 10,
    min_score: float = 0.0,
) -> Dict[str, Any]:
    """Search documents using semantic similarity.

    Args:
        query: Search query string
        collection: Collection name to search in
        filters: Optional metadata filters (e.g., {"author": "John", "format": "markdown"})
        limit: Maximum number of results to return
        min_score: Minimum similarity score (0.0-1.0)

    Returns:
        Dict with search results and metadata

    Example:
        ```python
        result = await search_documents(
            query="mortgage underwriting procedures",
            filters={"tags": ["compliance"]},
            limit=5,
            min_score=0.5
        )
        ```
    """
    try:
        filters = filters or {}

        # Initialize indexer
        indexer = DocumentIndexer(collection_name=collection)

        # Search
        results = indexer.search(query, filters=filters, limit=limit, min_score=min_score)

        # Convert to dict format
        results_list = []
        for result in results:
            results_list.append({
                "document_id": result.document_id,
                "title": result.title,
                "snippet": result.snippet,
                "score": round(result.score, 4),
                "highlights": result.highlights,
                "metadata": {
                    "author": result.metadata.author,
                    "format": result.metadata.format.value,
                    "tags": result.metadata.tags,
                    "created_at": result.metadata.created_at.isoformat(),
                    "word_count": result.metadata.word_count,
                },
            })

        logger.info(f"Search '{query}' returned {len(results_list)} results")

        return {
            "success": True,
            "query": query,
            "num_results": len(results_list),
            "results": results_list,
            "collection": collection,
            "filters_applied": filters,
        }

    except Exception as e:
        logger.error(f"Failed to search documents: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": query,
        }
