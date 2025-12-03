# Module 01: Data Ingestion Pipelines

**Learn to build production-grade data pipelines for RAG systems**

## Learning Objectives

By the end of this module, you will:

✅ Understand the Bronze/Silver/Gold data pipeline pattern
✅ Build ingestion pipelines with Prefect for observability
✅ Implement different chunking strategies and understand their tradeoffs
✅ Extract and validate metadata from documents
✅ Measure chunking quality with evaluation metrics
✅ Handle errors and retries in production pipelines

## Why This Matters

Bad ingestion → bad retrieval → bad answers

Most RAG failures start at ingestion:
- Wrong chunk size → context loss or noise
- Missing metadata → poor filtering
- Inconsistent processing → degraded search quality
- No validation → silent failures

This module teaches you to build **deterministic, testable, observable** pipelines.

## The Bronze/Silver/Gold Pattern

This is a data engineering pattern from data lakes/warehouses, adapted for RAG:

```
Raw Documents (PDF, DOCX, TXT, MD)
       ↓
[BRONZE] Raw ingestion - minimal processing
   - Extract text
   - Store original format
   - Add timestamps and source metadata
       ↓
[SILVER] Cleaning and normalization
   - Fix encoding issues
   - Remove boilerplate
   - Normalize whitespace
   - Extract structured metadata
       ↓
[GOLD] Chunking and enrichment
   - Apply chunking strategy
   - Add semantic metadata
   - Validate quality
   - Ready for embedding
```

**Benefits:**
- Can re-process from any stage without re-downloading
- Each stage is testable independently
- Failed stages don't lose raw data
- Easy to compare different chunking strategies

## Module Structure

```
01-ingestion/
├── prefect_flows/
│   ├── bronze_flow.py       # Raw ingestion
│   ├── silver_flow.py       # Cleaning and normalization
│   ├── gold_flow.py         # Chunking and enrichment
│   └── full_pipeline.py     # Orchestrated end-to-end
│
├── chunking/
│   ├── strategies.py        # Different chunking approaches
│   ├── evaluation.py        # Chunking quality metrics
│   └── examples/            # Comparison examples
│
├── metadata/
│   ├── extractors.py        # Metadata extraction
│   ├── validators.py        # Metadata validation
│   └── schema.py            # Metadata schemas
│
├── examples/
│   ├── 01_basic_pipeline.py      # Simple pipeline
│   ├── 02_bronze_silver_gold.py  # Full BSG pattern
│   ├── 03_chunking_strategies.py # Compare strategies
│   └── 04_metadata_extraction.py # Metadata handling
│
└── exercises/
    ├── exercise_01_build_pipeline.py    # Build your pipeline
    ├── exercise_02_compare_chunking.py  # Evaluate chunking
    └── exercise_03_error_handling.py    # Production patterns
```

## Quick Start

```bash
# Navigate to module
cd 01-ingestion

# Run basic example
python examples/01_basic_pipeline.py

# Run Prefect UI (in another terminal)
prefect server start

# Execute full pipeline
python examples/02_bronze_silver_gold.py

# View results in Prefect UI
open http://localhost:4200
```

## Chunking Strategies

This module implements and compares several chunking strategies:

### 1. Fixed-Size Chunking

**Strategy:** Split text into fixed-size chunks with overlap

```python
chunks = fixed_size_chunker(
    text=document,
    chunk_size=512,      # tokens
    overlap=50,          # tokens
)
```

**Pros:**
- Simple, predictable
- Consistent chunk sizes for embeddings

**Cons:**
- May split sentences/paragraphs awkwardly
- No semantic awareness

**Best for:** General documents, when you need predictable chunk sizes

### 2. Semantic Chunking

**Strategy:** Split on semantic boundaries (paragraphs, sections)

```python
chunks = semantic_chunker(
    text=document,
    separators=["\n\n", "\n", ". ", " "],
    target_size=512,
    max_size=768,
)
```

**Pros:**
- Respects document structure
- Preserves semantic coherence

**Cons:**
- Variable chunk sizes
- May create very small or large chunks

**Best for:** Structured documents with clear sections

### 3. Recursive Character Splitting

**Strategy:** Try different separators in order, recursively

```python
chunks = recursive_character_splitter(
    text=document,
    separators=["\n\n", "\n", ". ", " "],
    chunk_size=512,
    chunk_overlap=50,
)
```

**Pros:**
- Balance between semantic and fixed-size
- Used by LangChain by default

**Cons:**
- More complex to configure
- Still may split awkwardly

**Best for:** Mixed content types

### 4. Markdown-Aware Chunking

**Strategy:** Respect markdown structure (headers, code blocks, lists)

```python
chunks = markdown_chunker(
    text=markdown_document,
    chunk_size=512,
    respect_headers=True,
    respect_code_blocks=True,
)
```

**Pros:**
- Preserves code blocks intact
- Maintains header context

**Cons:**
- Only works for markdown
- May create large chunks for big code blocks

**Best for:** Technical documentation, README files, blog posts

## Chunking Evaluation Metrics

How do you know if your chunking strategy is good?

### Metrics We Track:

1. **Chunk Size Distribution**
   - Mean, median, std dev of chunk sizes
   - Percentage within target range
   - Outliers (too small/large)

2. **Boundary Quality**
   - Percentage of chunks ending at sentence boundaries
   - Percentage ending at paragraph boundaries
   - Split sentences (bad!)

3. **Semantic Coherence**
   - Embed each chunk
   - Measure within-chunk similarity
   - Higher = more coherent

4. **Coverage**
   - Total tokens in → total tokens in chunks
   - Should be ~100% (no data loss)

### Example Evaluation:

```python
from chunking.evaluation import evaluate_chunking

results = evaluate_chunking(
    original_text=document,
    chunks=chunks,
    embeddings=embeddings,
)

print(results)
# {
#     "mean_chunk_size": 487,
#     "std_chunk_size": 52,
#     "pct_in_range": 0.94,
#     "pct_sentence_boundary": 0.87,
#     "semantic_coherence": 0.82,
#     "coverage": 0.998,
# }
```

## Metadata Extraction

Good metadata improves retrieval quality dramatically:

### Document-Level Metadata

```python
{
    "source": "docs/api-reference.md",
    "doc_type": "markdown",
    "author": "engineering-team",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T14:22:00Z",
    "tags": ["api", "reference", "backend"],
    "language": "en",
}
```

### Chunk-Level Metadata

```python
{
    "chunk_id": "api-reference_chunk_003",
    "chunk_index": 3,
    "total_chunks": 24,
    "section": "Authentication",
    "subsection": "OAuth 2.0 Flow",
    "chunk_size": 512,
    "has_code": True,
    "code_language": "python",
}
```

### Why Metadata Matters

Enables filtered retrieval:

```python
# Only search API documentation
results = vector_store.search(
    query="how to authenticate",
    filter={"tags": {"$contains": "api"}},
)

# Only recent docs
results = vector_store.search(
    query="new features",
    filter={"updated_at": {"$gte": "2024-01-01"}},
)

# Only code examples in Python
results = vector_store.search(
    query="example implementation",
    filter={"has_code": True, "code_language": "python"},
)
```

## Prefect Flows

Prefect provides:
- **Observability**: See every step in the UI
- **Retries**: Automatic retry on failure
- **Caching**: Skip expensive recomputation
- **Scheduling**: Run pipelines on a schedule
- **Parametrization**: Easy configuration

### Flow Structure

```python
from prefect import flow, task

@task(retries=3, retry_delay_seconds=60)
def extract_text(file_path: str) -> str:
    """Bronze: Extract raw text"""
    # ... extraction logic
    return raw_text

@task
def clean_text(raw_text: str) -> str:
    """Silver: Clean and normalize"""
    # ... cleaning logic
    return cleaned_text

@task
def chunk_text(cleaned_text: str, strategy: str) -> list:
    """Gold: Chunk and enrich"""
    # ... chunking logic
    return chunks

@flow(name="Document Ingestion")
def ingest_document(file_path: str, strategy: str = "recursive"):
    """Full Bronze → Silver → Gold pipeline"""
    raw = extract_text(file_path)
    cleaned = clean_text(raw)
    chunks = chunk_text(cleaned, strategy)
    return chunks
```

## Exercises

### Exercise 1: Build Your Pipeline

File: `exercises/exercise_01_build_pipeline.py`

Build a complete ingestion pipeline that:
1. Reads documents from a directory
2. Processes them through Bronze → Silver → Gold
3. Validates each stage
4. Stores results with metadata

**Success criteria:**
- Pipeline completes without errors
- All stages logged to Prefect
- Metadata properly extracted
- Output validates against schema

### Exercise 2: Compare Chunking Strategies

File: `exercises/exercise_02_compare_chunking.py`

Implement and compare 3 chunking strategies:
1. Fixed-size (512 tokens, 50 overlap)
2. Semantic (paragraph boundaries)
3. Recursive character splitting

**Tasks:**
- Apply all three to the same document
- Compute evaluation metrics for each
- Determine which is best for this document type

**Questions to answer:**
- Which strategy has best semantic coherence?
- Which has most consistent chunk sizes?
- Which would you use for technical docs? Blog posts? Chat logs?

### Exercise 3: Production Error Handling

File: `exercises/exercise_03_error_handling.py`

Add production-grade error handling:
- Retry logic for transient failures
- Logging for debugging
- Partial failure handling (process what you can)
- Dead letter queue for failed documents

**Scenarios to handle:**
- Corrupted file
- Encoding issues
- Very large document
- Network timeout (if fetching remote)

## Key Takeaways

After this module, you should understand:

1. **Ingestion is data engineering** - Apply the same rigor as data pipelines
2. **Bronze/Silver/Gold separation** - Stages allow reprocessing without waste
3. **Chunking is crucial** - Wrong strategy → poor retrieval
4. **Metadata enables filtering** - Good metadata = better search
5. **Observability matters** - Use Prefect to see what's happening
6. **Evaluation over intuition** - Measure chunking quality, don't guess

## Common Mistakes to Avoid

❌ **Fixed 500-char chunks for everything** - Wrong unit (use tokens), ignores structure
❌ **No metadata** - Limits filtering options
❌ **No validation** - Silent failures
❌ **Processing in a single step** - Can't recover from failures
❌ **Ignoring chunk boundaries** - Split sentences reduce quality
❌ **No caching** - Reprocess everything on every run

## Next Module

Once you complete this module:

✅ Verify your pipeline with: `python examples/02_bronze_silver_gold.py`
✅ Complete all exercises
✅ Update your learning journal
✅ Move to **Module 02: Retrievers** to learn how to search your chunked data

---

**Remember:** Perfect chunks → good embeddings → great retrieval → accurate answers
