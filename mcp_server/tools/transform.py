"""Transform document tool - convert between formats."""

from typing import Any, Dict, Optional

from loguru import logger

from mcp_server.core.transformer import DocumentTransformer
from mcp_server.models.schemas import DocumentFormat


async def transform_document(
    content: str,
    source_format: str,
    target_format: str,
    options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Transform a document from one format to another.

    Supported formats: markdown, html, json, text (pdf, docx with optional deps)

    Args:
        content: Document content to transform
        source_format: Source format (markdown, html, json, text, pdf, docx)
        target_format: Target format (markdown, html, json, text, pdf, docx)
        options: Optional transformation options

    Returns:
        Dict with transformed content and metadata

    Example:
        ```python
        result = await transform_document(
            content="# Hello World\\n\\nThis is **bold**.",
            source_format="markdown",
            target_format="html",
            options={"full_document": True, "title": "My Document"}
        )
        ```
    """
    try:
        options = options or {}

        # Validate formats
        source = DocumentFormat(source_format.lower())
        target = DocumentFormat(target_format.lower())

        # Initialize transformer
        transformer = DocumentTransformer()

        # Transform
        transformed = transformer.transform(content, source, target, options)

        logger.info(f"Transformed document: {source.value} -> {target.value}")

        return {
            "success": True,
            "content": transformed,
            "source_format": source.value,
            "target_format": target.value,
            "options_used": options,
        }

    except NotImplementedError as e:
        logger.warning(f"Transformation not available: {e}")
        return {
            "success": False,
            "error": str(e),
            "source_format": source_format,
            "target_format": target_format,
        }
    except Exception as e:
        logger.error(f"Failed to transform document: {e}")
        return {
            "success": False,
            "error": str(e),
            "source_format": source_format,
            "target_format": target_format,
        }
