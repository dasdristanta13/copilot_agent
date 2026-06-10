"""Embedding provider abstraction."""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Abstract Base Class for generating text embeddings."""

    @abstractmethod
    async def embed_query(self, text: str) -> list[float]:
        """Generate embedding for a search query."""

    @abstractmethod
    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple document chunks."""


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI implementation of EmbeddingProvider."""

    def __init__(self, api_key: str, default_model: str = "text-embedding-3-small") -> None:
        self.api_key = api_key
        self.default_model = default_model

    async def embed_query(self, text: str) -> list[float]:
        """Generate embedding using OpenAI API."""
        # TODO: Phase 7 — Embed query with OpenAI API
        # Return a stub 1536-dimension vector
        return [0.0] * 1536

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings using OpenAI API."""
        # TODO: Phase 7 — Embed docs with OpenAI API
        return [[0.0] * 1536 for _ in texts]
