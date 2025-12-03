#!/usr/bin/env python
"""
Example 01: Hello LLM

Demonstrates basic LLM usage with LangChain:
- Simple text generation
- Token counting
- Cost estimation
- Different models and parameters
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from common.llm_clients import get_chat_model, LLMProvider, TokenCounter, estimate_cost
from common.logging import get_logger, log_execution_time

logger = get_logger(__name__)


def example_basic_call():
    """Most basic LLM call"""
    print("\n" + "=" * 70)
    print("Example 1: Basic LLM Call")
    print("=" * 70)

    # Get a chat model (defaults to GPT-4 Turbo)
    llm = get_chat_model(temperature=0.0)

    # Simple invocation
    response = llm.invoke("What is RAG in one sentence?")

    print(f"\nPrompt: What is RAG in one sentence?")
    print(f"Response: {response.content}")
    print(f"Model: {llm.model_name}")


def example_with_parameters():
    """LLM with different parameters"""
    print("\n" + "=" * 70)
    print("Example 2: LLM with Custom Parameters")
    print("=" * 70)

    # More creative responses with higher temperature
    llm = get_chat_model(
        model="gpt-3.5-turbo",  # Faster, cheaper model
        temperature=0.7,  # More creative
        max_tokens=100,  # Limit response length
    )

    response = llm.invoke("Write a haiku about vector databases")

    print(f"\nModel: {llm.model_name}")
    print(f"Temperature: 0.7 (more creative)")
    print(f"Max tokens: 100")
    print(f"\nResponse:\n{response.content}")


def example_token_counting():
    """Track token usage across multiple calls"""
    print("\n" + "=" * 70)
    print("Example 3: Token Counting and Cost Estimation")
    print("=" * 70)

    llm = get_chat_model(model="gpt-3.5-turbo")
    counter = TokenCounter()

    prompts = [
        "What is an embedding?",
        "What is a vector database?",
        "What is semantic search?",
    ]

    print("\nMaking 3 API calls...\n")

    for prompt in prompts:
        response = llm.invoke(prompt)
        counter.add(response)

        print(f"Q: {prompt}")
        print(f"A: {response.content}\n")

    # Print statistics
    stats = counter.get_stats()
    cost = estimate_cost(
        stats["prompt_tokens"], stats["completion_tokens"], model=llm.model_name
    )

    print("\n" + "-" * 70)
    print("Token Usage Statistics:")
    print(f"  Total calls: {stats['calls']}")
    print(f"  Prompt tokens: {stats['prompt_tokens']:,}")
    print(f"  Completion tokens: {stats['completion_tokens']:,}")
    print(f"  Total tokens: {stats['total_tokens']:,}")
    print(f"  Avg tokens/call: {stats['avg_tokens_per_call']:,}")
    print(f"  Estimated cost: ${cost:.4f}")


def example_different_providers():
    """Compare OpenAI vs Anthropic"""
    print("\n" + "=" * 70)
    print("Example 4: Different Providers")
    print("=" * 70)

    prompt = "Explain LangGraph state machines in one sentence"

    # Try OpenAI
    try:
        with log_execution_time("OpenAI call"):
            openai_llm = get_chat_model(provider=LLMProvider.OPENAI, model="gpt-3.5-turbo")
            openai_response = openai_llm.invoke(prompt)

        print(f"\nOpenAI ({openai_llm.model_name}):")
        print(f"  {openai_response.content}")
    except Exception as e:
        print(f"\nOpenAI not available: {e}")

    # Try Anthropic
    try:
        with log_execution_time("Anthropic call"):
            anthropic_llm = get_chat_model(provider=LLMProvider.ANTHROPIC)
            anthropic_response = anthropic_llm.invoke(prompt)

        print(f"\nAnthropic ({anthropic_llm.model_name}):")
        print(f"  {anthropic_response.content}")
    except Exception as e:
        print(f"\nAnthropic not available: {e}")


def example_structured_prompts():
    """Using more structured prompts"""
    print("\n" + "=" * 70)
    print("Example 5: Structured Prompts")
    print("=" * 70)

    llm = get_chat_model(temperature=0.0)

    # Multi-line structured prompt
    prompt = """You are a technical instructor teaching AI engineering.

    Explain the following concept to a student who knows Python but is new to AI:
    - Concept: Vector embeddings
    - Format: Definition, analogy, example
    - Length: 2-3 sentences per section
    """

    response = llm.invoke(prompt)

    print("\nStructured prompt with role, task, and format:")
    print(f"\n{response.content}")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("HELLO LLM - Basic Language Model Usage")
    print("=" * 70)

    try:
        example_basic_call()
        example_with_parameters()
        example_token_counting()
        example_different_providers()
        example_structured_prompts()

        print("\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)
        print("\nKey Takeaways:")
        print("  1. get_chat_model() provides consistent LLM access")
        print("  2. Temperature controls creativity (0.0 = deterministic)")
        print("  3. Token counting helps track costs")
        print("  4. Different providers have different strengths")
        print("  5. Structured prompts → better outputs")
        print("\nNext: python examples/02_hello_embeddings.py")
        print()

    except Exception as e:
        logger.error(f"Example failed: {e}")
        print(f"\n❌ Error: {e}")
        print("Make sure you've set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
