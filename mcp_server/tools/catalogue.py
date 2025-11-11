"""Catalogue document tool - index documents for search."""

from datetime import datetime
from typing import Any, Dict, Optional

from loguru import logger

from mcp_server.core.indexer import DocumentIndexer
from mcp_server.models.schemas import DocumentFormat, DocumentMetadata


async def catalogue_document(
    content: str,
    title: str,
    format: str = "markdown",
    metadata: Optional[Dict[str, Any]] = None,
    collection: str = "documents",
) -> Dict[str, Any]:
    """Catalogue a document by indexing it with metadata and embeddings.

    Args:
        content: Document content to catalogue
        title: Document title
        format: Document format (markdown, html, json, text)
        metadata: Optional metadata dict (author, tags, description, etc.)
        collection: Collection name to add document to

    Returns:
        Dict with document ID and cataloguing metadata

    Example:
        ```python
        result = await catalogue_document(
            content="# My Document\\n\\nContent here.",
            title="My Document",
            format="markdown",
            metadata={"author": "John Doe", "tags": ["important", "draft"]}
        )
        ```
    """
    try:
        metadata = metadata or {}

        # Create document metadata
        doc_format = DocumentFormat(format.lower())
        doc_metadata = DocumentMetadata(
            title=title,
            format=doc_format,
            created_at=metadata.get("created_at", datetime.now()),
            updated_at=metadata.get("updated_at", datetime.now()),
            author=metadata.get("author"),
            tags=metadata.get("tags", []),
            description=metadata.get("description"),
            source_path=metadata.get("source_path"),
            word_count=len(content.split()),
            language=metadata.get("language", "en"),
            custom_fields=metadata.get("custom_fields", {}),
        )

        # Initialize indexer
        indexer = DocumentIndexer(collection_name=collection)

        # Add document
        doc_id = indexer.add_document(content, doc_metadata)

        logger.info(f"Catalogued document: {doc_id} ({title})")

        return {
            "success": True,
            "document_id": doc_id,
            "title": title,
            "format": format,
            "collection": collection,
            "word_count": doc_metadata.word_count,
            "embedding_generated": True,
        }

    except Exception as e:
        logger.error(f"Failed to catalogue document: {e}")
        return {
            "success": False,
            "error": str(e),
            "title": title,
        }
