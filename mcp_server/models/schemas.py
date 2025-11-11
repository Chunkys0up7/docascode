"""Pydantic schemas for documents, graphs, and operations."""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DocumentFormat(str, Enum):
    """Supported document formats."""

    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"
    TEXT = "text"
    PDF = "pdf"
    DOCX = "docx"


class NodeType(str, Enum):
    """Knowledge graph node types."""

    PROCESS = "process"
    SYSTEM = "system"
    ROLE = "role"
    REGULATION = "regulation"
    CONTEXT = "context"
    DOCUMENT = "document"
    ENTITY = "entity"
    CONCEPT = "concept"


class EdgeRelation(str, Enum):
    """Knowledge graph edge relations."""

    REQUIRES = "requires"
    PERFORMED_BY = "performed_by"
    APPLIES_TO = "applies_to"
    CONDITIONAL_ON = "conditional_on"
    PRECEDES = "precedes"
    REFERENCES = "references"
    RELATED_TO = "related_to"
    CONTAINS = "contains"


class DocumentMetadata(BaseModel):
    """Document metadata for cataloguing."""

    title: str
    format: DocumentFormat
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    author: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    source_path: Optional[str] = None
    word_count: Optional[int] = None
    language: str = "en"
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class Document(BaseModel):
    """Document model with content and metadata."""

    id: str
    content: str
    metadata: DocumentMetadata
    embeddings: Optional[List[float]] = None


class GraphNode(BaseModel):
    """Knowledge graph node."""

    id: str
    label: str
    type: NodeType
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """Knowledge graph edge."""

    source: str
    target: str
    relation: EdgeRelation
    properties: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeGraph(BaseModel):
    """Complete knowledge graph structure."""

    nodes: List[GraphNode]
    edges: List[GraphEdge]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProcedureContext(BaseModel):
    """Context for procedure generation."""

    query: str
    filters: Dict[str, Any] = Field(default_factory=dict)
    start_node: Optional[str] = None
    max_depth: int = Field(default=10, ge=1, le=50)
    include_metadata: bool = True


class SearchResult(BaseModel):
    """Search result with relevance score."""

    document_id: str
    title: str
    snippet: str
    score: float
    metadata: DocumentMetadata
    highlights: List[str] = Field(default_factory=list)


class TransformRequest(BaseModel):
    """Document transformation request."""

    content: str
    source_format: DocumentFormat
    target_format: DocumentFormat
    options: Dict[str, Any] = Field(default_factory=dict)


class CatalogueRequest(BaseModel):
    """Document cataloguing request."""

    content: str
    format: DocumentFormat
    metadata: Optional[DocumentMetadata] = None
    extract_entities: bool = False


class CreateDocumentRequest(BaseModel):
    """Document creation request."""

    template_name: str
    context: Dict[str, Any] = Field(default_factory=dict)
    output_format: DocumentFormat = DocumentFormat.MARKDOWN
    graph_data: Optional[KnowledgeGraph] = None
