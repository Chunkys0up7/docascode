"""Template engine for document generation."""

from pathlib import Path
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape
from loguru import logger

from mcp_server.config import settings
from mcp_server.core.graph_engine import GraphEngine
from mcp_server.models.schemas import NodeType


class TemplateEngine:
    """Jinja2-based template engine with graph-aware filters."""

    def __init__(self, templates_dir: Optional[Path] = None) -> None:
        """Initialize template engine.

        Args:
            templates_dir: Directory containing templates (defaults to settings)
        """
        self.templates_dir = templates_dir or settings.templates_dir
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Create Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self._register_filters()

        logger.info(f"Initialized template engine: {self.templates_dir}")

    def _register_filters(self) -> None:
        """Register custom Jinja2 filters."""

        @self.env.filter
        def slugify(text: str) -> str:
            """Convert text to slug format."""
            slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in str(text))
            while "--" in slug:
                slug = slug.replace("--", "-")
            return slug.strip("-")

        @self.env.filter
        def truncate_words(text: str, num_words: int = 50) -> str:
            """Truncate text to specified number of words."""
            words = str(text).split()
            if len(words) <= num_words:
                return text
            return " ".join(words[:num_words]) + "..."

        @self.env.filter
        def markdown_link(text: str, url: str) -> str:
            """Create a markdown link."""
            return f"[{text}]({url})"

        @self.env.filter
        def bullet_list(items: list) -> str:
            """Create a markdown bullet list."""
            return "\n".join(f"- {item}" for item in items)

        @self.env.filter
        def numbered_list(items: list) -> str:
            """Create a markdown numbered list."""
            return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, 1))

    def render_template(
        self,
        template_name: str,
        context: Dict[str, Any],
        graph: Optional[GraphEngine] = None,
    ) -> str:
        """Render a template with context and optional graph data.

        Args:
            template_name: Name of the template file
            context: Template context variables
            graph: Optional graph engine for graph-aware features

        Returns:
            Rendered template content
        """
        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            raise ValueError(f"Template not found: {template_name}")

        # Add graph helper functions to context if graph is provided
        if graph:
            context = self._add_graph_helpers(context, graph)

        # Render template
        rendered = template.render(**context)
        logger.debug(f"Rendered template: {template_name}")

        return rendered

    def _add_graph_helpers(
        self, context: Dict[str, Any], graph: GraphEngine
    ) -> Dict[str, Any]:
        """Add graph helper functions to template context."""

        def get_node(node_id: str) -> Optional[Dict[str, Any]]:
            """Get node data by ID."""
            node = graph.get_node(node_id)
            if node:
                return {
                    "id": node.id,
                    "label": node.label,
                    "type": node.type.value,
                    **node.properties,
                }
            return None

        def get_neighbors(node_id: str, relation: Optional[str] = None) -> list:
            """Get neighboring nodes."""
            from mcp_server.models.schemas import EdgeRelation

            rel = EdgeRelation(relation) if relation else None
            neighbor_ids = graph.get_neighbors(node_id, relation=rel)
            return [get_node(nid) for nid in neighbor_ids if get_node(nid)]

        def get_nodes_by_type(node_type: str) -> list:
            """Get all nodes of a specific type."""
            ntype = NodeType(node_type)
            nodes = graph.get_nodes_by_type(ntype)
            return [
                {"id": n.id, "label": n.label, "type": n.type.value, **n.properties}
                for n in nodes
            ]

        def find_path(start: str, end: str) -> Optional[list]:
            """Find path between two nodes."""
            path = graph.find_path(start, end)
            return [get_node(nid) for nid in path] if path else None

        # Add helpers to context
        context["graph"] = {
            "get_node": get_node,
            "get_neighbors": get_neighbors,
            "get_nodes_by_type": get_nodes_by_type,
            "find_path": find_path,
            "stats": graph.get_statistics(),
        }

        return context

    def list_templates(self) -> list[str]:
        """List all available templates."""
        templates = []
        for path in self.templates_dir.rglob("*"):
            if path.is_file() and not path.name.startswith("."):
                rel_path = path.relative_to(self.templates_dir)
                templates.append(str(rel_path))
        return sorted(templates)

    def create_template(self, template_name: str, content: str) -> Path:
        """Create a new template file.

        Args:
            template_name: Name of the template
            content: Template content

        Returns:
            Path to created template
        """
        template_path = self.templates_dir / template_name
        template_path.parent.mkdir(parents=True, exist_ok=True)

        with open(template_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Created template: {template_name}")
        return template_path

    def get_template_content(self, template_name: str) -> str:
        """Get raw template content.

        Args:
            template_name: Name of the template

        Returns:
            Template content
        """
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise ValueError(f"Template not found: {template_name}")

        return template_path.read_text(encoding="utf-8")
