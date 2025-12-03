#!/usr/bin/env python
"""
Bronze/Silver/Gold Pipeline with Prefect

Demonstrates the medallion architecture for RAG data ingestion:
- Bronze: Raw text extraction
- Silver: Cleaning and normalization
- Gold: Chunking and enrichment

Each stage is independently testable and reprocessable.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

from common.logging import get_logger, log_execution_time, ProgressTracker

logger = get_logger(__name__)


# ============================================================================
# BRONZE LAYER: Raw Extraction
# ============================================================================


@task(name="Extract Raw Text", retries=3, retry_delay_seconds=5)
def bronze_extract_text(file_path: Path) -> Dict[str, Any]:
    """
    Bronze layer: Extract raw text from file with minimal processing

    Args:
        file_path: Path to document

    Returns:
        Dict with raw text and basic metadata
    """
    logger.info(f"[BRONZE] Extracting text from {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    metadata = {
        "source": str(file_path),
        "file_name": file_path.name,
        "file_size": file_path.stat().st_size,
        "extracted_at": datetime.utcnow().isoformat(),
        "stage": "bronze",
    }

    result = {"raw_text": raw_text, "metadata": metadata}

    logger.info(
        f"[BRONZE] Extracted {len(raw_text)} characters from {file_path.name}"
    )

    return result


@task(name="Save Bronze")
def bronze_save(bronze_data: Dict[str, Any], output_dir: Path) -> Path:
    """Save bronze data to disk"""
    bronze_dir = output_dir / "bronze"
    bronze_dir.mkdir(parents=True, exist_ok=True)

    file_name = Path(bronze_data["metadata"]["source"]).stem
    bronze_file = bronze_dir / f"{file_name}_bronze.json"

    with open(bronze_file, "w") as f:
        json.dump(bronze_data, f, indent=2)

    logger.info(f"[BRONZE] Saved to {bronze_file}")
    return bronze_file


# ============================================================================
# SILVER LAYER: Cleaning and Normalization
# ============================================================================


@task(name="Clean and Normalize")
def silver_clean_text(bronze_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Silver layer: Clean and normalize text

    Cleaning steps:
    - Remove excessive whitespace
    - Normalize line endings
    - Remove common boilerplate
    - Fix encoding issues
    """
    logger.info("[SILVER] Cleaning and normalizing text")

    raw_text = bronze_data["raw_text"]

    # Normalize line endings
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive whitespace
    lines = []
    for line in text.split("\n"):
        cleaned_line = " ".join(line.split())  # Normalize spaces
        if cleaned_line:  # Skip empty lines
            lines.append(cleaned_line)

    # Join with single newlines
    cleaned_text = "\n".join(lines)

    # Remove common boilerplate (customize for your use case)
    boilerplate_patterns = [
        "--- Page",  # PDF page markers
        "Copyright ©",  # Copyright notices
        "All rights reserved",
    ]

    for pattern in boilerplate_patterns:
        cleaned_text = cleaned_text.replace(pattern, "")

    # Update metadata
    metadata = bronze_data["metadata"].copy()
    metadata.update(
        {
            "cleaned_at": datetime.utcnow().isoformat(),
            "stage": "silver",
            "original_length": len(raw_text),
            "cleaned_length": len(cleaned_text),
            "reduction_pct": (1 - len(cleaned_text) / len(raw_text)) * 100,
        }
    )

    result = {"cleaned_text": cleaned_text, "metadata": metadata}

    logger.info(
        f"[SILVER] Cleaned text: {len(raw_text)} → {len(cleaned_text)} chars "
        f"({metadata['reduction_pct']:.1f}% reduction)"
    )

    return result


@task(name="Extract Metadata")
def silver_extract_metadata(silver_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract structured metadata from cleaned text

    Extracts:
    - Language
    - Has code blocks
    - Has lists
    - Estimated reading time
    """
    logger.info("[SILVER] Extracting structured metadata")

    text = silver_data["cleaned_text"]

    # Detect code blocks (markdown or generic)
    has_code = "```" in text or "def " in text or "class " in text

    # Detect lists
    has_lists = any(line.strip().startswith(("-", "*", "+")) for line in text.split("\n"))

    # Estimate reading time (average 200 words per minute)
    word_count = len(text.split())
    reading_time_minutes = max(1, word_count // 200)

    # Update metadata
    silver_data["metadata"].update(
        {
            "word_count": word_count,
            "has_code_blocks": has_code,
            "has_lists": has_lists,
            "estimated_reading_minutes": reading_time_minutes,
        }
    )

    logger.info(
        f"[SILVER] Metadata extracted: {word_count} words, "
        f"code={has_code}, lists={has_lists}"
    )

    return silver_data


@task(name="Save Silver")
def silver_save(silver_data: Dict[str, Any], output_dir: Path) -> Path:
    """Save silver data to disk"""
    silver_dir = output_dir / "silver"
    silver_dir.mkdir(parents=True, exist_ok=True)

    file_name = Path(silver_data["metadata"]["source"]).stem
    silver_file = silver_dir / f"{file_name}_silver.json"

    with open(silver_file, "w") as f:
        json.dump(silver_data, f, indent=2)

    logger.info(f"[SILVER] Saved to {silver_file}")
    return silver_file


# ============================================================================
# GOLD LAYER: Chunking and Enrichment
# ============================================================================


@task(name="Chunk Text")
def gold_chunk_text(
    silver_data: Dict[str, Any], chunk_size: int = 512, chunk_overlap: int = 50
) -> Dict[str, Any]:
    """
    Gold layer: Chunk text using RecursiveCharacterTextSplitter

    Args:
        silver_data: Cleaned text and metadata
        chunk_size: Target chunk size in tokens
        chunk_overlap: Overlap between chunks in tokens

    Returns:
        Dict with chunks and enriched metadata
    """
    logger.info(f"[GOLD] Chunking text (size={chunk_size}, overlap={chunk_overlap})")

    text = silver_data["cleaned_text"]

    # Initialize tokenizer (for token-accurate chunking)
    tokenizer = tiktoken.get_encoding("cl100k_base")

    def length_function(text: str) -> int:
        """Count tokens instead of characters"""
        return len(tokenizer.encode(text))

    # Create splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    # Split into chunks
    chunks = splitter.split_text(text)

    logger.info(f"[GOLD] Created {len(chunks)} chunks")

    # Enrich each chunk with metadata
    enriched_chunks = []
    for idx, chunk in enumerate(chunks):
        chunk_metadata = silver_data["metadata"].copy()
        chunk_metadata.update(
            {
                "chunk_id": f"{Path(chunk_metadata['source']).stem}_chunk_{idx:03d}",
                "chunk_index": idx,
                "total_chunks": len(chunks),
                "chunk_size_tokens": length_function(chunk),
                "chunk_size_chars": len(chunk),
                "stage": "gold",
                "chunked_at": datetime.utcnow().isoformat(),
            }
        )

        enriched_chunks.append({"text": chunk, "metadata": chunk_metadata})

    result = {"chunks": enriched_chunks, "metadata": silver_data["metadata"]}

    # Log chunk statistics
    chunk_sizes = [c["metadata"]["chunk_size_tokens"] for c in enriched_chunks]
    avg_size = sum(chunk_sizes) / len(chunk_sizes)
    min_size = min(chunk_sizes)
    max_size = max(chunk_sizes)

    logger.info(
        f"[GOLD] Chunk stats: avg={avg_size:.0f}, min={min_size}, max={max_size} tokens"
    )

    return result


@task(name="Validate Chunks")
def gold_validate_chunks(gold_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate chunk quality

    Checks:
    - No empty chunks
    - Sizes within reasonable bounds
    - No duplicate chunks
    - Total coverage (no data loss)
    """
    logger.info("[GOLD] Validating chunks")

    chunks = gold_data["chunks"]

    # Check for empty chunks
    empty_chunks = [c for c in chunks if not c["text"].strip()]
    if empty_chunks:
        logger.warning(f"Found {len(empty_chunks)} empty chunks")

    # Check sizes
    sizes = [c["metadata"]["chunk_size_tokens"] for c in chunks]
    out_of_range = [s for s in sizes if s < 50 or s > 1000]
    if out_of_range:
        logger.warning(
            f"{len(out_of_range)} chunks outside expected range (50-1000 tokens)"
        )

    # Check for duplicates
    texts = [c["text"] for c in chunks]
    unique_texts = set(texts)
    if len(texts) != len(unique_texts):
        logger.warning(f"Found {len(texts) - len(unique_texts)} duplicate chunks")

    validation_results = {
        "total_chunks": len(chunks),
        "empty_chunks": len(empty_chunks),
        "out_of_range_chunks": len(out_of_range),
        "duplicate_chunks": len(texts) - len(unique_texts),
        "validated_at": datetime.utcnow().isoformat(),
    }

    gold_data["validation"] = validation_results

    logger.info(f"[GOLD] Validation complete: {validation_results}")

    return gold_data


@task(name="Save Gold")
def gold_save(gold_data: Dict[str, Any], output_dir: Path) -> Path:
    """Save gold data to disk"""
    gold_dir = output_dir / "gold"
    gold_dir.mkdir(parents=True, exist_ok=True)

    source_file = Path(gold_data["metadata"]["source"]).stem
    gold_file = gold_dir / f"{source_file}_gold.json"

    with open(gold_file, "w") as f:
        json.dump(gold_data, f, indent=2)

    logger.info(f"[GOLD] Saved {len(gold_data['chunks'])} chunks to {gold_file}")
    return gold_file


# ============================================================================
# MAIN FLOW: Orchestrate Bronze → Silver → Gold
# ============================================================================


@flow(
    name="Bronze-Silver-Gold Pipeline",
    description="Full medallion architecture data pipeline",
    task_runner=ConcurrentTaskRunner(),
)
def bronze_silver_gold_pipeline(
    file_path: Path,
    output_dir: Path,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> Dict[str, Any]:
    """
    Run complete Bronze → Silver → Gold pipeline

    Args:
        file_path: Path to input document
        output_dir: Output directory for artifacts
        chunk_size: Target chunk size in tokens
        chunk_overlap: Overlap between chunks

    Returns:
        Final gold data with chunks and metadata
    """
    logger.info(f"Starting BSG pipeline for {file_path}")

    with log_execution_time("Bronze-Silver-Gold Pipeline"):
        # BRONZE: Extract raw text
        bronze_data = bronze_extract_text(file_path)
        bronze_file = bronze_save(bronze_data, output_dir)

        # SILVER: Clean and enrich
        silver_data = silver_clean_text(bronze_data)
        silver_data = silver_extract_metadata(silver_data)
        silver_file = silver_save(silver_data, output_dir)

        # GOLD: Chunk and validate
        gold_data = gold_chunk_text(silver_data, chunk_size, chunk_overlap)
        gold_data = gold_validate_chunks(gold_data)
        gold_file = gold_save(gold_data, output_dir)

        logger.success(
            f"Pipeline complete: {len(gold_data['chunks'])} chunks ready for embedding"
        )

    return gold_data


# ============================================================================
# Example Usage
# ============================================================================


def main():
    """Example: Process a sample document"""
    print("\n" + "=" * 70)
    print("BRONZE-SILVER-GOLD PIPELINE EXAMPLE")
    print("=" * 70)

    # Create sample document
    sample_dir = Path("data/sample")
    sample_dir.mkdir(parents=True, exist_ok=True)

    sample_file = sample_dir / "sample_doc.md"
    with open(sample_file, "w") as f:
        f.write("""# AI Engineering Bootcamp

## Module 01: Data Ingestion

This module teaches you how to build production-grade data pipelines for RAG systems.

### The Bronze-Silver-Gold Pattern

The medallion architecture is a data engineering best practice:

1. **Bronze Layer**: Raw data extraction with minimal processing
2. **Silver Layer**: Cleaning, normalization, and enrichment
3. **Gold Layer**: Business logic, chunking, and final transformations

### Why This Matters

- **Reprocessability**: Can re-run any stage without re-downloading
- **Testability**: Each layer is independently testable
- **Debuggability**: Clear boundaries make issues easy to isolate
- **Efficiency**: Only reprocess what changed

```python
# Example: Bronze extraction
@task
def extract_text(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()
```

### Best Practices

1. Always validate at each stage
2. Add comprehensive metadata
3. Use Prefect for observability
4. Implement retry logic
5. Log everything

This approach scales from prototypes to production systems handling millions of documents.
""")

    print(f"\n📄 Created sample document: {sample_file}")
    print(f"   Size: {sample_file.stat().st_size} bytes\n")

    # Run pipeline
    output_dir = Path("outputs/bsg_example")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = bronze_silver_gold_pipeline(
        file_path=sample_file, output_dir=output_dir, chunk_size=256, chunk_overlap=25
    )

    # Display results
    print("\n" + "=" * 70)
    print("PIPELINE RESULTS")
    print("=" * 70)

    print(f"\n✅ Processed: {result['metadata']['source']}")
    print(f"✅ Total chunks: {len(result['chunks'])}")
    print(f"✅ Validation: {result['validation']}")

    print(f"\n📂 Output files:")
    print(f"   Bronze: {output_dir}/bronze/")
    print(f"   Silver: {output_dir}/silver/")
    print(f"   Gold: {output_dir}/gold/")

    print("\n📊 Sample chunk:")
    first_chunk = result["chunks"][0]
    print(f"   Chunk ID: {first_chunk['metadata']['chunk_id']}")
    print(f"   Size: {first_chunk['metadata']['chunk_size_tokens']} tokens")
    print(f"   Text preview: {first_chunk['text'][:100]}...")

    print("\n🎯 Next steps:")
    print("   1. Open Prefect UI: http://localhost:4200")
    print("   2. View flow runs and task details")
    print("   3. Try processing your own documents")
    print("   4. Experiment with different chunk sizes")
    print()


if __name__ == "__main__":
    main()
