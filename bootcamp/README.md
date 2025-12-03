# AI Engineering Bootcamp 2025

**Production-Ready Learning Platform for LangGraph, RAG, and Agentic Workflows**

## Philosophy: Learn by Building, Validate by Testing

This bootcamp teaches modern AI engineering through **progressive scaffolding**—each module builds on the last, adding complexity only when foundations are solid. Every concept is taught through executable code, evaluation loops, and real-world patterns.

## What You'll Build

By the end of this bootcamp, you'll have built a complete **AI Agent for Developer Onboarding** that includes:

- 📊 **Multi-stage ingestion pipeline** (Bronze → Silver → Gold with Prefect)
- 🔍 **Hybrid retrieval** (Vector + BM25 + GraphRAG with Qdrant)
- 🤖 **LangGraph orchestration** (State machines, branching, error recovery)
- 🧠 **Memory systems** (Graphiti temporal knowledge graphs)
- 🛠️ **Tool integration** (Search, code context, file operations)
- 📈 **Evaluation framework** (RAGAS + LangSmith)
- 👁️ **Observability** (Tracing, debugging, monitoring)

## The Learning Path: From Simple to Sophisticated

### Phase 1: Deterministic Foundations

**Module 00: Bootstrap** — Environment setup, dependencies, validation
**Module 01: Ingestion** — Data pipelines without the magic
**Module 02: Retrievers** — Vector search, hybrid search, chunking strategies

🎯 **Goal:** Build predictable, testable retrieval systems

### Phase 2: Controlled Orchestration

**Module 03: LangGraph Basics** — State machines, nodes, edges, policies
**Module 04: Agents & Tools** — Tool calling, error handling, routing

🎯 **Goal:** Understand orchestration patterns and when to use them

### Phase 3: Full Agentic Systems

**Module 05: Memory** — Graphiti temporal graphs, context management
**Module 06: Evaluation** — RAGAS metrics, LangSmith tracing, regression testing
**Module 07: Observability** — Debugging, monitoring, production patterns
**Module 08: End-to-End Project** — Complete onboarding assistant

🎯 **Goal:** Build production-grade agentic systems with observable behavior

## The RAG System Maturity Model

Every student progresses through these levels:

```
Level 0 — No RAG (baseline LLM)
   ↓
Level 1 — Basic vector retrieval (Qdrant + embeddings)
   ↓
Level 2 — Hybrid search (BM25 + vector)
   ↓
Level 3 — GraphRAG (knowledge graphs with Graphiti)
   ↓
Level 4 — Agentic RAG (tools + memory + routing)
   ↓
Level 5 — Multi-agent orchestration (LangGraph + evaluation)
```

Each module includes exercises to upgrade your system from one level to the next.

## Repository Structure

```
bootcamp/
├── 00-bootstrap/                    # Setup and prerequisites
│   ├── setup.py                     # Environment validation
│   ├── examples/                    # "Hello World" for each tool
│   └── exercises/                   # Pre-flight checks
│
├── 01-ingestion/                    # Data pipeline fundamentals
│   ├── prefect_flows/               # Bronze → Silver → Gold
│   ├── chunking/                    # Strategies and evaluation
│   ├── metadata/                    # Extraction and validation
│   └── exercises/                   # Build your own pipeline
│
├── 02-retrievers/                   # Search and retrieval
│   ├── qdrant_setup/                # Vector DB configuration
│   ├── hybrid_search/               # BM25 + vector fusion
│   ├── reranking/                   # Cross-encoder patterns
│   └── exercises/                   # Retrieval evaluation
│
├── 03-langgraph-basics/             # State machine fundamentals
│   ├── simple_graphs/               # 3-node examples
│   ├── branching/                   # Conditional routing
│   ├── state_management/            # Typed state patterns
│   └── exercises/                   # Build retrieval graphs
│
├── 04-agents-tools/                 # Tool calling and routing
│   ├── tool_definitions/            # Schema-driven tools
│   ├── routing_strategies/          # When to use which tool
│   ├── error_handling/              # Retries and fallbacks
│   └── exercises/                   # Build multi-tool agents
│
├── 05-memory/                       # Knowledge graphs and context
│   ├── graphiti_setup/              # Temporal graph memory
│   ├── neo4j_integration/           # Graph database patterns
│   ├── memory_strategies/           # When to use graph vs vector
│   └── exercises/                   # Add memory to agents
│
├── 06-evaluation/                   # Testing and metrics
│   ├── ragas_examples/              # Faithfulness, relevancy, etc.
│   ├── langsmith_traces/            # Debugging and regression
│   ├── test_suites/                 # Automated evaluation
│   └── exercises/                   # Build evaluation loops
│
├── 07-observability/                # Production monitoring
│   ├── tracing/                     # LangSmith + OpenTelemetry
│   ├── debugging/                   # Common failure patterns
│   ├── monitoring/                  # Metrics and alerts
│   └── exercises/                   # Debug intentional failures
│
├── 08-end-to-end-project/           # Capstone project
│   ├── scaffold/                    # Starting architecture
│   ├── requirements/                # Feature specifications
│   ├── evaluation/                  # Acceptance criteria
│   └── solutions/                   # Reference implementation
│
├── common/                          # Shared utilities
│   ├── llm_clients/                 # OpenAI, Anthropic, etc.
│   ├── evaluation/                  # Reusable metrics
│   ├── logging/                     # Structured logging
│   └── testing/                     # Test fixtures
│
└── docs/
    ├── pedagogy/                    # Teaching philosophy
    ├── instructor_guides/           # Module-by-module guidance
    ├── student_journal_template.md  # Reflection prompts
    └── debugging_playbook.md        # Common failure patterns
```

## How This Bootcamp Is Different

### 1. Executable Narratives, Not Slide Decks

Every lesson follows this pattern:
1. **Present a scenario**: "Build X for Y use case"
2. **Provide a scaffold**: Minimal working code
3. **Students extend**: Fill in ingestion, retrieval, orchestration, tools
4. **Validate immediately**: `make validate` or `uv run scripts/eval.py`

### 2. Evaluation-Driven Learning

Students don't "feel" if their RAG works—they **measure** it:
- After ingestion: metadata correctness
- After retrieval: precision/recall
- After orchestration: node timings + error paths
- After agents: hallucination risk + tool accuracy

### 3. Failure-Driven Intuition

Each module includes "Debugging the Wrong Way" exercises:
- Mis-embedded chunks
- Broken metadata
- Vector DB misconfigurations
- LangGraph loops
- Agent hallucinations

Teaching failure patterns builds senior-level intuition.

### 4. Modern Stack (2025)

- **Orchestration**: LangGraph (state machines, not chains)
- **Vector DB**: Qdrant (fast, Rust-based, hybrid search)
- **Memory**: Graphiti (temporal knowledge graphs)
- **Pipelines**: Prefect (durable execution, observability)
- **Evaluation**: RAGAS + LangSmith
- **Graph DB**: Neo4j or FalkorDB

### 5. Industry-Aligned Capstone

The final project mirrors real interview questions:
"Build an AI agent that helps onboard new engineers by answering questions about our codebase, tools, and processes."

This covers every competency employers care about in 2025.

## Prerequisites

### Required Knowledge
- Python 3.11+
- Basic understanding of LLMs and embeddings
- Git and command-line comfort
- API usage (REST, JSON)

### Recommended (But We'll Teach)
- Graph databases
- State machines
- Prefect/Airflow
- Evaluation frameworks

## Setup

```bash
# Clone and navigate
git clone <your-repo>
cd bootcamp

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .

# Validate environment
python 00-bootstrap/setup.py

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Running Modules

Each module has:
- **README.md**: Learning objectives and concepts
- **examples/**: Working reference code
- **exercises/**: Hands-on challenges
- **solutions/**: Reference solutions (try exercises first!)
- **Makefile** or **scripts/**: Validation and testing

```bash
# Navigate to a module
cd 01-ingestion

# Read the learning objectives
cat README.md

# Run examples
python examples/01_basic_pipeline.py

# Try exercises
python exercises/build_your_pipeline.py

# Validate your work
make validate
# or
uv run scripts/eval.py
```

## Learning Journal

After each module, update your `learning_journal.md`:

```markdown
## Module 03: LangGraph Basics

### What behavior changed?
- Switched from sequential chains to state machines

### Why?
- Needed conditional branching based on retrieval quality

### Where was the bottleneck?
- State serialization when using complex Python objects

### Next steps?
- Explore typed state with Pydantic models
```

This mirrors real engineering retrospectives and accelerates learning.

## Evaluation Philosophy

Every module ends with quantifiable metrics:

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

results = evaluate(
    dataset=test_set,
    metrics=[faithfulness(), answer_relevancy()],
    llm=client
)

print(f"Faithfulness: {results['faithfulness']:.3f}")
print(f"Relevancy: {results['answer_relevancy']:.3f}")
```

You'll learn to:
- Set baseline metrics (Level 0)
- Improve systematically (Levels 1-5)
- Detect regressions automatically
- Debug failures with traces

## Tools We'll Use

| Tool | Purpose | Module Introduced |
|------|---------|-------------------|
| **LangChain** | LLM framework basics | 00-bootstrap |
| **LangGraph** | State machine orchestration | 03-langgraph-basics |
| **Qdrant** | Vector database | 02-retrievers |
| **Prefect** | Pipeline orchestration | 01-ingestion |
| **Graphiti** | Temporal knowledge graphs | 05-memory |
| **Neo4j** | Graph database | 05-memory |
| **RAGAS** | RAG evaluation metrics | 06-evaluation |
| **LangSmith** | Tracing and debugging | 06-evaluation |
| **OpenTelemetry** | Distributed tracing | 07-observability |

## Instructor Resources

Each module includes:
- **instructor_guide.md**: Teaching notes, common mistakes, solutions
- **slide_deck.md**: Minimal framing (not lecture replacement)
- **discussion_prompts.md**: Socratic questions for live sessions
- **grading_rubric.md**: Clear evaluation criteria

See `docs/instructor_guides/` for complete teaching materials.

## Student Success Metrics

By the end, students should be able to:

✅ Explain when to use vector vs hybrid vs graph retrieval
✅ Design LangGraph state machines with typed state
✅ Implement tool-calling agents with error recovery
✅ Set up RAGAS evaluation loops
✅ Debug agent failures with LangSmith traces
✅ Build production-grade ingestion pipelines
✅ Use Graphiti for temporal memory
✅ Deploy observable, testable agentic systems

## Support and Community

- **Issues**: Report bugs or unclear materials via GitHub Issues
- **Discussions**: Ask questions and share learnings
- **Office Hours**: [Schedule TBD]
- **Slack/Discord**: [Link TBD]

## Contributing

Found a better way to teach a concept? Improved an exercise? Fixed a bug?

See `CONTRIBUTING.md` for guidelines on submitting improvements.

## License

[Your License Here]

---

**Built for builders. Optimized for how advanced engineers actually learn.**

*Start with Module 00: Bootstrap →*
