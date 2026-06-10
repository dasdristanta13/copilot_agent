"""Base classes and interfaces for LLM Providers."""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    """Standardized response from an LLM."""

    content: str
    raw_response: Any = Field(default=None)
    prompt_tokens: int = Field(default=0)
    completion_tokens: int = Field(default=0)
    total_tokens: int = Field(default=0)
    cost: float = Field(default=0.0)
    model_name: str
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)


class LLMChunk(BaseModel):
    """A streamed chunk from an LLM."""

    content_delta: str
    raw_chunk: Any = Field(default=None)
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    cost: float | None = None
    model_name: str
    tool_calls_delta: list[dict[str, Any]] = Field(default_factory=list)


class LLMProvider(ABC):
    """Abstract Base Class for LLM Providers."""

    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        config: dict[str, Any] | None = None,
    ) -> LLMResponse:
        """Generate a complete response from the LLM."""

    @abstractmethod
    async def stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        config: dict[str, Any] | None = None,
    ) -> AsyncIterator[LLMChunk]:
        """Stream response chunks from the LLM."""
