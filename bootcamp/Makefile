.PHONY: help setup install install-dev clean test lint format validate-all docker-up docker-down

# Default target
help:
	@echo "AI Engineering Bootcamp - Available Commands"
	@echo "=============================================="
	@echo "Setup and Installation:"
	@echo "  make setup         - Complete first-time setup (env + install + docker)"
	@echo "  make install       - Install dependencies with uv"
	@echo "  make install-dev   - Install with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make format        - Format code with black and ruff"
	@echo "  make lint          - Run linters (ruff, mypy)"
	@echo "  make test          - Run all tests"
	@echo "  make clean         - Clean cache and temp files"
	@echo ""
	@echo "Infrastructure:"
	@echo "  make docker-up     - Start Qdrant + Neo4j + Prefect"
	@echo "  make docker-down   - Stop all services"
	@echo ""
	@echo "Validation:"
	@echo "  make validate-all  - Run environment validation"
	@echo "  make validate-module M=01  - Validate specific module"
	@echo ""
	@echo "Module Navigation:"
	@echo "  cd 00-bootstrap    - Start here!"
	@echo "  cd 01-ingestion    - Data pipelines"
	@echo "  cd 02-retrievers   - Vector search"
	@echo "  cd 03-langgraph-basics  - State machines"
	@echo "  cd 04-agents-tools - Tool calling"
	@echo "  cd 05-memory       - Knowledge graphs"
	@echo "  cd 06-evaluation   - RAGAS + LangSmith"
	@echo "  cd 07-observability - Tracing and debugging"
	@echo "  cd 08-end-to-end-project - Capstone"

# ============================================================================
# Setup and Installation
# ============================================================================

setup: install docker-up validate-all
	@echo "✅ Setup complete! Run 'cd 00-bootstrap' to start learning."

install:
	@echo "📦 Installing dependencies with uv..."
	uv sync
	@echo "✅ Dependencies installed"

install-dev:
	@echo "📦 Installing with dev dependencies..."
	uv sync --all-extras
	@echo "✅ Dev dependencies installed"

# ============================================================================
# Code Quality
# ============================================================================

format:
	@echo "🎨 Formatting code..."
	black .
	ruff check --fix .
	@echo "✅ Code formatted"

lint:
	@echo "🔍 Running linters..."
	ruff check .
	mypy common/
	@echo "✅ Linting complete"

test:
	@echo "🧪 Running tests..."
	pytest tests/ -v
	@echo "✅ Tests passed"

clean:
	@echo "🧹 Cleaning cache and temp files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .cache/
	@echo "✅ Cleaned"

# ============================================================================
# Docker Infrastructure
# ============================================================================

docker-up:
	@echo "🐳 Starting infrastructure services..."
	@docker compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 5
	@echo "✅ Services started:"
	@echo "   - Qdrant: http://localhost:6333"
	@echo "   - Neo4j: http://localhost:7474 (user: neo4j, password: bootcamp123)"
	@echo "   - Prefect: http://localhost:4200"

docker-down:
	@echo "🛑 Stopping infrastructure services..."
	@docker compose down
	@echo "✅ Services stopped"

docker-clean:
	@echo "🧹 Removing containers and volumes..."
	@docker compose down -v
	@echo "✅ Cleaned"

# ============================================================================
# Validation
# ============================================================================

validate-all:
	@echo "🔍 Validating environment setup..."
	python 00-bootstrap/setup.py
	@echo "✅ Environment validation complete"

validate-module:
	@if [ -z "$(M)" ]; then \
		echo "❌ Please specify module number: make validate-module M=01"; \
		exit 1; \
	fi
	@echo "🔍 Validating module $(M)..."
	@cd $(shell printf "%02d" $(M))-* && make validate 2>/dev/null || \
		(cd $(shell printf "%02d" $(M))-* && python scripts/eval.py)
	@echo "✅ Module $(M) validation complete"

# ============================================================================
# Learning Journey
# ============================================================================

journal:
	@echo "📝 Opening learning journal..."
	@mkdir -p logs
	@touch logs/learning_journal.md
	@${EDITOR:-vim} logs/learning_journal.md

start:
	@echo "🚀 Starting your AI Engineering journey!"
	@echo ""
	@echo "1. Make sure you've copied .env.example to .env and added your API keys"
	@echo "2. Run: make setup"
	@echo "3. Navigate to: cd 00-bootstrap"
	@echo "4. Read the README and run the examples"
	@echo ""
	@echo "Happy learning! 🎓"

# ============================================================================
# Quick Commands Per Module
# ============================================================================

module-00:
	@cd 00-bootstrap && python examples/01_hello_world.py

module-01:
	@cd 01-ingestion && python examples/01_basic_pipeline.py

module-02:
	@cd 02-retrievers && python examples/01_vector_search.py

module-03:
	@cd 03-langgraph-basics && python examples/01_simple_graph.py

module-04:
	@cd 04-agents-tools && python examples/01_basic_agent.py

module-05:
	@cd 05-memory && python examples/01_graphiti_intro.py

module-06:
	@cd 06-evaluation && python examples/01_ragas_basics.py

module-07:
	@cd 07-observability && python examples/01_tracing.py

module-08:
	@cd 08-end-to-end-project && python scaffold/main.py

# ============================================================================
# Instructor Tools
# ============================================================================

reset-student-env:
	@echo "🔄 Resetting to student starting state..."
	@git clean -fdx exercises/ || true
	@git checkout exercises/ || true
	@echo "✅ Student environment reset"

generate-solutions:
	@echo "📚 Generating solution guides..."
	@python scripts/generate_solutions.py
	@echo "✅ Solutions generated"
