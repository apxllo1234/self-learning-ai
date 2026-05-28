"""
Main Self-Learning AI Orchestrator
Coordinates all agents and manages the learning loop
"""

from typing import Dict, Any, List, Optional
from .memory import MemorySystem
from .agents.research_agent import ResearchAgent
from .agents.code_agent import CodeAgent
from .agents.training_agent import TrainingAgent
from .agents.testing_agent import TestingAgent
from .agents.report_agent import ReportAgent
from .agents.safety_controller import SafetyController
from .sandbox import SandboxExecutor
from .config import Config

class SelfLearningAI:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        
        # Initialize components
        self.memory = MemorySystem(self.config.memory.persist_directory)
        self.safety = SafetyController()
        self.sandbox = SandboxExecutor()
        
        # Initialize agents
        self.agents = {
            "research": ResearchAgent(self.memory, self.config.llm.__dict__),
            "code": CodeAgent(self.memory, self.config.llm.__dict__),
            "training": TrainingAgent(self.memory, self.config.llm.__dict__),
            "testing": TestingAgent(self.memory, self.config.llm.__dict__),
            "report": ReportAgent(self.memory, self.config.llm.__dict__),
        }
        
        self.pending_approvals = []

    def set_goal(self, goal: str, priority: str = "medium"):
        """Set a learning goal for the AI"""
        goal_data = self.memory.add_goal(goal, priority)
        self.process_goal(goal_data["id"])
        return goal_data

    def process_goal(self, goal_id: str):
        """Process a goal through the AI pipeline"""
        goals = self.memory.get_goals()
        goal = next((g for g in goals if g["id"] == goal_id), None)
        
        if not goal:
            return {"error": "Goal not found"}
        
        self.memory.update_goal(goal_id, "in_progress", "Started processing")
        
        # Phase 1: Research
        research_results = self.agents["research"].run(goal["goal"])
        self.memory.update_goal(goal_id, "in_progress", f"Research complete: {len(research_results.get('findings', []))} sources")
        
        # Phase 2: Code generation (if needed)
        if "code" in goal["goal"].lower() or "implement" in goal["goal"].lower():
            code_result = self.agents["code"].run(goal["goal"])
            if code_result.get("requires_review"):
                approval_id = self.safety.request_approval(
                    code_result["code"],
                    {"goal": goal["goal"]}
                )
                self.pending_approvals.append(approval_id)
                self.memory.update_goal(goal_id, "pending_approval", f"Code ready, awaiting approval: {approval_id}")
                return {"status": "pending_approval", "approval_id": approval_id}
        
        # Phase 3: Testing
        if "code" in str(locals()):
            test_results = self.agents["testing"].run(goal["goal"], {"target": "generated_code"})
            self.memory.update_goal(goal_id, "in_progress", f"Tests: {test_results['results']['passed']}/{test_results['results']['total']} passed")
        
        # Phase 4: Training (if learning task)
        if "learn" in goal["goal"].lower():
            training_results = self.agents["training"].run(goal["goal"])
            self.memory.update_goal(goal_id, "in_progress", f"Training accuracy: {training_results['evaluation']['accuracy']}")
        
        self.memory.update_goal(goal_id, "completed", "Goal processed successfully")
        return {"status": "completed", "goal": goal}

    def approve_code(self, approval_id: str, approved: bool):
        """Process code approval"""
        if approved:
            self.safety.approve_operation(approval_id)
            return {"status": "approved"}
        else:
            reason = input("Rejection reason: ")
            self.safety.reject_operation(approval_id, reason)
            return {"status": "rejected", "reason": reason}

    def get_report(self, goal_id: Optional[str] = None) -> str:
        """Generate a report"""
        if goal_id:
            return self.agents["report"].progress_report(goal_id)
        return self.agents["report"].daily_summary()

    def learn_topic(self, topic: str):
        """Learn about a specific topic"""
        return self.agents["research"].learn_topic(topic)

    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "pending_approvals": len(self.pending_approvals),
            "active_goals": len([g for g in self.memory.get_goals() if g["status"] == "in_progress"]),
            "memory_items": len(self.memory.short_term) + len(self.memory.long_term),
            "learned_topics": list(self.memory.learned_topics.keys())
        }

def main():
    """Example usage"""
    ai = SelfLearningAI()
    
    # Set a learning goal
    goal = ai.set_goal("Learn about machine learning optimization techniques", "high")
    print(f"Goal set: {goal['goal']}")
    
    # Get daily report
    print(ai.get_report())

if __name__ == "__main__":
    main()