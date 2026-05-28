"""
Core configuration for Self-Learning AI
"""
import os
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LLMConfig:
    provider: str = os.getenv("LLM_PROVIDER", "openai")
    model: str = os.getenv("LLM_MODEL", "gpt-4")
    api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    base_url: Optional[str] = os.getenv("LLM_BASE_URL")
    temperature: float = 0.7
    max_tokens: int = 4000

@dataclass
class SafetyConfig:
    sandbox_enabled: bool = True
    human_approval_required: bool = True
    max_cost_per_run: float = 10.0
    allowed_code_changes: List[str] = field(default_factory=lambda: [".py", ".md", ".json", ".yaml"])
    blocked_operations: List[str] = field(default_factory=lambda: ["rm -rf", "drop database", "sudo"])

@dataclass
class MemoryConfig:
    vector_db_type: str = os.getenv("VECTOR_DB", "chroma")
    persist_directory: str = "./data/memory"
    max_memory_items: int = 10000

@dataclass
class Config:
    llm: LLMConfig = field(default_factory=LLMConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    goals: List[str] = field(default_factory=list)
    learning_topics: List[str] = field(default_factory=list)

config = Config()