"""Create document tool - generate documents from templates."""

from typing import Any, Dict, Optional

from loguru import logger

from mcp_server.core.graph_engine import GraphEngine
from mcp_server.core.templates import TemplateEngine
from mcp_server.models.schemas import DocumentFormat, KnowledgeGraph


async def create_document(
    template_name: str,
    context: Dict[str, Any],
    output_format: str = "markdown",
    graph_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create a document from a template with context and optional graph data.

    Args:
        template_name: Name of the template file to use
        context: Template context variables (dict)
        output_format: Output format (markdown, html, json, text)
        graph_data: Optional knowledge graph data as dict

    Returns:
        Dict with created document content and metadata

    Example:
        ```python
        result = await create_document(
            template_name="procedure.md.j2",
            context={"title": "My Procedure", "steps": ["Step 1", "Step 2"]},
            output_format="markdown"
        )
        ```
    """
    try:
        # Initialize template engine
        template_engine = TemplateEngine()

        # Initialize graph if provided
        graph = None
        if graph_data:
            kg = KnowledgeGraph(**graph_data)
            graph = GraphEngine()
            graph.load_from_model(kg)
            logger.info(f"Loaded graph with {len(kg.nodes)} nodes")

        # Render template
        content = template_engine.render_template(template_name, context, graph)

        # Convert format if needed
        doc_format = DocumentFormat(output_format.lower())
        if doc_format != DocumentFormat.MARKDOWN:
            from mcp_server.core.transformer import DocumentTransformer

            transformer = DocumentTransformer()
            content = transformer.transform(
                content, DocumentFormat.MARKDOWN, doc_format, {}
            )

        logger.info(f"Created document from template: {template_name}")

        return {
            "success": True,
            "content": content,
            "format": output_format,
            "template": template_name,
            "context_keys": list(context.keys()),
        }

    except Exception as e:
        logger.error(f"Failed to create document: {e}")
        return {
            "success": False,
            "error": str(e),
            "template": template_name,
        }
