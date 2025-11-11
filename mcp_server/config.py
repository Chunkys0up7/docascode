"""Configuration management for DocAsCode MCP service."""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_prefix="DOCASCODE_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Paths
    data_dir: Path = Field(default=Path("data"), description="Base data directory")
    documents_dir: Path = Field(
        default=Path("data/documents"), description="Document storage directory"
    )
    graphs_dir: Path = Field(
        default=Path("data/graphs"), description="Knowledge graph storage directory"
    )
    indices_dir: Path = Field(
        default=Path("data/indices"), description="Search indices directory"
    )
    templates_dir: Path = Field(default=Path("templates"), description="Templates directory")

    # Vector Store
    vector_store_type: str = Field(default="chromadb", description="Vector store backend")
    chromadb_path: Optional[Path] = Field(
        default=Path("data/indices/chroma"), description="ChromaDB persistence path"
    )
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Sentence transformer model",
    )

    # Graph Database
    graph_backend: str = Field(
        default="networkx", description="Graph backend: networkx, neo4j, json"
    )
    neo4j_uri: Optional[str] = Field(default=None, description="Neo4j URI")
    neo4j_user: Optional[str] = Field(default=None, description="Neo4j username")
    neo4j_password: Optional[str] = Field(default=None, description="Neo4j password")

    # NLP
    spacy_model: str = Field(default="en_core_web_sm", description="spaCy model")
    enable_nlp: bool = Field(default=False, description="Enable NLP features")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[Path] = Field(default=None, description="Log file path")

    # Server
    server_name: str = Field(default="docascode-mcp", description="MCP server name")
    server_version: str = Field(default="0.1.0", description="Server version")

    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        for dir_path in [
            self.data_dir,
            self.documents_dir,
            self.graphs_dir,
            self.indices_dir,
            self.templates_dir,
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)

        if self.chromadb_path:
            self.chromadb_path.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
