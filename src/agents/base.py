"""
Base Agent class for Self-Learning AI
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json

class BaseAgent(ABC):
    def __init__(self, name: str, memory, llm_config: Dict):
        self.name = name
        self.memory = memory
        self.llm_config = llm_config

    @abstractmethod
    def run(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        pass

    def think(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Use the LLM to think about a task"""
        # Placeholder for actual LLM call
        # In production, this would call OpenAI, Claude, or local LLM
        return f"[{self.name}] Processing: {prompt[:100]}..."

    def log(self, message: str, level: str = "info"):
        """Log agent activity"""
        timestamp = self.memory.add(
            type="log",
            content=f"[{self.name}] {level.upper()}: {message}",
            metadata={"agent": self.name, "level": level}
        )
        print(f"[{self.name}] {message}")
        return timestamp

    def save_result(self, result: Dict[str, Any]):
        """Save agent output to memory"""
        self.memory.add(
            type="result",
            content=json.dumps(result),
            metadata={"agent": self.name, "result_type": type(result).__name__}
        )