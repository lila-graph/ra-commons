# Module 00: Bootstrap

**Welcome to the AI Engineering Bootcamp!**

This module ensures your environment is correctly set up and introduces you to the tools you'll use throughout the bootcamp.

## Learning Objectives

By the end of this module, you will:

✅ Have a working development environment with all required tools
✅ Understand how to run and validate code in each module
✅ Know the basic APIs for LangChain, LangGraph, Qdrant, and Prefect
✅ Be able to debug common setup issues
✅ Have validated your API keys and service connections

## Prerequisites

### Required Software

- **Python 3.11+**: `python --version`
- **Docker**: `docker --version` (for running infrastructure)
- **Git**: `git --version`
- **uv** (recommended): `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Required API Keys

You'll need at least one LLM provider:

- **OpenAI** (recommended): Get key at https://platform.openai.com/api-keys
- **Anthropic** (alternative): Get key at https://console.anthropic.com/

Optional but recommended:

- **LangSmith**: Get key at https://smith.langchain.com (free tier available)

## Setup Instructions

### 1. Environment Configuration

```bash
# From bootcamp root directory
cd bootcamp

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# At minimum, set OPENAI_API_KEY or ANTHROPIC_API_KEY
nano .env  # or use your preferred editor
```

### 2. Install Dependencies

```bash
# Using uv (recommended - faster)
uv sync

# Or using pip
pip install -e .
```

### 3. Start Infrastructure Services

```bash
# Start Qdrant, Neo4j, and Prefect using Docker
make docker-up

# Verify services are running
docker ps

# You should see:
# - qdrant (port 6333)
# - neo4j (ports 7474, 7687)
# - prefect-server (port 4200)
# - postgres (port 5432)
```

### 4. Validate Setup

```bash
# Navigate to bootstrap module
cd 00-bootstrap

# Run validation script
python setup.py

# You should see green checkmarks for all tests
```

## What Gets Validated

The `setup.py` script checks:

1. **Python Environment**
   - Python version >= 3.11
   - All required packages installed
   - Import tests for key libraries

2. **API Keys**
   - At least one LLM provider (OpenAI or Anthropic)
   - LangSmith (warning if missing, not required)

3. **Infrastructure Services**
   - Qdrant vector database connectivity
   - Neo4j graph database connectivity
   - Prefect server availability

4. **Basic Functionality**
   - LLM API calls work
   - Embedding generation works
   - Vector storage and retrieval works

## Examples

The `examples/` directory contains "Hello World" examples for each tool:

```bash
# Run examples sequentially
python examples/01_hello_llm.py
python examples/02_hello_embeddings.py
python examples/03_hello_qdrant.py
python examples/04_hello_neo4j.py
python examples/05_hello_prefect.py
python examples/06_hello_langgraph.py
```

Each example demonstrates:
- Basic API usage
- Common patterns you'll see throughout the bootcamp
- Expected output formats

## Exercises

Complete these exercises to ensure you understand the basics:

### Exercise 1: Environment Validation

Run `setup.py` and ensure all checks pass. If any fail:
1. Check the error message
2. Refer to troubleshooting section below
3. Fix the issue
4. Re-run validation

### Exercise 2: Modify LLM Example

Edit `exercises/exercise_01_llm.py`:
1. Try different models (GPT-4, GPT-3.5, Claude)
2. Experiment with temperature settings
3. Count tokens used
4. Estimate costs

### Exercise 3: Embed and Search

Edit `exercises/exercise_02_vector_search.py`:
1. Create embeddings for custom documents
2. Store them in Qdrant
3. Perform similarity search
4. Understand the results

### Exercise 4: Simple Graph

Edit `exercises/exercise_03_simple_graph.py`:
1. Create a 3-node LangGraph graph
2. Define state schema
3. Add conditional edges
4. Execute and observe state transitions

## Troubleshooting

### Python Version Issues

```bash
# Check your Python version
python --version

# If < 3.11, install a newer version
# On macOS with Homebrew:
brew install python@3.11

# On Linux:
sudo apt-get install python3.11
```

### API Key Not Found

```bash
# Verify .env file exists
ls -la .env

# Verify API key is set (don't print the actual key!)
grep OPENAI_API_KEY .env

# If empty, edit .env and add your key
nano .env
```

### Docker Services Not Starting

```bash
# Check if Docker is running
docker info

# Check if ports are already in use
lsof -i :6333  # Qdrant
lsof -i :7474  # Neo4j HTTP
lsof -i :7687  # Neo4j Bolt

# If ports are in use, stop existing services or use different ports

# View logs for specific service
docker logs bootcamp-qdrant
docker logs bootcamp-neo4j
docker logs bootcamp-prefect
```

### Import Errors

```bash
# Reinstall dependencies
uv sync --force

# Or with pip
pip install -e . --force-reinstall

# Verify installation
python -c "import langchain; import langgraph; import qdrant_client; print('OK')"
```

### Qdrant Connection Fails

```bash
# Check if Qdrant is running
curl http://localhost:6333/health

# Expected response: {"status":"ok"}

# If not running:
docker-compose up -d qdrant

# Check logs
docker logs bootcamp-qdrant
```

### Neo4j Connection Fails

```bash
# Check if Neo4j is running
curl http://localhost:7474

# Should see Neo4j browser page

# Try connecting with cypher-shell
docker exec -it bootcamp-neo4j cypher-shell -u neo4j -p bootcamp123

# Run a test query
RETURN "Hello Neo4j" as message;

# Exit with :exit
```

## Understanding the Tools

### LangChain vs LangGraph

- **LangChain**: Framework for building LLM applications
  - Provides components: prompts, chains, retrievers
  - Good for simple, linear workflows

- **LangGraph**: State machine orchestration (built on LangChain)
  - For complex, branching workflows
  - Explicit state management
  - Better for multi-agent systems

**When to use which?**
- Simple RAG query → LangChain
- Multi-step agent with tools → LangGraph
- Conditional routing based on output → LangGraph

### Qdrant vs Neo4j

- **Qdrant**: Vector database
  - Stores embeddings
  - Semantic similarity search
  - Fast retrieval (sub-millisecond)

- **Neo4j**: Graph database
  - Stores entities and relationships
  - Knowledge graph traversal
  - Structured queries with Cypher

**When to use which?**
- Semantic search → Qdrant
- Relationship queries → Neo4j
- GraphRAG → Both (vectors in Qdrant, graph in Neo4j)

### Prefect

- **Purpose**: Workflow orchestration
- **Why not just Python?**: Observability, retries, caching, scheduling
- **Use cases**: Data pipelines, batch processing, ETL

You'll use Prefect in Module 01 for ingestion pipelines.

## Key Concepts to Understand

### 1. Embeddings

Embeddings are dense vector representations of text:
```python
text = "AI is transforming software engineering"
embedding = [0.023, -0.145, 0.892, ...]  # 1536 dimensions

# Semantically similar texts have similar embeddings
# Measured by cosine similarity or euclidean distance
```

### 2. State Machines

LangGraph uses state machines for workflow control:
```
[Input] → [Process] → [Decision]
                          ↓
                    [Action A] or [Action B]
                          ↓
                      [Output]
```

State is preserved between nodes and can be inspected/modified.

### 3. Vector Search

Finding similar documents:
```
Query: "How do I deploy a model?"

1. Embed query → vector
2. Search vector DB for similar vectors
3. Return corresponding documents
4. Rank by relevance
```

## Success Criteria

Before moving to Module 01, you should:

✅ Have `setup.py` passing all checks
✅ Successfully run all examples
✅ Complete all exercises
✅ Understand the purpose of each tool
✅ Be able to debug common issues independently

## Next Steps

Once you've completed this module:

1. **Update your learning journal**
   ```bash
   nano ../logs/learning_journal.md
   ```

   Answer:
   - What was most confusing initially?
   - What clicked after the examples?
   - What questions do you still have?

2. **Move to Module 01: Ingestion**
   ```bash
   cd ../01-ingestion
   cat README.md
   ```

3. **Optional: Explore the tools**
   - Open Qdrant dashboard: http://localhost:6333/dashboard
   - Open Neo4j browser: http://localhost:7474
   - Open Prefect UI: http://localhost:4200

## Resources

### Official Documentation
- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [Neo4j Docs](https://neo4j.com/docs/)
- [Prefect Docs](https://docs.prefect.io/)

### Bootcamp-Specific
- `common/llm_clients.py` - LLM client wrappers
- `common/config.py` - Configuration management
- `common/logging.py` - Logging utilities

---

**Questions or stuck?** Check the troubleshooting section above or ask for help!

**Ready to continue?** → `cd ../01-ingestion`
