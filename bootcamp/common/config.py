"""
Configuration management for the bootcamp

Loads environment variables and provides typed settings using Pydantic.
"""

from pathlib import Path
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    # ========================================================================
    # LLM API Keys
    # ========================================================================
    openai_api_key: Optional[str] = None
    openai_org_id: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # ========================================================================
    # LangSmith
    # ========================================================================
    langsmith_api_key: Optional[str] = None
    langsmith_project: str = "bootcamp-default"
    langsmith_tracing: bool = Field(default=False, alias="LANGSMITH_TRACING")
    langsmith_endpoint: str = "https://api.smith.langchain.com"

    # ========================================================================
    # Vector Database (Qdrant)
    # ========================================================================
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_grpc_port: int = 6334
    qdrant_url: Optional[str] = None  # For Qdrant Cloud
    qdrant_api_key: Optional[str] = None

    # ========================================================================
    # Graph Database (Neo4j)
    # ========================================================================
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "bootcamp123"

    # ========================================================================
    # Graphiti
    # ========================================================================
    graphiti_storage_type: Literal["neo4j", "falkordb"] = "neo4j"
    graphiti_llm_provider: Literal["openai", "anthropic"] = "openai"

    # ========================================================================
    # Prefect
    # ========================================================================
    prefect_api_url: str = "http://127.0.0.1:4200/api"
    prefect_logging_level: str = "INFO"

    # ========================================================================
    # Application Settings
    # ========================================================================
    environment: Literal["development", "staging", "production"] = "development"
    log_level: str = "INFO"
    log_format: Literal["json", "pretty"] = "pretty"

    # Data directories
    data_dir: Path = Field(default=Path("./data"))
    cache_dir: Path = Field(default=Path("./.cache"))
    output_dir: Path = Field(default=Path("./outputs"))

    # ========================================================================
    # Embedding Models
    # ========================================================================
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    # ========================================================================
    # Module-Specific Settings
    # ========================================================================
    # Chunking defaults (Module 01)
    default_chunk_size: int = 512
    default_chunk_overlap: int = 50

    # Retrieval defaults (Module 02)
    top_k_results: int = 10
    rerank_top_k: int = 5

    # Agent defaults (Module 04)
    max_iterations: int = 10
    agent_timeout: int = 300

    # ========================================================================
    # Optional: External Tools
    # ========================================================================
    google_api_key: Optional[str] = None
    google_cse_id: Optional[str] = None
    tavily_api_key: Optional[str] = None

    # ========================================================================
    # Development/Testing
    # ========================================================================
    test_mode: bool = False
    test_llm_model: str = "gpt-3.5-turbo"
    debug: bool = False

    def model_post_init(self, __context) -> None:
        """Create directories if they don't exist"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment == "production"

    def get_qdrant_config(self) -> dict:
        """Get Qdrant connection configuration"""
        if self.qdrant_url:
            return {"url": self.qdrant_url, "api_key": self.qdrant_api_key}
        return {"host": self.qdrant_host, "port": self.qdrant_port}

    def get_neo4j_config(self) -> dict:
        """Get Neo4j connection configuration"""
        return {
            "uri": self.neo4j_uri,
            "user": self.neo4j_user,
            "password": self.neo4j_password,
        }


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance"""
    return settings


def reload_settings() -> Settings:
    """Reload settings from environment (useful for testing)"""
    global settings
    settings = Settings()
    return settings
