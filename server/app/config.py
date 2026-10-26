import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///./demo.db')
    storage: Path = Path(os.getenv('PRIVATE_STORAGE', './private_uploads'))
    analyst_token: str = os.getenv('ANALYST_TOKEN', 'local-analyst-change-me')
    reviewer_token: str = os.getenv('REVIEWER_TOKEN', 'local-reviewer-change-me')
    llm_mode: str = os.getenv('LLM_MODE', 'mock')
    ollama_host: str = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    ollama_model: str = os.getenv('OLLAMA_MODEL', '')
    llm_timeout: float = float(os.getenv('LLM_TIMEOUT', '45'))
    llm_retries: int = int(os.getenv('LLM_RETRIES', '1'))
    max_upload: int = 10 * 1024 * 1024
    max_pages: int = 50
    cors_origins: str = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:8080')
settings = Settings()

