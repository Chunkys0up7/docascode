"""Document format transformation engine."""

import json
from typing import Any, Dict, Optional

import markdown
from bs4 import BeautifulSoup
from loguru import logger

from mcp_server.models.schemas import DocumentFormat


class DocumentTransformer:
    """Transform documents between different formats."""

    def __init__(self) -> None:
        """Initialize transformer with markdown processor."""
        self.md = markdown.Markdown(
            extensions=[
                "extra",
                "codehilite",
                "toc",
                "tables",
                "fenced_code",
                "nl2br",
            ]
        )

    def transform(
        self,
        content: str,
        source_format: DocumentFormat,
        target_format: DocumentFormat,
        options: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Transform document from source format to target format.

        Args:
            content: Document content
            source_format: Source format
            target_format: Target format
            options: Optional transformation options

        Returns:
            Transformed document content
        """
        options = options or {}

        if source_format == target_format:
            return content

        # Route to appropriate transformation method
        transform_key = f"{source_format.value}_to_{target_format.value}"
        transform_method = getattr(self, transform_key, None)

        if transform_method:
            logger.debug(f"Transforming {source_format.value} -> {target_format.value}")
            return transform_method(content, options)

        # Try intermediate conversion through markdown
        if source_format != DocumentFormat.MARKDOWN:
            intermediate = self.transform(content, source_format, DocumentFormat.MARKDOWN, options)
            return self.transform(intermediate, DocumentFormat.MARKDOWN, target_format, options)

        raise ValueError(
            f"Unsupported transformation: {source_format.value} -> {target_format.value}"
        )

    # Markdown transformations
    def markdown_to_html(self, content: str, options: Dict[str, Any]) -> str:
        """Convert Markdown to HTML."""
        self.md.reset()
        html = self.md.convert(content)

        if options.get("full_document", False):
            title = options.get("title", "Document")
            css = options.get("css", "")
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f4f4f4; }}
        {css}
    </style>
</head>
<body>
{html}
</body>
</html>"""
        return html

    def markdown_to_text(self, content: str, options: Dict[str, Any]) -> str:
        """Convert Markdown to plain text."""
        # First convert to HTML, then extract text
        html = self.markdown_to_html(content, {})
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n", strip=True)

    def markdown_to_json(self, content: str, options: Dict[str, Any]) -> str:
        """Convert Markdown to JSON structure."""
        lines = content.split("\n")
        sections = []
        current_section = {"type": "content", "content": []}

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#"):
                # Save previous section
                if current_section["content"]:
                    sections.append(current_section)

                # Start new section
                level = len(stripped) - len(stripped.lstrip("#"))
                title = stripped.lstrip("#").strip()
                current_section = {"type": "heading", "level": level, "title": title, "content": []}
            else:
                current_section["content"].append(line)

        # Save last section
        if current_section["content"]:
            current_section["content"] = "\n".join(current_section["content"]).strip()
            sections.append(current_section)

        result = {"format": "markdown", "sections": sections}
        return json.dumps(result, indent=2)

    # HTML transformations
    def html_to_markdown(self, content: str, options: Dict[str, Any]) -> str:
        """Convert HTML to Markdown (basic conversion)."""
        soup = BeautifulSoup(content, "html.parser")

        # Remove script and style tags
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Convert common tags
        for tag in soup.find_all("h1"):
            tag.replace_with(f"\n# {tag.get_text()}\n")
        for tag in soup.find_all("h2"):
            tag.replace_with(f"\n## {tag.get_text()}\n")
        for tag in soup.find_all("h3"):
            tag.replace_with(f"\n### {tag.get_text()}\n")
        for tag in soup.find_all("strong"):
            tag.replace_with(f"**{tag.get_text()}**")
        for tag in soup.find_all("em"):
            tag.replace_with(f"*{tag.get_text()}*")
        for tag in soup.find_all("code"):
            tag.replace_with(f"`{tag.get_text()}`")
        for tag in soup.find_all("a"):
            href = tag.get("href", "")
            text = tag.get_text()
            tag.replace_with(f"[{text}]({href})")

        # Convert lists
        for ul in soup.find_all("ul"):
            items = []
            for li in ul.find_all("li", recursive=False):
                items.append(f"- {li.get_text()}")
            ul.replace_with("\n" + "\n".join(items) + "\n")

        for ol in soup.find_all("ol"):
            items = []
            for idx, li in enumerate(ol.find_all("li", recursive=False), 1):
                items.append(f"{idx}. {li.get_text()}")
            ol.replace_with("\n" + "\n".join(items) + "\n")

        # Get remaining text
        text = soup.get_text()

        # Clean up extra whitespace
        lines = [line.rstrip() for line in text.split("\n")]
        # Remove excessive blank lines
        cleaned = []
        prev_blank = False
        for line in lines:
            if not line.strip():
                if not prev_blank:
                    cleaned.append("")
                prev_blank = True
            else:
                cleaned.append(line)
                prev_blank = False

        return "\n".join(cleaned).strip()

    def html_to_text(self, content: str, options: Dict[str, Any]) -> str:
        """Convert HTML to plain text."""
        soup = BeautifulSoup(content, "html.parser")
        return soup.get_text(separator="\n", strip=True)

    def html_to_json(self, content: str, options: Dict[str, Any]) -> str:
        """Convert HTML to JSON."""
        # Convert to markdown first, then to JSON
        markdown_content = self.html_to_markdown(content, options)
        return self.markdown_to_json(markdown_content, options)

    # Text transformations
    def text_to_markdown(self, content: str, options: Dict[str, Any]) -> str:
        """Convert plain text to Markdown (minimal formatting)."""
        # Add paragraph breaks
        lines = content.split("\n")
        paragraphs = []
        current = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                if current:
                    paragraphs.append(" ".join(current))
                    current = []
            else:
                current.append(stripped)

        if current:
            paragraphs.append(" ".join(current))

        return "\n\n".join(paragraphs)

    def text_to_html(self, content: str, options: Dict[str, Any]) -> str:
        """Convert plain text to HTML."""
        markdown_content = self.text_to_markdown(content, options)
        return self.markdown_to_html(markdown_content, options)

    def text_to_json(self, content: str, options: Dict[str, Any]) -> str:
        """Convert plain text to JSON."""
        lines = content.split("\n")
        result = {"format": "text", "lines": lines, "content": content}
        return json.dumps(result, indent=2)

    # JSON transformations
    def json_to_markdown(self, content: str, options: Dict[str, Any]) -> str:
        """Convert JSON to Markdown."""
        try:
            data = json.loads(content)

            # If it's our structured format
            if isinstance(data, dict) and "sections" in data:
                parts = []
                for section in data["sections"]:
                    if section.get("type") == "heading":
                        level = section.get("level", 1)
                        title = section.get("title", "")
                        parts.append(f"{'#' * level} {title}\n")
                    content_part = section.get("content", "")
                    if content_part:
                        parts.append(content_part + "\n")
                return "\n".join(parts).strip()

            # Otherwise, pretty print as code block
            return f"```json\n{json.dumps(data, indent=2)}\n```"

        except json.JSONDecodeError:
            return f"```json\n{content}\n```"

    def json_to_html(self, content: str, options: Dict[str, Any]) -> str:
        """Convert JSON to HTML."""
        markdown_content = self.json_to_markdown(content, options)
        return self.markdown_to_html(markdown_content, options)

    def json_to_text(self, content: str, options: Dict[str, Any]) -> str:
        """Convert JSON to plain text."""
        try:
            data = json.loads(content)
            return json.dumps(data, indent=2)
        except json.JSONDecodeError:
            return content

    # PDF and DOCX conversions (placeholders for optional dependencies)
    def markdown_to_pdf(self, content: str, options: Dict[str, Any]) -> str:
        """Convert Markdown to PDF (requires pypdf/reportlab)."""
        raise NotImplementedError("PDF generation requires optional 'pdf' dependencies")

    def pdf_to_markdown(self, content: str, options: Dict[str, Any]) -> str:
        """Convert PDF to Markdown (requires pypdf)."""
        raise NotImplementedError("PDF parsing requires optional 'pdf' dependencies")

    def markdown_to_docx(self, content: str, options: Dict[str, Any]) -> str:
        """Convert Markdown to DOCX (requires python-docx)."""
        raise NotImplementedError("DOCX generation requires optional 'docx' dependencies")

    def docx_to_markdown(self, content: str, options: Dict[str, Any]) -> str:
        """Convert DOCX to Markdown (requires python-docx)."""
        raise NotImplementedError("DOCX parsing requires optional 'docx' dependencies")
