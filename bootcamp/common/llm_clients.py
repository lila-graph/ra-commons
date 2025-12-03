"""
LLM client wrappers for consistent interface across providers

Provides unified access to OpenAI and Anthropic models with:
- Consistent error handling
- Automatic retries
- Token counting
- Cost tracking
"""

from typing import Optional, Dict, Any, List
from enum import Enum

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings

from common.config import settings


class LLMProvider(str, Enum):
    """Supported LLM providers"""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class LLMModel(str, Enum):
    """Common LLM models"""

    # OpenAI
    GPT4_TURBO = "gpt-4-turbo-preview"
    GPT4 = "gpt-4"
    GPT35_TURBO = "gpt-3.5-turbo"

    # Anthropic
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"


def get_chat_model(
    provider: LLMProvider = LLMProvider.OPENAI,
    model: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: Optional[int] = None,
    streaming: bool = False,
    **kwargs: Any,
) -> BaseChatModel:
    """
    Get a configured chat model

    Args:
        provider: LLM provider (openai or anthropic)
        model: Specific model name (uses defaults if None)
        temperature: Sampling temperature (0.0 = deterministic)
        max_tokens: Maximum tokens in response
        streaming: Enable streaming responses
        **kwargs: Additional provider-specific arguments

    Returns:
        Configured chat model

    Examples:
        >>> # Get default OpenAI model
        >>> llm = get_chat_model()

        >>> # Get specific Anthropic model
        >>> llm = get_chat_model(
        ...     provider=LLMProvider.ANTHROPIC,
        ...     model=LLMModel.CLAUDE_3_SONNET
        ... )

        >>> # Use for generation
        >>> response = llm.invoke("What is RAG?")
    """
    if provider == LLMProvider.OPENAI:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")

        return ChatOpenAI(
            model=model or LLMModel.GPT4_TURBO.value,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=streaming,
            api_key=settings.openai_api_key,
            organization=settings.openai_org_id,
            **kwargs,
        )

    elif provider == LLMProvider.ANTHROPIC:
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")

        return ChatAnthropic(
            model=model or LLMModel.CLAUDE_3_SONNET.value,
            temperature=temperature,
            max_tokens=max_tokens or 4096,
            streaming=streaming,
            api_key=settings.anthropic_api_key,
            **kwargs,
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")


def get_embeddings(
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    **kwargs: Any,
) -> Embeddings:
    """
    Get configured embeddings model

    Args:
        model: Embedding model name
        dimensions: Output dimensions (for models that support it)
        **kwargs: Additional arguments

    Returns:
        Configured embeddings model

    Examples:
        >>> # Get default embeddings
        >>> embeddings = get_embeddings()

        >>> # Get smaller embeddings for faster processing
        >>> embeddings = get_embeddings(
        ...     model="text-embedding-3-small",
        ...     dimensions=512
        ... )

        >>> # Embed documents
        >>> vectors = embeddings.embed_documents(["Hello", "World"])
    """
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")

    return OpenAIEmbeddings(
        model=model,
        dimensions=dimensions,
        api_key=settings.openai_api_key,
        **kwargs,
    )


def get_test_llm() -> BaseChatModel:
    """
    Get a fast, cheap LLM for testing

    Uses GPT-3.5-turbo by default for cost-effective testing.

    Returns:
        Configured test model
    """
    return get_chat_model(
        provider=LLMProvider.OPENAI,
        model=settings.test_llm_model,
        temperature=0.0,
    )


class TokenCounter:
    """Track token usage across multiple calls"""

    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.calls = 0

    def add(self, response: Any) -> None:
        """Add token counts from a response"""
        if hasattr(response, "usage_metadata"):
            metadata = response.usage_metadata
            self.prompt_tokens += metadata.get("input_tokens", 0)
            self.completion_tokens += metadata.get("output_tokens", 0)
            self.total_tokens += metadata.get("total_tokens", 0)
            self.calls += 1

    def reset(self) -> None:
        """Reset counters"""
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.calls = 0

    def get_stats(self) -> Dict[str, int]:
        """Get current statistics"""
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "calls": self.calls,
            "avg_tokens_per_call": (
                self.total_tokens // self.calls if self.calls > 0 else 0
            ),
        }

    def __str__(self) -> str:
        stats = self.get_stats()
        return (
            f"Tokens: {stats['total_tokens']:,} "
            f"(prompt: {stats['prompt_tokens']:,}, "
            f"completion: {stats['completion_tokens']:,}) "
            f"across {stats['calls']} calls"
        )


def estimate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    model: str = "gpt-4-turbo-preview",
) -> float:
    """
    Estimate cost for token usage

    Args:
        prompt_tokens: Number of input tokens
        completion_tokens: Number of output tokens
        model: Model name

    Returns:
        Estimated cost in USD

    Note:
        Prices as of January 2025. Check OpenAI/Anthropic pricing for updates.
    """
    # Prices per 1M tokens (input / output)
    PRICES = {
        "gpt-4-turbo-preview": (10.0, 30.0),
        "gpt-4": (30.0, 60.0),
        "gpt-3.5-turbo": (0.5, 1.5),
        "claude-3-opus-20240229": (15.0, 75.0),
        "claude-3-sonnet-20240229": (3.0, 15.0),
        "claude-3-haiku-20240307": (0.25, 1.25),
    }

    if model not in PRICES:
        # Default to GPT-4 pricing if unknown
        input_price, output_price = PRICES["gpt-4"]
    else:
        input_price, output_price = PRICES[model]

    input_cost = (prompt_tokens / 1_000_000) * input_price
    output_cost = (completion_tokens / 1_000_000) * output_price

    return input_cost + output_cost


# Example usage
if __name__ == "__main__":
    # Test LLM initialization
    print("Testing LLM clients...")

    try:
        llm = get_chat_model()
        print(f"✅ OpenAI client initialized: {llm.model_name}")

        response = llm.invoke("What is RAG in one sentence?")
        print(f"Response: {response.content}")

    except Exception as e:
        print(f"❌ Error: {e}")

    try:
        embeddings = get_embeddings()
        print(f"✅ Embeddings initialized: {embeddings.model}")

        vectors = embeddings.embed_documents(["test"])
        print(f"Embedding dimensions: {len(vectors[0])}")

    except Exception as e:
        print(f"❌ Error: {e}")
