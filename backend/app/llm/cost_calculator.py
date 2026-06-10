"""Token counting and cost estimation utilities."""



# Hardcoded model pricing per 1M tokens (input, output) in USD
# Ref: §10.3 of the blueprint
MODEL_RATES = {
    "gpt-4o-mini": {"input": 0.150, "output": 0.600},
    "gpt-4o": {"input": 2.500, "output": 10.000},
    "text-embedding-3-small": {"input": 0.020, "output": 0.000},
}


def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """Estimate token count for a text using tiktoken or simple fallback."""
    # TODO: Phase 10 — Implement tiktoken counting
    # Fallback/estimate: roughly 4 characters per token
    return len(text) // 4


def calculate_execution_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int = 0,
) -> float:
    """Calculate USD cost for LLM usage based on prompt and completion tokens."""
    rates = MODEL_RATES.get(model, MODEL_RATES["gpt-4o-mini"])
    input_cost = (prompt_tokens / 1_000_000) * rates["input"]
    output_cost = (completion_tokens / 1_000_000) * rates["output"]
    return float(input_cost + output_cost)
