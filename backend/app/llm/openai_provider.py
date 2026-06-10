"""OpenAI LLM provider implementation."""

from collections.abc import AsyncIterator
from typing import Any

from app.llm.base import LLMChunk, LLMProvider, LLMResponse


class OpenAIProvider(LLMProvider):
    """OpenAI LLM Provider implementation using OpenAI Responses API."""

    def __init__(self, api_key: str, default_model: str = "gpt-4o-mini") -> None:
        self.api_key = api_key
        self.default_model = default_model

    async def generate(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        config: dict[str, Any] | None = None,
    ) -> LLMResponse:
        """Generate a response using OpenAI API."""
        # TODO: Phase 9/10 — Full integration with openai async client
        model = (config or {}).get("model", self.default_model)
        return LLMResponse(
            content="Stub response from OpenAIProvider",
            model_name=model,
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            cost=0.0001,
        )

    async def stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        config: dict[str, Any] | None = None,
    ) -> AsyncIterator[LLMChunk]:
        """Stream response chunks using OpenAI API."""
        # TODO: Phase 11 — Full integration with openai streaming API
        model = (config or {}).get("model", self.default_model)

        async def _stream_generator() -> AsyncIterator[LLMChunk]:
            yield LLMChunk(content_delta="Stub ", model_name=model)
            yield LLMChunk(content_delta="streamed ", model_name=model)
            yield LLMChunk(content_delta="response.", model_name=model)

        return _stream_generator()
