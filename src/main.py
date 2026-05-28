"""
Main Self-Learning AI Orchestrator
Coordinates the scratch learning core
"""

from typing import Dict, Any, List, Optional
from .memory import MemorySystem
from .learning_core import ScratchAI
from .config import Config

class SelfLearningAI:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        
        # Initialize components
        self.memory = MemorySystem(self.config.memory.persist_directory)
        self.ai_core = ScratchAI(self.memory)
        
        self.pending_approvals = []

    def generate_response(self, message: str) -> str:
        """Generate response using the scratch AI core"""
        return self.ai_core.generate_response(message)

    def set_goal(self, goal: str, priority: str = "medium"):
        """Set a learning goal for the AI"""
        goal_data = self.memory.add_goal(goal, priority)
        return goal_data

    def learn_topic(self, topic: str):
        """Learn about a specific topic"""
        return self.ai_core.learn_topic(topic)

    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "pending_approvals": len(self.pending_approvals),
            "memory_items": len(self.memory.short_term) + len(self.memory.long_term),
            "learned_topics": list(self.memory.learned_topics.keys())
        }

def main():
    """Example usage"""
    ai = SelfLearningAI()
    print("Scratch AI initialized. Type something to start learning.")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            response = ai.generate_response(user_input)
            print(f"AI: {response}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
