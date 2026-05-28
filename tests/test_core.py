"""
Unit tests for Self-Learning AI
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from memory import MemorySystem
from agents.safety_controller import SafetyController, SafetyRule

class TestMemorySystem:
    def setup_method(self):
        self.memory = MemorySystem("./test_data/memory")

    def test_add_memory(self):
        item = self.memory.add("knowledge", "Test content", {"source": "test"})
        assert item.id is not None
        assert item.content == "Test content"
        assert item.type == "knowledge"

    def test_search_memory(self):
        self.memory.add("knowledge", "Python programming")
        results = self.memory.search("Python")
        assert len(results) > 0

    def test_goals(self):
        goal = self.memory.add_goal("Learn AI", "high")
        assert goal["goal"] == "Learn AI"
        assert goal["priority"] == "high"
        
        goals = self.memory.get_goals()
        assert len(goals) == 1

    def test_update_goal(self):
        goal = self.memory.add_goal("Test goal")
        self.memory.update_goal(goal["id"], "in_progress", "Started")
        
        updated = self.memory.get_goals()[0]
        assert updated["status"] == "in_progress"
        assert len(updated["progress"]) == 1

    def teardown_method(self):
        self.memory.clear()
        import shutil
        if os.path.exists("./test_data"):
            shutil.rmtree("./test_data")

class TestSafetyController:
    def setup_method(self):
        self.safety = SafetyController()

    def test_safe_operation(self):
        result = self.safety.check_operation("print('hello')")
        assert result["safe"] == True

    def test_blocked_operation(self):
        result = self.safety.check_operation("rm -rf /")
        assert result["safe"] == False
        assert len(result["violations"]) > 0

    def test_approval_request(self):
        approval_id = self.safety.request_approval(
            "dangerous_operation",
            {"context": "test"}
        )
        assert approval_id is not None
        
        pending = self.safety.get_pending_approvals()
        assert len(pending) == 1

    def test_approve_operation(self):
        approval_id = self.safety.request_approval("test", {})
        result = self.safety.approve_operation(approval_id)
        assert result == True

    def test_reject_operation(self):
        approval_id = self.safety.request_approval("test", {})
        result = self.safety.reject_operation(approval_id, "Not approved")
        assert result == True

    def test_add_custom_rule(self):
        rule = SafetyRule(
            name="test_rule",
            description="Test safety rule",
            check_function=lambda x: "test" in x,
            severity="low"
        )
        self.safety.add_rule(rule)
        assert len(self.safety.rules) > 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])