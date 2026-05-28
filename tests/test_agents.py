"""
Tests for agents
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from memory import MemorySystem
from agents.research_agent import ResearchAgent
from agents.code_agent import CodeAgent
from agents.testing_agent import TestingAgent
from agents.report_agent import ReportAgent

class TestResearchAgent:
    def setup_method(self):
        self.memory = MemorySystem("./test_data/memory")
        self.agent = ResearchAgent(self.memory, {})

    def test_run(self):
        result = self.agent.run("machine learning")
        assert result["status"] == "complete"
        assert "findings" in result

    def test_learn_topic(self):
        result = self.agent.learn_topic("Python")
        assert "topic" in result
        assert result["topic"] == "Python"

    def teardown_method(self):
        self.memory.clear()

class TestCodeAgent:
    def setup_method(self):
        self.memory = MemorySystem("./test_data/memory")
        self.agent = CodeAgent(self.memory, {}, "./test_project")

    def test_safe_task(self):
        result = self.agent.run("print hello world")
        assert result["status"] in ["pending_approval", "blocked"]

    def test_dangerous_task(self):
        result = self.agent.run("rm -rf /")
        assert result["status"] == "blocked"

    def teardown_method(self):
        self.memory.clear()

class TestTestingAgent:
    def setup_method(self):
        self.memory = MemorySystem("./test_data/memory")
        self.agent = TestingAgent(self.memory, {}, "./test_sandbox")

    def test_run(self):
        result = self.agent.run("test suite")
        assert result["status"] == "complete"

    def test_code_safety(self):
        result = self.agent.test_code_safety("print('safe')")
        assert result["safe"] == True

    def test_unsafe_code(self):
        result = self.agent.test_code_safety("os.system('rm -rf')")
        assert result["safe"] == False

    def teardown_method(self):
        self.memory.clear()

class TestReportAgent:
    def setup_method(self):
        self.memory = MemorySystem("./test_data/memory")
        self.agent = ReportAgent(self.memory, {})

    def test_run(self):
        self.memory.add("knowledge", "Test knowledge")
        result = self.agent.run("general report")
        assert result["status"] == "complete"
        assert "report" in result

    def test_daily_summary(self):
        report = self.agent.daily_summary()
        assert "Daily Summary" in report

    def teardown_method(self):
        self.memory.clear()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])