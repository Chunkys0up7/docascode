"""Tests for document transformer."""

import pytest

from mcp_server.core.transformer import DocumentTransformer
from mcp_server.models.schemas import DocumentFormat


@pytest.fixture
def transformer():
    """Create transformer instance."""
    return DocumentTransformer()


def test_markdown_to_html(transformer):
    """Test markdown to HTML conversion."""
    markdown = "# Hello\n\nThis is **bold**."
    html = transformer.transform(markdown, DocumentFormat.MARKDOWN, DocumentFormat.HTML, {})

    assert "<h1>Hello</h1>" in html
    assert "<strong>bold</strong>" in html


def test_markdown_to_text(transformer):
    """Test markdown to text conversion."""
    markdown = "# Hello\n\nThis is **bold**."
    text = transformer.transform(markdown, DocumentFormat.MARKDOWN, DocumentFormat.TEXT, {})

    assert "Hello" in text
    assert "bold" in text
    assert "#" not in text


def test_html_to_markdown(transformer):
    """Test HTML to markdown conversion."""
    html = "<h1>Hello</h1><p>This is <strong>bold</strong>.</p>"
    markdown = transformer.transform(html, DocumentFormat.HTML, DocumentFormat.MARKDOWN, {})

    assert "# Hello" in markdown
    assert "**bold**" in markdown


def test_markdown_to_json(transformer):
    """Test markdown to JSON conversion."""
    markdown = "# Section 1\n\nContent here.\n\n## Section 2\n\nMore content."
    json_str = transformer.transform(markdown, DocumentFormat.MARKDOWN, DocumentFormat.JSON, {})

    assert "sections" in json_str
    assert "Section 1" in json_str


def test_same_format_passthrough(transformer):
    """Test that same format returns unchanged."""
    content = "# Hello"
    result = transformer.transform(content, DocumentFormat.MARKDOWN, DocumentFormat.MARKDOWN, {})
    assert result == content


def test_html_full_document(transformer):
    """Test full HTML document generation."""
    markdown = "# Hello World"
    html = transformer.transform(
        markdown,
        DocumentFormat.MARKDOWN,
        DocumentFormat.HTML,
        {"full_document": True, "title": "Test Doc"},
    )

    assert "<!DOCTYPE html>" in html
    assert "<title>Test Doc</title>" in html
    assert "</html>" in html
