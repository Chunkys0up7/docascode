"""Tests for MCP tools."""

import pytest

from mcp_server.tools import transform_document


@pytest.mark.asyncio
async def test_transform_document():
    """Test transform_document tool."""
    result = await transform_document(
        content="# Hello\n\nThis is **bold**.",
        source_format="markdown",
        target_format="html",
    )

    assert result["success"] is True
    assert "html" in result["content"].lower()
    assert result["source_format"] == "markdown"
    assert result["target_format"] == "html"


@pytest.mark.asyncio
async def test_transform_document_invalid_format():
    """Test transform_document with invalid format."""
    with pytest.raises(ValueError):
        await transform_document(
            content="test", source_format="invalid", target_format="html"
        )
