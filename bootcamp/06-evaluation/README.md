# Module 06: Evaluation with RAGAS and LangSmith

**Make RAG quality measurable, not just feelable**

## Learning Objectives

By the end of this module, you will:

✅ Understand why evaluation is crucial for RAG systems
✅ Use RAGAS metrics to quantify retrieval and generation quality
✅ Build evaluation loops that run automatically
✅ Track experiments with LangSmith
✅ Create regression test suites to prevent quality degradation
✅ Debug RAG failures systematically with traces
✅ Set up continuous evaluation in production

## The Core Problem

**Without evaluation, you're flying blind:**

```python
# You make a change
chunks = chunk_text(document, size=1024)  # Was 512

# Does quality improve or degrade?
# ¯\_(ツ)_/¯

# You can't know without measurement!
```

**With evaluation:**

```python
# Baseline
baseline_score = evaluate(chunks_512)  # 0.78

# After change
new_score = evaluate(chunks_1024)  # 0.72

# ❌ Change degraded quality → revert
```

## RAGAS: Retrieval Augmented Generation Assessment

RAGAS provides metrics for both retrieval and generation:

### Retrieval Metrics

**1. Context Precision**
*Are the retrieved documents actually relevant?*

```python
from ragas.metrics import context_precision

# High precision = most retrieved docs are relevant
# Low precision = lots of irrelevant docs retrieved
```

**Why it matters:** Irrelevant context confuses the LLM and increases cost.

**2. Context Recall**
*Did we retrieve all relevant documents?*

```python
from ragas.metrics import context_recall

# High recall = we got all the relevant docs
# Low recall = we missed important information
```

**Why it matters:** Missing key context leads to incomplete answers.

### Generation Metrics

**3. Faithfulness**
*Is the answer grounded in the retrieved context?*

```python
from ragas.metrics import faithfulness

# High faithfulness = answer supported by context
# Low faithfulness = hallucination!
```

**Why it matters:** This is the hallucination detector!

**4. Answer Relevancy**
*Does the answer actually address the question?*

```python
from ragas.metrics import answer_relevancy

# High relevancy = directly answers the question
# Low relevancy = tangential or off-topic
```

**Why it matters:** Even factual answers can be irrelevant.

### End-to-End Metric

**5. Answer Correctness**
*Is the answer factually correct?*

```python
from ragas.metrics import answer_correctness

# Requires ground truth answers
# Measures semantic similarity to correct answer
```

## Complete Evaluation Example

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset

# Your RAG system
def rag_system(question: str) -> dict:
    docs = retriever.get_relevant_documents(question)
    answer = generator.generate(question, docs)

    return {
        "question": question,
        "answer": answer,
        "contexts": [doc.page_content for doc in docs],
    }

# Test questions
test_cases = [
    {
        "question": "How do I implement RAG?",
        "ground_truth": "Retrieve relevant docs, pass to LLM with prompt",
    },
    # ... more test cases
]

# Run your system
results = []
for test in test_cases:
    result = rag_system(test["question"])
    result["ground_truth"] = test["ground_truth"]
    results.append(result)

# Evaluate
dataset = Dataset.from_list(results)
evaluation = evaluate(
    dataset,
    metrics=[
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    ],
)

print(evaluation)
# {
#     'context_precision': 0.817,
#     'context_recall': 0.923,
#     'faithfulness': 0.891,
#     'answer_relevancy': 0.856,
# }
```

## Interpreting Scores

### Good Scores (Production-Ready)

| Metric | Good Score | Interpretation |
|--------|-----------|----------------|
| Context Precision | > 0.8 | Most retrieved docs relevant |
| Context Recall | > 0.85 | Capturing all important context |
| Faithfulness | > 0.9 | No hallucinations |
| Answer Relevancy | > 0.85 | Directly answers question |

### Warning Signs

| Metric | Score | Problem | Fix |
|--------|-------|---------|-----|
| Precision | < 0.6 | Too much noise | Improve retrieval, add reranking |
| Recall | < 0.7 | Missing context | Increase top_k, improve chunking |
| Faithfulness | < 0.8 | Hallucinating | Adjust prompt, add citation |
| Relevancy | < 0.7 | Off-topic answers | Improve prompt, add examples |

## LangSmith: Tracing and Debugging

LangSmith provides **observability** for your RAG system.

### Basic Setup

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "your-key"
os.environ["LANGSMITH_PROJECT"] = "rag-evaluation"

# That's it! Now all LangChain calls are traced
```

### What Gets Traced

- Every LLM call (prompt, response, tokens, latency)
- Every retrieval (query, results, scores)
- Every chain/graph step
- Errors and exceptions
- Custom metadata

### Debugging with Traces

**Scenario: Low faithfulness score**

1. Open LangSmith UI: https://smith.langchain.com
2. Find the failing test case
3. Inspect the trace:
   - What documents were retrieved?
   - What was the prompt sent to LLM?
   - What did the LLM generate?
4. Identify the issue:
   - ❌ Wrong documents retrieved → Fix retrieval
   - ❌ Documents are right but LLM hallucinates → Fix prompt
   - ❌ Documents are irrelevant → Fix chunking

### Comparing Experiments

```python
# Experiment 1: Baseline
os.environ["LANGSMITH_PROJECT"] = "rag-baseline"
baseline_score = run_evaluation()

# Experiment 2: Larger chunks
os.environ["LANGSMITH_PROJECT"] = "rag-large-chunks"
chunk_size = 1024  # Was 512
large_chunks_score = run_evaluation()

# Compare in LangSmith UI
# See which performed better and why
```

## Building a Regression Test Suite

Prevent quality degradation over time:

```python
# tests/test_rag_quality.py
import pytest
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

# Golden test set (manually curated)
GOLDEN_TEST_SET = [
    {
        "question": "What is RAG?",
        "ground_truth": "Retrieval Augmented Generation...",
    },
    # ... 50+ carefully selected test cases
]

# Minimum acceptable scores
MIN_FAITHFULNESS = 0.85
MIN_RELEVANCY = 0.80

def test_rag_quality_does_not_degrade():
    """Ensure RAG quality meets minimum thresholds"""
    results = run_rag_on_test_set(GOLDEN_TEST_SET)

    evaluation = evaluate(
        results,
        metrics=[faithfulness, answer_relevancy],
    )

    assert evaluation["faithfulness"] >= MIN_FAITHFULNESS, \
        f"Faithfulness {evaluation['faithfulness']} below threshold"

    assert evaluation["answer_relevancy"] >= MIN_RELEVANCY, \
        f"Relevancy {evaluation['answer_relevancy']} below threshold"

# Run in CI/CD
# pytest tests/test_rag_quality.py
```

## Evaluation-Driven Development Workflow

**1. Establish Baseline**
```bash
python evaluate.py --config baseline.yaml
# Faithfulness: 0.82, Relevancy: 0.79
```

**2. Make Change**
```python
# Try different chunking strategy
chunk_size = 1024  # Was 512
```

**3. Re-evaluate**
```bash
python evaluate.py --config new_chunking.yaml
# Faithfulness: 0.78, Relevancy: 0.81
```

**4. Decide**
```
Faithfulness decreased (0.82 → 0.78) ❌
Relevancy increased (0.79 → 0.81) ✅

Overall: Net negative → REJECT change
```

**5. Iterate**
```python
# Try different approach
chunk_size = 512  # Keep original
overlap = 100  # Increase overlap (was 50)
```

**6. Re-evaluate**
```bash
python evaluate.py --config more_overlap.yaml
# Faithfulness: 0.85, Relevancy: 0.82
```

**7. Accept**
```
Both improved → ACCEPT change ✅
```

## Creating Good Test Cases

**Characteristics of a good evaluation set:**

1. **Representative** - Covers real user queries
2. **Diverse** - Different question types
3. **Challenging** - Include edge cases
4. **Ground truth** - Manual answers or verified facts
5. **Stable** - Don't change frequently

**Example structure:**

```python
test_cases = [
    # Simple factual
    {
        "question": "What is the capital of France?",
        "ground_truth": "Paris",
        "category": "factual",
        "difficulty": "easy",
    },

    # Multi-hop reasoning
    {
        "question": "Who wrote the book that inspired Blade Runner?",
        "ground_truth": "Philip K. Dick",
        "category": "reasoning",
        "difficulty": "medium",
    },

    # Temporal
    {
        "question": "What new features were added last month?",
        "ground_truth": "OAuth 2.0 support and rate limiting",
        "category": "temporal",
        "difficulty": "hard",
    },

    # Negation
    {
        "question": "What authentication methods are NOT supported?",
        "ground_truth": "SAML and LDAP",
        "category": "negation",
        "difficulty": "hard",
    },
]
```

## Module Examples

### Example 1: Basic RAGAS Evaluation
`examples/01_basic_ragas.py`

Run RAGAS on a simple RAG system and understand each metric.

### Example 2: LangSmith Integration
`examples/02_langsmith_tracing.py`

Set up LangSmith tracing and explore the UI.

### Example 3: Comparing Chunking Strategies
`examples/03_compare_strategies.py`

Evaluate different chunking approaches quantitatively.

### Example 4: Regression Test Suite
`examples/04_regression_tests.py`

Build automated tests that catch quality degradation.

### Example 5: Continuous Evaluation
`examples/05_continuous_eval.py`

Set up evaluation that runs on every change.

## Exercises

### Exercise 1: Evaluate Your Pipeline

Take your Module 01 ingestion pipeline and Module 02 retriever:
1. Create a test set of 10 questions
2. Run RAGAS evaluation
3. Identify the weakest metric
4. Make improvements targeting that metric
5. Re-evaluate and measure improvement

### Exercise 2: Debug with LangSmith

Intentionally create a poorly-performing RAG system:
- Use wrong chunk size
- Retrieve too few documents
- Use a bad prompt

Then use LangSmith traces to identify each issue.

### Exercise 3: Build Regression Suite

Create a test suite with:
- 20+ test cases covering different question types
- Minimum thresholds for each metric
- Automated test that fails if quality drops

Run it in your CI/CD pipeline.

## Key Takeaways

1. **Measure everything** - Don't trust your intuition
2. **RAGAS provides the metrics** - Standardized, reproducible
3. **LangSmith provides the debugging** - See exactly what happened
4. **Regression tests prevent degradation** - Quality is fragile
5. **Evaluation-driven development** - Make data-driven decisions

## Common Mistakes

❌ **Evaluating only once** - Evaluation is continuous, not one-time
❌ **Small test sets** - Need 50+ cases for statistical significance
❌ **Only measuring generation** - Retrieval quality matters too
❌ **No baseline** - Can't measure improvement without baseline
❌ **Ignoring traces** - Metrics tell you *what*, traces tell you *why*
❌ **No regression tests** - Quality will degrade over time

## Success Criteria

Before moving to Module 07, you should:

✅ Be able to run RAGAS evaluation on any RAG system
✅ Interpret all RAGAS metrics correctly
✅ Use LangSmith to debug quality issues
✅ Build automated regression test suites
✅ Follow evaluation-driven development workflow

## Next Module

Once complete:

✅ Run all examples
✅ Complete exercises
✅ Set up LangSmith for your project
✅ Move to **Module 07: Observability** for production monitoring

---

**Remember:** If you can't measure it, you can't improve it.
