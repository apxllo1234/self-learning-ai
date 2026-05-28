"""
Memory System for Self-Learning AI
Stores knowledge, context, and learning progress
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class MemoryItem:
    id: str
    type: str  # knowledge, experience, goal, learning
    content: str
    metadata: Dict[str, Any]
    created_at: str
    accessed_count: int = 0
    relevance_score: float = 0.0

class MemorySystem:
    def __init__(self, persist_dir: str = "./data/memory"):
        self.persist_dir = persist_dir
        self.short_term: List[MemoryItem] = []
        self.long_term: Dict[str, MemoryItem] = {}
        self.goals: List[Dict] = []
        self.learned_topics: Dict[str, List[str]] = {}
        os.makedirs(persist_dir, exist_ok=True)
        self._load()

    def _generate_id(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def add(self, type: str, content: str, metadata: Optional[Dict] = None) -> MemoryItem:
        item = MemoryItem(
            id=self._generate_id(content),
            type=type,
            content=content,
            metadata=metadata or {},
            created_at=datetime.now().isoformat()
        )
        self.short_term.append(item)
        if len(self.short_term) > 20:
            self._consolidate_to_long_term()
        self._save()
        return item

    def _consolidate_to_long_term(self):
        """Move important short-term memories to long-term storage"""
        for item in self.short_term[:5]:
            self.long_term[item.id] = item
        self.short_term = self.short_term[5:]

    def search(self, query: str, limit: int = 10) -> List[MemoryItem]:
        results = []
        for item in list(self.short_term) + list(self.long_term.values()):
            if query.lower() in item.content.lower():
                item.accessed_count += 1
                results.append(item)
        return sorted(results, key=lambda x: x.accessed_count, reverse=True)[:limit]

    def get_goals(self) -> List[Dict]:
        return self.goals

    def add_goal(self, goal: str, priority: str = "medium") -> Dict:
        goal_data = {
            "id": self._generate_id(goal),
            "goal": goal,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "progress": []
        }
        self.goals.append(goal_data)
        self._save()
        return goal_data

    def update_goal(self, goal_id: str, status: str, progress: str):
        for g in self.goals:
            if g["id"] == goal_id:
                g["status"] = status
                g["progress"].append({
                    "timestamp": datetime.now().isoformat(),
                    "update": progress
                })
                self._save()
                return g
        return None

    def get_all(self) -> Dict[str, Any]:
        return {
            "short_term": [asdict(i) for i in self.short_term],
            "long_term": {k: asdict(v) for k, v in self.long_term.items()},
            "goals": self.goals,
            "learned_topics": self.learned_topics
        }

    def _save(self):
        data = {
            "long_term": {k: asdict(v) for k, v in self.long_term.items()},
            "goals": self.goals,
            "learned_topics": self.learned_topics
        }
        with open(os.path.join(self.persist_dir, "memory.json"), "w") as f:
            json.dump(data, f, indent=2)

    def _load(self):
        path = os.path.join(self.persist_dir, "memory.json")
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                self.long_term = {k: MemoryItem(**v) for k, v in data.get("long_term", {}).items()}
                self.goals = data.get("goals", [])
                self.learned_topics = data.get("learned_topics", {})
            except Exception:
                pass

    def clear(self):
        self.short_term = []
        self.long_term = {}
        self._save()