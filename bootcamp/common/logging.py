"""
Structured logging for the bootcamp

Uses loguru for beautiful, structured logging with:
- Colored output for development
- JSON output for production
- Automatic context injection
- Performance tracking
"""

import sys
import time
from pathlib import Path
from typing import Optional, Any, Dict
from contextlib import contextmanager

from loguru import logger

from common.config import settings


def setup_logging(
    log_file: Optional[Path] = None,
    level: str = "INFO",
    format_type: str = "pretty",
) -> None:
    """
    Configure logging for the application

    Args:
        log_file: Path to log file (optional)
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        format_type: "pretty" for development, "json" for production
    """
    # Remove default handler
    logger.remove()

    # Pretty format for development
    if format_type == "pretty":
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
            level=level,
            colorize=True,
        )
    # JSON format for production
    else:
        logger.add(
            sys.stderr,
            format="{message}",
            level=level,
            serialize=True,
        )

    # Add file handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            rotation="500 MB",
            retention="10 days",
            compression="zip",
            level=level,
            serialize=(format_type == "json"),
        )


def get_logger(name: str) -> Any:
    """
    Get a logger instance with context

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance with bound context
    """
    return logger.bind(module=name)


@contextmanager
def log_execution_time(operation: str, logger_instance: Any = logger):
    """
    Context manager to log execution time

    Args:
        operation: Description of the operation
        logger_instance: Logger to use

    Examples:
        >>> with log_execution_time("embedding documents"):
        ...     vectors = embed_docs(documents)
    """
    start_time = time.time()
    logger_instance.info(f"Starting: {operation}")

    try:
        yield
    except Exception as e:
        elapsed = time.time() - start_time
        logger_instance.error(
            f"Failed: {operation} after {elapsed:.2f}s", exception=e
        )
        raise
    else:
        elapsed = time.time() - start_time
        logger_instance.success(
            f"Completed: {operation} in {elapsed:.2f}s"
        )


class ProgressTracker:
    """Track progress of multi-step operations"""

    def __init__(self, total_steps: int, operation: str):
        self.total_steps = total_steps
        self.current_step = 0
        self.operation = operation
        self.start_time = time.time()
        logger.info(f"Starting {operation} ({total_steps} steps)")

    def step(self, description: str = "") -> None:
        """Increment progress and log"""
        self.current_step += 1
        elapsed = time.time() - self.start_time
        progress_pct = (self.current_step / self.total_steps) * 100

        logger.info(
            f"[{self.current_step}/{self.total_steps}] "
            f"({progress_pct:.1f}%) {description}",
            elapsed=elapsed,
        )

    def complete(self) -> None:
        """Mark operation as complete"""
        total_time = time.time() - self.start_time
        logger.success(
            f"Completed {self.operation}: "
            f"{self.total_steps} steps in {total_time:.2f}s"
        )


def log_metrics(metrics: Dict[str, Any], prefix: str = "") -> None:
    """
    Log metrics in a structured way

    Args:
        metrics: Dictionary of metrics
        prefix: Prefix for log message

    Examples:
        >>> log_metrics({
        ...     "precision": 0.85,
        ...     "recall": 0.78,
        ...     "f1": 0.81
        ... }, prefix="Evaluation")
    """
    metric_str = " | ".join(
        f"{k}: {v:.3f}" if isinstance(v, float) else f"{k}: {v}"
        for k, v in metrics.items()
    )

    if prefix:
        logger.info(f"{prefix} | {metric_str}", **metrics)
    else:
        logger.info(metric_str, **metrics)


# Initialize logging on import
setup_logging(
    level=settings.log_level,
    format_type=settings.log_format,
)


# Example usage
if __name__ == "__main__":
    # Test logging
    test_logger = get_logger(__name__)

    test_logger.debug("Debug message")
    test_logger.info("Info message")
    test_logger.warning("Warning message")
    test_logger.success("Success message")

    # Test execution time tracking
    with log_execution_time("test operation"):
        time.sleep(0.5)

    # Test progress tracking
    tracker = ProgressTracker(5, "test workflow")
    for i in range(5):
        time.sleep(0.1)
        tracker.step(f"Processing item {i+1}")
    tracker.complete()

    # Test metrics logging
    log_metrics(
        {
            "accuracy": 0.95,
            "precision": 0.92,
            "recall": 0.88,
            "f1": 0.90,
        },
        prefix="Model Evaluation",
    )
