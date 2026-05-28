"""
Testing Agent - Runs tests and validates code
"""

import subprocess
import os
from typing import Dict, Any, Optional, List
from .base import BaseAgent

class TestingAgent(BaseAgent):
    def __init__(self, memory, llm_config: Dict, sandbox_path: str = "./sandbox"):
        super().__init__("TestingAgent", memory, llm_config)
        self.sandbox_path = sandbox_path

    def run(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        self.log(f"Running tests for: {task}")
        
        # Determine what to test
        test_target = context.get("target") if context else task
        
        # Run tests
        results = self._run_tests(test_target)
        
        # Analyze results
        analysis = self._analyze_results(results)
        
        self.save_result({"task": task, "results": results, "analysis": analysis})
        return {"status": "complete", "results": results, "analysis": analysis}

    def _run_tests(self, target: str) -> Dict[str, Any]:
        # Placeholder - would run actual tests
        self.log(f"Executing test suite for: {target}")
        return {
            "passed": 15,
            "failed": 2,
            "skipped": 1,
            "total": 18,
            "duration": 2.5
        }

    def _analyze_results(self, results: Dict) -> Dict[str, Any]:
        failed = results.get("failed", 0)
        passed = results.get("passed", 0)
        total = results.get("total", 1)
        
        pass_rate = (passed / total) * 100 if total > 0 else 0
        
        return {
            "pass_rate": pass_rate,
            "status": "pass" if failed == 0 else "needs_fix",
            "recommendations": [
                f"Fix {failed} failing tests" if failed > 0 else "All tests passing"
            ]
        }

    def test_code_safety(self, code: str) -> Dict[str, Any]:
        """Test if code is safe to execute"""
        self.log("Checking code safety...")
        
        # Check for dangerous patterns
        dangerous_patterns = [
            "os.system(",
            "subprocess.call",
            "eval(",
            "exec(",
            "__import__",
            "open(",
        ]
        
        issues = []
        for pattern in dangerous_patterns:
            if pattern in code:
                issues.append(f"Potential security issue: {pattern}")
        
        return {
            "safe": len(issues) == 0,
            "issues": issues
        }

    def benchmark(self, code: str, inputs: List[Any]) -> Dict[str, Any]:
        """Benchmark code performance"""
        self.log("Running performance benchmarks...")
        
        # Placeholder - would actually benchmark
        return {
            "avg_time_ms": 15.2,
            "min_time_ms": 10.1,
            "max_time_ms": 45.3,
            "iterations": len(inputs)
        }