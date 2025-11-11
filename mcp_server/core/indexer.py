"""Document indexing with vector search and metadata storage."""

import hashlib
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings
from loguru import logger
from sentence_transformers import SentenceTransformer

from mcp_server.config import settings
from mcp_server.models.schemas import Document, DocumentMetadata, SearchResult


class DocumentIndexer:
    """Index and search documents using vector embeddings and metadata."""

    def __init__(self, collection_name: str = "documents") -> None:
        """Initialize indexer with vector store and embedding model.

        Args:
            collection_name: Name of the collection to use
        """
        self.collection_name = collection_name

        # Initialize embedding model
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        self.embedding_dimension = self.embedding_model.get_sentence_embedding_dimension()

        # Initialize ChromaDB
        if settings.chromadb_path:
            settings.chromadb_path.mkdir(parents=True, exist_ok=True)
            self.client = chromadb.PersistentClient(
                path=str(settings.chromadb_path),
                settings=ChromaSettings(anonymized_telemetry=False),
            )
        else:
            self.client = chromadb.Client(
                settings=ChromaSettings(anonymized_telemetry=False)
            )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Document collection with embeddings"},
        )
        logger.info(f"Initialized collection: {collection_name}")

    def generate_document_id(self, content: str, metadata: DocumentMetadata) -> str:
        """Generate a unique document ID based on content and metadata."""
        # Create hash of content + key metadata
        hash_input = f"{content}:{metadata.title}:{metadata.created_at}"
        content_hash = hashlib.md5(hash_input.encode()).hexdigest()[:12]
        return f"doc-{content_hash}"

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding vector for text."""
        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def extract_snippets(self, content: str, query: str, max_length: int = 200) -> List[str]:
        """Extract relevant snippets from content based on query."""
        # Simple implementation: find sentences containing query terms
        query_terms = set(query.lower().split())
        sentences = content.split(". ")
        snippets = []

        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(term in sentence_lower for term in query_terms):
                # Trim to max length
                snippet = sentence[:max_length]
                if len(sentence) > max_length:
                    snippet += "..."
                snippets.append(snippet)

        return snippets[:3]  # Return top 3 snippets

    def add_document(self, content: str, metadata: DocumentMetadata) -> str:
        """Add a document to the index.

        Args:
            content: Document content
            metadata: Document metadata

        Returns:
            Document ID
        """
        # Generate document ID
        doc_id = self.generate_document_id(content, metadata)

        # Generate embedding
        logger.debug(f"Generating embedding for document: {metadata.title}")
        embedding = self.embed_text(content)

        # Prepare metadata for ChromaDB (must be flat dict with simple types)
        chroma_metadata = {
            "title": metadata.title,
            "format": metadata.format.value,
            "author": metadata.author or "unknown",
            "language": metadata.language,
            "created_at": metadata.created_at.isoformat(),
            "updated_at": metadata.updated_at.isoformat(),
            "word_count": metadata.word_count or 0,
            "tags": ",".join(metadata.tags) if metadata.tags else "",
            "description": metadata.description or "",
        }

        # Add to collection
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[chroma_metadata],
        )

        logger.info(f"Added document: {doc_id} ({metadata.title})")
        return doc_id

    def update_document(self, doc_id: str, content: str, metadata: DocumentMetadata) -> None:
        """Update an existing document.

        Args:
            doc_id: Document ID
            content: New content
            metadata: New metadata
        """
        # Update metadata timestamp
        metadata.updated_at = datetime.now()

        # Generate new embedding
        embedding = self.embed_text(content)

        # Prepare metadata
        chroma_metadata = {
            "title": metadata.title,
            "format": metadata.format.value,
            "author": metadata.author or "unknown",
            "language": metadata.language,
            "created_at": metadata.created_at.isoformat(),
            "updated_at": metadata.updated_at.isoformat(),
            "word_count": metadata.word_count or 0,
            "tags": ",".join(metadata.tags) if metadata.tags else "",
            "description": metadata.description or "",
        }

        # Update in collection
        self.collection.update(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[chroma_metadata],
        )

        logger.info(f"Updated document: {doc_id}")

    def delete_document(self, doc_id: str) -> None:
        """Delete a document from the index.

        Args:
            doc_id: Document ID
        """
        self.collection.delete(ids=[doc_id])
        logger.info(f"Deleted document: {doc_id}")

    def get_document(self, doc_id: str) -> Optional[Document]:
        """Retrieve a document by ID.

        Args:
            doc_id: Document ID

        Returns:
            Document or None if not found
        """
        results = self.collection.get(ids=[doc_id], include=["documents", "metadatas", "embeddings"])

        if not results["ids"]:
            return None

        metadata_dict = results["metadatas"][0]
        metadata = DocumentMetadata(
            title=metadata_dict["title"],
            format=metadata_dict["format"],
            created_at=datetime.fromisoformat(metadata_dict["created_at"]),
            updated_at=datetime.fromisoformat(metadata_dict["updated_at"]),
            author=metadata_dict.get("author"),
            tags=metadata_dict.get("tags", "").split(",") if metadata_dict.get("tags") else [],
            description=metadata_dict.get("description"),
            language=metadata_dict.get("language", "en"),
            word_count=metadata_dict.get("word_count"),
        )

        return Document(
            id=doc_id,
            content=results["documents"][0],
            metadata=metadata,
            embeddings=results["embeddings"][0] if results["embeddings"] else None,
        )

    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        min_score: float = 0.0,
    ) -> List[SearchResult]:
        """Search documents using semantic similarity.

        Args:
            query: Search query
            filters: Optional metadata filters
            limit: Maximum number of results
            min_score: Minimum similarity score (0-1)

        Returns:
            List of search results
        """
        # Generate query embedding
        query_embedding = self.embed_text(query)

        # Prepare where clause for metadata filtering
        where = None
        if filters:
            where = {}
            for key, value in filters.items():
                if key in ["title", "author", "format", "language"]:
                    where[key] = value
                elif key == "tags" and isinstance(value, list):
                    # For tags, check if any match (simplified)
                    where["tags"] = {"$contains": value[0]} if value else None

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        # Convert to SearchResult objects
        search_results = []
        for idx in range(len(results["ids"][0])):
            doc_id = results["ids"][0][idx]
            content = results["documents"][0][idx]
            metadata_dict = results["metadatas"][0][idx]
            distance = results["distances"][0][idx]

            # Convert distance to similarity score (cosine distance -> similarity)
            # ChromaDB uses L2 distance by default, convert to similarity
            similarity = 1.0 / (1.0 + distance)

            if similarity < min_score:
                continue

            # Create metadata object
            metadata = DocumentMetadata(
                title=metadata_dict["title"],
                format=metadata_dict["format"],
                created_at=datetime.fromisoformat(metadata_dict["created_at"]),
                updated_at=datetime.fromisoformat(metadata_dict["updated_at"]),
                author=metadata_dict.get("author"),
                tags=metadata_dict.get("tags", "").split(",") if metadata_dict.get("tags") else [],
                description=metadata_dict.get("description"),
                language=metadata_dict.get("language", "en"),
                word_count=metadata_dict.get("word_count"),
            )

            # Extract snippets
            snippets = self.extract_snippets(content, query)
            snippet = snippets[0] if snippets else content[:200] + "..."

            search_results.append(
                SearchResult(
                    document_id=doc_id,
                    title=metadata.title,
                    snippet=snippet,
                    score=similarity,
                    metadata=metadata,
                    highlights=snippets,
                )
            )

        logger.info(f"Search for '{query}' returned {len(search_results)} results")
        return search_results

    def get_statistics(self) -> Dict[str, Any]:
        """Get indexer statistics."""
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "total_documents": count,
            "embedding_model": settings.embedding_model,
            "embedding_dimension": self.embedding_dimension,
        }

    def clear(self) -> None:
        """Clear all documents from the collection."""
        # Delete and recreate collection
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "Document collection with embeddings"},
        )
        logger.warning(f"Cleared collection: {self.collection_name}")
