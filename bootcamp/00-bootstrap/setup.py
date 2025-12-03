#!/usr/bin/env python
"""
Environment Setup Validation

Checks that all required dependencies, API keys, and services are properly configured.
Run this before starting the bootcamp to ensure smooth learning experience.
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple, Callable
import importlib

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class Colors:
    """ANSI color codes for terminal output"""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


def print_header(text: str) -> None:
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")


def print_result(test_name: str, passed: bool, message: str = "") -> None:
    """Print test result with color coding"""
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} | {test_name}")
    if message:
        indent = "         "
        print(f"{indent}{Colors.YELLOW}{message}{Colors.END}")


def run_checks(checks: List[Tuple[str, Callable]]) -> Tuple[int, int]:
    """
    Run a list of validation checks

    Args:
        checks: List of (check_name, check_function) tuples

    Returns:
        (passed_count, total_count)
    """
    passed = 0
    total = len(checks)

    for check_name, check_func in checks:
        try:
            success, message = check_func()
            print_result(check_name, success, message)
            if success:
                passed += 1
        except Exception as e:
            print_result(check_name, False, f"Error: {str(e)}")

    return passed, total


# ============================================================================
# Environment Checks
# ============================================================================


def check_python_version() -> Tuple[bool, str]:
    """Check Python version is 3.11+"""
    version = sys.version_info
    current = f"{version.major}.{version.minor}.{version.micro}"

    if version >= (3, 11):
        return True, f"Python {current}"
    return False, f"Python {current} (need >= 3.11)"


def check_package(package_name: str, import_name: str = None) -> Tuple[bool, str]:
    """Check if a package is installed and importable"""
    import_name = import_name or package_name

    try:
        module = importlib.import_module(import_name)
        version = getattr(module, "__version__", "unknown")
        return True, f"v{version}"
    except ImportError:
        return False, f"Not installed (run: uv sync)"


def check_langchain() -> Tuple[bool, str]:
    """Check LangChain installation"""
    return check_package("langchain")


def check_langgraph() -> Tuple[bool, str]:
    """Check LangGraph installation"""
    return check_package("langgraph")


def check_qdrant_client() -> Tuple[bool, str]:
    """Check Qdrant client installation"""
    return check_package("qdrant-client", "qdrant_client")


def check_neo4j() -> Tuple[bool, str]:
    """Check Neo4j driver installation"""
    return check_package("neo4j")


def check_prefect() -> Tuple[bool, str]:
    """Check Prefect installation"""
    return check_package("prefect")


def check_ragas() -> Tuple[bool, str]:
    """Check RAGAS installation"""
    return check_package("ragas")


# ============================================================================
# API Key Checks
# ============================================================================


def check_env_file() -> Tuple[bool, str]:
    """Check if .env file exists"""
    env_file = Path(__file__).parent.parent / ".env"

    if env_file.exists():
        return True, f"Found at {env_file}"
    return False, "Missing (copy .env.example to .env)"


def check_openai_api_key() -> Tuple[bool, str]:
    """Check OpenAI API key"""
    from common.config import settings

    if settings.openai_api_key:
        masked = f"{settings.openai_api_key[:8]}...{settings.openai_api_key[-4:]}"
        return True, f"Set ({masked})"
    return False, "Not set (add to .env)"


def check_anthropic_api_key() -> Tuple[bool, str]:
    """Check Anthropic API key"""
    from common.config import settings

    if settings.anthropic_api_key:
        masked = f"{settings.anthropic_api_key[:8]}...{settings.anthropic_api_key[-4:]}"
        return True, f"Set ({masked})"
    return False, "Not set (optional)"


def check_langsmith_api_key() -> Tuple[bool, str]:
    """Check LangSmith API key"""
    from common.config import settings

    if settings.langsmith_api_key:
        return True, f"Set (project: {settings.langsmith_project})"
    return False, "Not set (optional but recommended)"


def check_at_least_one_llm() -> Tuple[bool, str]:
    """Check that at least one LLM provider is configured"""
    from common.config import settings

    if settings.openai_api_key or settings.anthropic_api_key:
        providers = []
        if settings.openai_api_key:
            providers.append("OpenAI")
        if settings.anthropic_api_key:
            providers.append("Anthropic")
        return True, f"Configured: {', '.join(providers)}"
    return False, "Need at least OpenAI or Anthropic API key"


# ============================================================================
# Service Checks
# ============================================================================


def check_qdrant_connection() -> Tuple[bool, str]:
    """Check Qdrant service is accessible"""
    try:
        from qdrant_client import QdrantClient
        from common.config import settings

        config = settings.get_qdrant_config()
        client = QdrantClient(**config)

        # Try to get collections (should work even if empty)
        collections = client.get_collections()
        return True, f"Connected ({len(collections.collections)} collections)"
    except Exception as e:
        return False, f"Cannot connect (run: make docker-up) - {str(e)[:50]}"


def check_neo4j_connection() -> Tuple[bool, str]:
    """Check Neo4j service is accessible"""
    try:
        from neo4j import GraphDatabase
        from common.config import settings

        config = settings.get_neo4j_config()
        driver = GraphDatabase.driver(
            config["uri"], auth=(config["user"], config["password"])
        )

        # Try to execute a simple query
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            result.single()

        driver.close()
        return True, f"Connected to {config['uri']}"
    except Exception as e:
        return False, f"Cannot connect (run: make docker-up) - {str(e)[:50]}"


def check_prefect_server() -> Tuple[bool, str]:
    """Check Prefect server is accessible"""
    try:
        import httpx
        from common.config import settings

        response = httpx.get(
            f"{settings.prefect_api_url}/health",
            timeout=5.0,
        )

        if response.status_code == 200:
            return True, f"Server running at {settings.prefect_api_url}"
        return False, f"Server returned {response.status_code}"
    except Exception as e:
        return False, f"Cannot connect (run: make docker-up) - {str(e)[:50]}"


# ============================================================================
# Functionality Checks
# ============================================================================


def check_llm_api_call() -> Tuple[bool, str]:
    """Test actual LLM API call"""
    try:
        from common.llm_clients import get_chat_model, LLMProvider
        from common.config import settings

        # Use OpenAI if available, otherwise Anthropic
        if settings.openai_api_key:
            llm = get_chat_model(provider=LLMProvider.OPENAI, model="gpt-3.5-turbo")
        elif settings.anthropic_api_key:
            llm = get_chat_model(provider=LLMProvider.ANTHROPIC)
        else:
            return False, "No LLM API key configured"

        response = llm.invoke("Say 'Hello' in one word")
        return True, f"Response received ({len(response.content)} chars)"
    except Exception as e:
        return False, f"API call failed: {str(e)[:50]}"


def check_embeddings_generation() -> Tuple[bool, str]:
    """Test embedding generation"""
    try:
        from common.llm_clients import get_embeddings

        embeddings = get_embeddings()
        vectors = embeddings.embed_documents(["test document"])

        if vectors and len(vectors[0]) > 0:
            return True, f"Generated {len(vectors[0])}-dim vectors"
        return False, "Empty vectors generated"
    except Exception as e:
        return False, f"Embedding failed: {str(e)[:50]}"


def check_vector_storage() -> Tuple[bool, str]:
    """Test Qdrant vector storage and retrieval"""
    try:
        from qdrant_client import QdrantClient, models
        from common.config import settings
        from common.llm_clients import get_embeddings

        # Get clients
        config = settings.get_qdrant_config()
        qdrant = QdrantClient(**config)
        embeddings = get_embeddings()

        # Create test collection
        collection_name = "test_bootstrap"
        vector_size = 1536

        # Delete if exists
        try:
            qdrant.delete_collection(collection_name)
        except:
            pass

        # Create collection
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )

        # Add a test document
        test_doc = "AI Engineering Bootcamp"
        vector = embeddings.embed_query(test_doc)

        qdrant.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(id=1, vector=vector, payload={"text": test_doc})
            ],
        )

        # Search
        search_results = qdrant.search(
            collection_name=collection_name, query_vector=vector, limit=1
        )

        # Cleanup
        qdrant.delete_collection(collection_name)

        if search_results and search_results[0].score > 0.99:
            return True, "Storage and retrieval working"
        return False, "Search returned unexpected results"

    except Exception as e:
        return False, f"Vector storage failed: {str(e)[:50]}"


# ============================================================================
# Main Validation
# ============================================================================


def main():
    """Run all validation checks"""
    print_header("AI ENGINEERING BOOTCAMP - ENVIRONMENT VALIDATION")

    all_passed = 0
    all_total = 0

    # Python Environment Checks
    print_header("Python Environment")
    checks = [
        ("Python Version", check_python_version),
        ("LangChain", check_langchain),
        ("LangGraph", check_langgraph),
        ("Qdrant Client", check_qdrant_client),
        ("Neo4j Driver", check_neo4j),
        ("Prefect", check_prefect),
        ("RAGAS", check_ragas),
    ]
    passed, total = run_checks(checks)
    all_passed += passed
    all_total += total

    # API Key Checks
    print_header("API Keys & Configuration")
    checks = [
        (".env File", check_env_file),
        ("OpenAI API Key", check_openai_api_key),
        ("Anthropic API Key", check_anthropic_api_key),
        ("LangSmith API Key", check_langsmith_api_key),
        ("At Least One LLM", check_at_least_one_llm),
    ]
    passed, total = run_checks(checks)
    all_passed += passed
    all_total += total

    # Service Checks
    print_header("Infrastructure Services")
    checks = [
        ("Qdrant Vector DB", check_qdrant_connection),
        ("Neo4j Graph DB", check_neo4j_connection),
        ("Prefect Server", check_prefect_server),
    ]
    passed, total = run_checks(checks)
    all_passed += passed
    all_total += total

    # Functionality Checks
    print_header("Functionality Tests")
    checks = [
        ("LLM API Call", check_llm_api_call),
        ("Embeddings Generation", check_embeddings_generation),
        ("Vector Storage", check_vector_storage),
    ]
    passed, total = run_checks(checks)
    all_passed += passed
    all_total += total

    # Final Summary
    print_header("VALIDATION SUMMARY")
    percentage = (all_passed / all_total) * 100 if all_total > 0 else 0

    print(f"Passed: {all_passed}/{all_total} ({percentage:.1f}%)\n")

    if all_passed == all_total:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL CHECKS PASSED!{Colors.END}")
        print(
            f"{Colors.GREEN}Your environment is ready. Start learning with:"
            f"\n   cd 00-bootstrap && python examples/01_hello_llm.py{Colors.END}\n"
        )
        return 0
    else:
        failed = all_total - all_passed
        print(f"{Colors.RED}{Colors.BOLD}❌ {failed} CHECKS FAILED{Colors.END}")
        print(f"{Colors.YELLOW}Please fix the issues above and re-run this script.{Colors.END}")
        print(f"{Colors.YELLOW}See 00-bootstrap/README.md for troubleshooting.{Colors.END}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
