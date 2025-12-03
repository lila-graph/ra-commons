# AI Engineering Bootcamp - Instructor Guide

**Comprehensive teaching guide for delivering the bootcamp**

## Table of Contents

1. [Overview](#overview)
2. [Teaching Philosophy](#teaching-philosophy)
3. [Module-by-Module Guide](#module-by-module-guide)
4. [Common Student Struggles](#common-student-struggles)
5. [Assessment Rubrics](#assessment-rubrics)
6. [Office Hours FAQ](#office-hours-faq)
7. [Grading Guidelines](#grading-guidelines)

## Overview

### Bootcamp Structure

**Duration**: 4 weeks (can be compressed to 2 weeks intensive or extended to 8 weeks part-time)

**Format**: Hybrid (async content + sync sessions)
- **Async**: Students work through modules independently
- **Sync**: Weekly live sessions for Q&A, debugging, discussions

**Target Audience**: Software engineers with Python experience, new to AI engineering

**Prerequisites**:
- Python 3.11+
- Basic understanding of LLMs and embeddings
- Git and CLI comfort
- API usage experience

### Learning Outcomes

By end of bootcamp, students should be able to:

✅ Design and implement production-grade RAG systems
✅ Use LangGraph for complex multi-agent workflows
✅ Evaluate and debug AI systems systematically
✅ Deploy observable, maintainable AI applications
✅ Make data-driven decisions about architecture choices

## Teaching Philosophy

### Core Principles

**1. Executable Narratives > Slide Decks**

Don't lecture about concepts—let students discover them:

```python
# ❌ Don't: Lecture about LangGraph state management
"State in LangGraph is a typed dictionary that..."

# ✅ Do: Let them break it and understand why
"Run example_02_wrong_state.py. Why does it fail?
Now run example_03_right_state.py. What's different?"
```

**2. Failure-Driven Learning**

Intentionally introduce failures for pedagogical value:

```python
# examples/chunking_wrong_way.py
chunks = text.split("\n\n")  # Naive approach

# Students run this, get poor RAGAS scores
# Then you show the right way
```

**3. Evaluation Before and After Every Change**

Never make a change without measuring its impact:

```bash
# Always this workflow:
python evaluate.py  # Baseline: 0.78
# Make change
python evaluate.py  # New score: 0.82
# Discuss why it improved
```

**4. Mental Models Over Implementation Details**

Teach how to think, not just how to code:

- **LangGraph** = State machine (not just a chain library)
- **Chunking** = Information preservation trade-off
- **RAG** = Three-stage pipeline (retrieve, rank, generate)

## Module-by-Module Guide

### Module 00: Bootstrap

**Time**: 1-2 hours

**Learning Objectives**:
- Environment setup
- Tool familiarity
- API basics

**Teaching Tips**:

1. **Run setup validation together in live session**
   - Students often have environment issues
   - Catch them early before they compound

2. **Emphasize LangGraph != LangChain**
   - Many students confuse them
   - Show simple graph vs chain comparison

3. **Don't skip the examples**
   - Examples build intuition
   - Code reading is as important as writing

**Common Issues**:

| Problem | Solution |
|---------|----------|
| Docker not starting | Check ports, show `docker logs` |
| Import errors | Verify `uv sync` ran successfully |
| API keys not found | Check `.env` location and format |

**Assessment**: setup.py passes all checks

---

### Module 01: Ingestion

**Time**: 1 week

**Learning Objectives**:
- Bronze/Silver/Gold pattern
- Chunking strategies
- Metadata extraction
- Prefect orchestration

**Teaching Tips**:

1. **Make chunking visceral**
   - Show same document with 3 different strategies
   - Run RAGAS on each
   - Let students see the score differences

2. **Emphasize the "why" of Bronze/Silver/Gold**
   - Not just best practice cargo culting
   - Real benefit: reprocessability without re-downloading

3. **Connect to data engineering**
   - Many students have DE experience
   - This module is pure data engineering with AI flavor

**Live Session Activities**:

- **Activity 1: Chunking Competition**
  - Give students same document
  - Challenge: Get highest RAGAS score
  - Discuss winning strategies

- **Activity 2: Break the Pipeline**
  - Introduce corrupted file
  - See whose error handling catches it
  - Review good error handling patterns

**Common Struggles**:

- **Chunking by characters instead of tokens**
  - Show example where this fails
  - Demonstrate token counting

- **Ignoring metadata**
  - Show retrieval with/without metadata filtering
  - Dramatic quality difference

**Assessment Rubric**:

| Criteria | Weight | Excellent | Adequate | Needs Work |
|----------|--------|-----------|----------|------------|
| Pipeline completeness | 30% | All stages work | Bronze/Silver work | Only Bronze |
| Chunking strategy | 30% | Evaluated 3+ strategies | Evaluated 1-2 | No evaluation |
| Metadata extraction | 20% | Comprehensive metadata | Basic metadata | No metadata |
| Error handling | 20% | Robust with retries | Basic try/catch | No error handling |

---

### Module 03: LangGraph Basics

**Time**: 1 week

**Learning Objectives**:
- State machine mental model
- Typed state schemas
- Conditional routing
- Node design patterns

**Teaching Tips**:

1. **Draw diagrams first, code second**
   - Never write a graph without drawing it
   - Enforce this with students

2. **Use the "state = function input/output" analogy**
   - Helps students coming from functional programming

3. **Emphasize "when" vs "how"**
   - Edges define "when" to transition
   - Nodes define "how" to process
   - This separation is LangGraph's killer feature

**Live Session Activities**:

- **Activity 1: Design a State Machine**
  - Give scenario: "Multi-step approval workflow"
  - Students draw state machine
  - Discuss different designs

- **Activity 2: Debug a Broken Graph**
  - Provide graph with subtle bug
  - Students trace execution
  - Identify and fix issue

**Common Struggles**:

- **Returning full state instead of updates**
  ```python
  # ❌ Wrong
  def node(state):
      return state

  # ✅ Right
  def node(state):
      return {"new_field": value}
  ```

- **Tight coupling between nodes**
  - Students call nodes directly instead of using edges
  - Show why this breaks observability

**Mental Model Check**:

Ask students: *"When should you use LangGraph vs a simple chain?"*

Good answer: *"When you have conditional branching, retry logic, or need to inspect/modify state between steps."*

**Assessment Rubric**:

| Criteria | Weight | Excellent | Adequate | Needs Work |
|----------|--------|-----------|----------|------------|
| State design | 30% | Typed with reducers | Typed dictionary | Untyped dict |
| Node implementation | 30% | Pure functions | Some side effects | Tightly coupled |
| Routing logic | 25% | Conditional edges used | Only linear edges | Logic in nodes |
| Error handling | 15% | Graceful retries | Basic try/catch | No handling |

---

### Module 06: Evaluation

**Time**: 1 week

**Learning Objectives**:
- RAGAS metrics
- LangSmith tracing
- Regression testing
- Evaluation-driven development

**Teaching Tips**:

1. **Make metrics concrete**
   - Don't just show scores
   - Show examples of high vs low scores
   - Connect scores to user experience

2. **Teach debugging workflow**
   - Metric shows problem (what)
   - Trace shows cause (why)
   - This workflow is crucial

3. **Emphasize continuous evaluation**
   - Not one-time activity
   - Part of every change

**Live Session Activities**:

- **Activity 1: Debug with Traces**
  - Give failing test case
  - Students use LangSmith to identify issue
  - Compare findings

- **Activity 2: Evaluation-Driven Refactor**
  - Give baseline system with known score
  - Challenge: Improve specific metric
  - Must prove improvement with evaluation

**Common Struggles**:

- **Small test sets**
  - Students use 5 test cases
  - Emphasize need for 50+ for significance

- **Not using traces**
  - Students guess at issues
  - Enforce trace-based debugging

**Key Discussion Points**:

- **Q: What's a good faithfulness score?**
  - A: > 0.85 for production, but depends on use case
  - More important: trend over time

- **Q: How many test cases do we need?**
  - A: Minimum 30 for statistical significance, 100+ ideal
  - Cover diverse question types

**Assessment Rubric**:

| Criteria | Weight | Excellent | Adequate | Needs Work |
|----------|--------|-----------|----------|------------|
| Test set quality | 30% | 50+ diverse cases | 20-49 cases | < 20 cases |
| Metric interpretation | 25% | Correctly diagnoses issues | Understands scores | Misinterprets |
| LangSmith usage | 25% | Uses traces to debug | Views traces | Doesn't use traces |
| Regression suite | 20% | Automated in CI/CD | Manual tests | No tests |

---

### Module 08: Capstone

**Time**: 1-2 weeks

**Learning Objectives**:
- Integrate all prior modules
- Production-ready code
- System design
- Documentation

**Teaching Tips**:

1. **Emphasize milestones**
   - Students often try to build everything at once
   - Enforce working milestone by milestone

2. **Code reviews are crucial**
   - Review after each milestone
   - Catch issues early

3. **Encourage documentation as you go**
   - Not at the end
   - Part of each milestone

**Live Session Activities**:

- **Milestone Reviews** (15 min per student)
  - Student demos working milestone
  - Instructor asks probing questions
  - Peers provide feedback

- **Architecture Whiteboarding**
  - Students present system design
  - Class critiques design decisions
  - Discuss alternatives

**Assessment Rubric**: See [Grading Guidelines](#grading-guidelines)

## Common Student Struggles

### Technical Issues

**1. "My embeddings are giving weird results"**

Common causes:
- Using wrong embedding model
- Not normalizing vectors
- Mixing embedding models

Debug process:
```python
# Check embedding dimensions
print(len(embedding))  # Should be 1536 for text-embedding-3-small

# Check first few values
print(embedding[:5])  # Should be floats in [-1, 1]

# Check similarity
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

print(cosine_similarity(embed("hello"), embed("hello")))  # Should be ~1.0
```

**2. "LangGraph state isn't updating"**

Common causes:
- Returning full state instead of updates
- Modifying state in-place
- Not understanding reducers

Fix:
```python
# Show difference between:
def wrong(state):
    state["field"] = value
    return state

def right(state):
    return {"field": value}
```

**3. "RAGAS scores are very low"**

Common causes:
- Poor chunking
- Wrong retrieval strategy
- Missing ground truth
- Bad prompts

Systematic debugging:
1. Check context precision (retrieval quality)
2. Check faithfulness (hallucination)
3. Check relevancy (prompt quality)
4. Fix weakest link first

### Conceptual Confusion

**1. "When do I use LangGraph vs chains?"**

Decision tree:
```
Need conditional branching? → LangGraph
Need retry logic? → LangGraph
Need state inspection? → LangGraph
Simple linear flow? → Chain
```

**2. "What's the difference between vector and graph RAG?"**

Analogy:
- **Vector RAG** = Google search (find similar documents)
- **Graph RAG** = Wikipedia (traverse relationships)
- **Hybrid** = Both (best of both worlds)

**3. "How do I know if my chunks are good?"**

Answer: Measure them!
- Run RAGAS on different strategies
- Compare scores objectively
- Don't trust intuition

## Office Hours FAQ

### Module 01: Ingestion

**Q: "What chunk size should I use?"**

A: It depends! But here's a starting point:
- Short-form content (tweets, Q&A): 256 tokens
- Medium-form (blog posts, docs): 512 tokens
- Long-form (books, papers): 1024 tokens

More important: Evaluate and compare!

**Q: "Should I use fixed or semantic chunking?"**

A: Fixed is simpler and more predictable. Semantic respects document structure but variable sizes can be tricky. Try both, measure, decide.

### Module 03: LangGraph

**Q: "Can I call one node from another?"**

A: Technically yes, but **don't**! This breaks the graph abstraction. Use edges instead.

**Q: "How do I pass data between nodes?"**

A: Through state! That's the whole point.

```python
# Node 1 adds to state
def node1(state):
    return {"result": compute()}

# Node 2 uses it
def node2(state):
    return {"final": process(state["result"])}
```

### Module 06: Evaluation

**Q: "My faithfulness score is 0.6. Is that bad?"**

A: Yes. That means 40% of your answers aren't supported by context (hallucinations). For production, you want > 0.85.

**Q: "How many test cases do I need?"**

A: Minimum 30, ideally 100+. More importantly: diverse coverage (different question types, edge cases).

## Grading Guidelines

### Capstone Project (Module 08)

**Total Points: 100**

#### Code Quality (25 points)

- **Modularity** (8 pts): Well-organized, separated concerns
- **Documentation** (7 pts): Docstrings, comments, README
- **Type Hints** (5 pts): Proper type annotations
- **Style** (5 pts): Follows PEP 8, clean code

#### Functionality (30 points)

- **Core Features** (15 pts): All must-haves working
- **Edge Cases** (8 pts): Handles errors gracefully
- **User Experience** (7 pts): Clear outputs, good UX

#### Quality Metrics (25 points)

- **RAGAS Scores** (15 pts):
  - Faithfulness > 0.85: 6 pts
  - Relevancy > 0.80: 5 pts
  - Precision > 0.75: 4 pts

- **Test Coverage** (10 pts):
  - 30+ test cases: 5 pts
  - 95%+ success rate: 5 pts

#### Documentation & Presentation (10 points)

- **README Quality** (5 pts): Clear, comprehensive
- **Architecture Diagram** (3 pts): Clear system design
- **Demo** (2 pts): Effective 10-min presentation

#### Innovation (10 points)

- **Novel Improvements** (5 pts): Beyond requirements
- **Performance** (3 pts): Optimizations
- **Extra Features** (2 pts): Nice-to-haves implemented

### Grade Ranges

- **A (90-100)**: Production-ready, exceeds requirements
- **B (80-89)**: Solid implementation, meets all requirements
- **C (70-79)**: Basic functionality, some gaps
- **D (60-69)**: Incomplete or significant issues
- **F (<60)**: Does not meet minimum standards

## Tips for Instructors

### First Time Teaching This Bootcamp

1. **Do all exercises yourself first**
   - You'll find pain points students will hit
   - Prepare solutions and debugging tips

2. **Set up infrastructure early**
   - Docker issues compound
   - Have backup cloud instances ready

3. **Over-communicate timelines**
   - Students underestimate time needed
   - Build in buffer for each module

### Making It Your Own

This bootcamp is a framework, not a script. Customize:

- **Replace examples** with your domain (e.g., healthcare, finance)
- **Add modules** for your organization's needs
- **Adjust pacing** based on your students' experience

### Measuring Success

Track these metrics:

- **Module completion rate** (target: > 90%)
- **Capstone quality** (target: avg grade > 85)
- **Student satisfaction** (target: > 4.5/5)
- **Time to completion** (target: students finish on time)

### Continuous Improvement

After each cohort:

1. **Collect feedback** (surveys + interviews)
2. **Identify pain points** (where students struggled)
3. **Update materials** (clearer examples, better exercises)
4. **Share improvements** (contribute back to repo)

## Resources for Instructors

### Technical References

- [LangChain Docs](https://python.langchain.com/docs/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [RAGAS Docs](https://docs.ragas.io/)
- [Qdrant Docs](https://qdrant.tech/documentation/)

### Pedagogical Resources

- `examples/` - Working reference code
- `solutions/` - Exercise solutions
- `docs/faq.md` - Common questions
- `docs/debugging_playbook.md` - Issue resolution guide

### Community

- GitHub Discussions for student questions
- Slack/Discord for real-time help
- Monthly instructor sync meetings

---

**Questions about teaching this bootcamp?** Open an issue or discussion on GitHub.

**Teaching for the first time?** Join the instructor onboarding session (schedule TBD).

**Good luck and happy teaching!** 🎓
