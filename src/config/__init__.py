"""
Core configuration for Self-Learning AI
"""
import os
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LearningConfig:
    algorithm: str = os.getenv("LEARNING_ALGO", "markov")
    memory_size: int = 1000
    learning_rate: float = 0.1

@dataclass
class SafetyConfig:
    sandbox_enabled: bool = True
    human_approval_required: bool = True
    max_cost_per_run: float = 10.0
    allowed_code_changes: List[str] = field(default_factory=lambda: [".py", ".md", ".json", ".yaml"])
    blocked_operations: List[str] = field(default_factory=lambda: ["rm -rf", "drop database", "sudo"])

@dataclass
class MemoryConfig:
    persist_directory: str = "./data/memory"
    max_memory_items: int = 10000

@dataclass
class Config:
    learning: LearningConfig = field(default_factory=LearningConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    goals: List[str] = field(default_factory=list)
    learning_topics: List[str] = field(default_factory=list)

config = Config()
