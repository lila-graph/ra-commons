# Module 08: End-to-End Capstone Project

**Build a Production-Ready AI Agent for Developer Onboarding**

## Project Overview

You'll build a complete AI-powered onboarding assistant that helps new engineers understand:
- Codebase structure and architecture
- Development workflows and tools
- API documentation and usage
- Team conventions and best practices

This project integrates everything from Modules 00-07:
- ✅ Ingestion pipeline (Module 01)
- ✅ Hybrid retrieval (Module 02)
- ✅ LangGraph orchestration (Module 03)
- ✅ Tool integration (Module 04)
- ✅ Memory management (Module 05)
- ✅ RAGAS evaluation (Module 06)
- ✅ Observability (Module 07)

## Why This Project

This mirrors a **real interview question** and a **real production use case**:

Companies ask: *"How would you build an AI assistant for our internal documentation?"*

Your answer is this project.

## Requirements

### Functional Requirements

**Must Have (Core Features):**

1. **Question Answering**
   - Answer questions about codebase, APIs, workflows
   - Cite sources (file:line references)
   - Handle follow-up questions

2. **Multiple Retrieval Strategies**
   - Vector search (semantic)
   - BM25 search (keyword)
   - GraphRAG (relationship traversal)
   - Hybrid fusion of all three

3. **Tool Integration**
   - Code search (find function definitions)
   - File reading (view specific files)
   - Web search (external docs)

4. **Memory Management**
   - Remember conversation context
   - Build knowledge graph of relationships
   - Temporal awareness (what changed recently)

5. **Quality Assurance**
   - Validate answer quality before returning
   - Retry with refined query if quality low
   - Graceful fallbacks

**Should Have (Important):**

6. **Multi-Agent Routing**
   - Code agent (for code questions)
   - API agent (for API docs)
   - General agent (for workflows/culture)

7. **Evaluation Suite**
   - 30+ test cases covering question types
   - RAGAS metrics tracked
   - Regression tests in CI/CD

8. **Production Observability**
   - LangSmith tracing
   - Metrics dashboard
   - Error tracking

**Nice to Have (Bonus):**

9. **Personalization**
   - Remember user preferences
   - Adapt to expertise level

10. **Proactive Suggestions**
    - Recommend related docs
    - Suggest next steps

### Non-Functional Requirements

- **Response Time**: < 5 seconds for simple queries
- **Accuracy**: RAGAS faithfulness > 0.85
- **Reliability**: 99%+ success rate on test set
- **Scalability**: Handle 100+ concurrent users
- **Maintainability**: Modular, tested, documented

## Architecture

```
User Query
    ↓
[Classify Intent]
    ↓
┌───────────┬────────────┬──────────────┐
│           │            │              │
│  Code     │    API     │   General    │
│  Agent    │   Agent    │   Agent      │
│           │            │              │
└───────────┴────────────┴──────────────┘
    ↓
[Retrieve Documents]
    ├─ Vector Search (Qdrant)
    ├─ BM25 Search
    └─ Graph Traversal (Graphiti/Neo4j)
    ↓
[Rerank Results]
    ↓
[Generate Answer]
    ↓
[Validate Quality] ──no──> [Refine Query] ──┐
    │ yes                                   │
    ↓                                       │
[Update Memory] <──────────────────────────┘
    ↓
[Return Answer + Citations]
```

## Project Structure

```
08-end-to-end-project/
├── README.md                    # This file
├── requirements.txt             # Project-specific dependencies
│
├── scaffold/                    # Starting point for students
│   ├── main.py                  # Entry point
│   ├── config.yaml              # Configuration
│   ├── state_schema.py          # LangGraph state definition
│   ├── agents/                  # Agent definitions
│   │   ├── code_agent.py
│   │   ├── api_agent.py
│   │   └── general_agent.py
│   ├── tools/                   # Tool implementations
│   │   ├── code_search.py
│   │   ├── file_reader.py
│   │   └── web_search.py
│   ├── retrieval/               # Retrieval strategies
│   │   ├── vector_retriever.py
│   │   ├── bm25_retriever.py
│   │   └── graph_retriever.py
│   └── memory/                  # Memory management
│       └── graphiti_manager.py
│
├── evaluation/                  # Evaluation framework
│   ├── test_cases.json          # Golden test set
│   ├── run_evaluation.py        # Evaluation script
│   └── metrics_dashboard.py     # Visualize results
│
├── data/                        # Sample data
│   ├── codebase_docs/           # Sample code documentation
│   ├── api_specs/               # Sample API docs
│   └── onboarding_guides/       # Sample guides
│
├── tests/                       # Test suite
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   ├── test_agents.py
│   └── test_quality.py
│
└── solutions/                   # Reference implementation
    └── README.md                # Explanation of design decisions
```

## Implementation Milestones

### Milestone 1: Data Ingestion (Week 1)

**Tasks:**
- Set up Bronze/Silver/Gold pipeline
- Ingest sample codebase documentation
- Chunk with optimal strategy
- Store in Qdrant

**Deliverables:**
- Working ingestion pipeline
- 500+ chunks in vector DB
- Metadata properly extracted

**Validation:**
- Run: `python scripts/validate_milestone_1.py`
- All checks pass

### Milestone 2: Retrieval (Week 1)

**Tasks:**
- Implement vector search
- Implement BM25 search
- Implement hybrid fusion
- Add reranking

**Deliverables:**
- Three retrieval strategies working
- Comparison evaluation
- Reranking improves quality

**Validation:**
- Run: `python scripts/validate_milestone_2.py`
- Context precision > 0.75

### Milestone 3: Basic LangGraph Workflow (Week 2)

**Tasks:**
- Define state schema
- Implement retrieve → generate → validate nodes
- Add conditional routing
- Handle retries

**Deliverables:**
- Working LangGraph
- State transitions correct
- Retry logic works

**Validation:**
- Run: `python scripts/validate_milestone_3.py`
- Graph executes end-to-end

### Milestone 4: Tool Integration (Week 2)

**Tasks:**
- Implement code search tool
- Implement file reader tool
- Implement web search tool
- Add tool selection logic

**Deliverables:**
- Three tools working
- Correct tool selected for query type
- Tools integrate with LangGraph

**Validation:**
- Run: `python scripts/validate_milestone_4.py`
- Tools called correctly

### Milestone 5: Memory & Multi-Agent (Week 3)

**Tasks:**
- Set up Graphiti memory
- Implement conversation history
- Add multi-agent routing
- Build knowledge graph

**Deliverables:**
- Memory persists across sessions
- Three specialized agents
- Routing works correctly

**Validation:**
- Run: `python scripts/validate_milestone_5.py`
- Memory correctly maintained

### Milestone 6: Evaluation & Observability (Week 3)

**Tasks:**
- Create golden test set (30+ cases)
- Set up RAGAS evaluation
- Configure LangSmith tracing
- Build metrics dashboard

**Deliverables:**
- Comprehensive test suite
- RAGAS scores tracked
- LangSmith configured

**Validation:**
- Run: `python evaluation/run_evaluation.py`
- All metrics meet thresholds

### Milestone 7: Production Polish (Week 4)

**Tasks:**
- Add error handling
- Optimize performance
- Write documentation
- Deploy demo

**Deliverables:**
- Production-ready code
- < 5s response time
- Comprehensive README

**Validation:**
- Run: `make test-all`
- All tests pass
- Demo works

## Evaluation Criteria

Your project will be evaluated on:

### Code Quality (25%)
- Modular, well-organized code
- Type hints and docstrings
- Following best practices
- Clean git history

### Functionality (30%)
- All core features working
- Handles edge cases
- Graceful error handling
- Good UX

### Quality Metrics (25%)
- RAGAS faithfulness > 0.85
- RAGAS relevancy > 0.80
- Context precision > 0.75
- 95%+ success rate on test set

### Documentation (10%)
- Clear README
- API documentation
- Architecture diagrams
- Design decision explanations

### Innovation (10%)
- Novel improvements
- Creative solutions
- Performance optimizations
- Extra features

## Getting Started

### Step 1: Review Requirements

Read this README thoroughly. Understand what you're building and why.

### Step 2: Explore the Scaffold

```bash
cd scaffold/
python main.py --help
```

The scaffold provides:
- State schema template
- Agent stubs
- Tool interfaces
- Configuration structure

Your job: Fill in the implementation!

### Step 3: Set Up Your Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Set up infrastructure
make docker-up

# Verify setup
python scripts/check_setup.py
```

### Step 4: Ingest Sample Data

```bash
python scripts/ingest_sample_data.py

# Verify
python scripts/verify_ingestion.py
```

### Step 5: Start Building

Begin with Milestone 1 and work sequentially.

```bash
# Work on ingestion
cd scaffold/

# Implement pipeline
nano ingestion_pipeline.py

# Test
python tests/test_ingestion.py

# Validate milestone
python ../scripts/validate_milestone_1.py
```

## Tips for Success

### Start Simple

Build the simplest possible version first:
1. Single agent (no routing)
2. Vector search only (no hybrid)
3. No memory (stateless)
4. Basic validation

Then add complexity incrementally.

### Test Continuously

After every feature:
```bash
make test
python evaluation/run_evaluation.py
```

Don't wait until the end to test!

### Use the Modules

This project integrates Modules 01-07. Review them as needed:
- Module 01: Ingestion patterns
- Module 02: Retrieval strategies
- Module 03: LangGraph workflows
- Module 04: Tool integration
- Module 05: Memory management
- Module 06: Evaluation with RAGAS
- Module 07: Observability

### Track Your Progress

Update your learning journal after each milestone:
- What worked well?
- What was challenging?
- What would you do differently?
- What did you learn?

### Ask for Help

Stuck? Resources:
- Module examples and exercises
- Common utilities in `common/`
- Instructor office hours
- Peer discussions
- Solutions (only after trying!)

## Demo Requirements

For final presentation, prepare a 10-minute demo showing:

1. **Live Query Handling** (3 min)
   - Ask 3 diverse questions
   - Show retrieval, routing, generation
   - Highlight quality validation

2. **Observability** (2 min)
   - Show LangSmith traces
   - Explain a failure case
   - Show metrics dashboard

3. **Evaluation Results** (2 min)
   - Show RAGAS scores
   - Compare to baselines
   - Explain improvements made

4. **Architecture Overview** (2 min)
   - Show system diagram
   - Explain design decisions
   - Highlight innovations

5. **Q&A** (1 min)

## Success Metrics

A successful project will:

✅ Answer questions accurately (faithfulness > 0.85)
✅ Retrieve relevant context (precision > 0.75)
✅ Respond quickly (< 5 seconds)
✅ Handle errors gracefully (no crashes)
✅ Pass all regression tests (100%)
✅ Have clean, documented code
✅ Demonstrate mastery of all modules

## What Comes Next

After completing this project, you'll have:

- A portfolio piece for interviews
- Practical experience with production AI systems
- Understanding of the full RAG stack
- Ability to build similar systems independently

You can extend this project into:
- A SaaS product
- An open-source tool
- A research paper
- Your own startup

The skills you've learned apply to any LLM-powered application.

---

**Ready to build?** → Start with `scaffold/README.md`

**Questions?** → See `docs/faq.md` or ask in discussions

**Good luck!** 🚀
