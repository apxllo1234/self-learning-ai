"""
Code Generator Agent - Writes and modifies code
"""

import os
from typing import Dict, Any, Optional, List
from .base import BaseAgent

class CodeAgent(BaseAgent):
    def __init__(self, memory, llm_config: Dict, project_root: str = "./project"):
        super().__init__("CodeAgent", memory, llm_config)
        self.project_root = project_root

    def run(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        self.log(f"Generating code for: {task}")
        
        # Check safety constraints
        if not self._check_safety(task):
            return {"status": "blocked", "reason": "Safety check failed"}
        
        # Generate code
        code = self._generate_code(task, context)
        
        # Return code for review (human approval or automated)
        return {
            "status": "pending_approval",
            "code": code,
            "task": task,
            "requires_review": True
        }

    def _check_safety(self, task: str) -> bool:
        """Check if the task violates safety constraints"""
        blocked = ["rm -rf /", "drop database", "sudo", "delete everything"]
        for block in blocked:
            if block in task.lower():
                self.log(f"Safety block: {block} found in task", "warning")
                return False
        return True

    def _generate_code(self, task: str, context: Optional[Dict]) -> str:
        # Placeholder - in production, use LLM to generate code
        return f"# Generated code for: {task}\nprint('Hello from generated code')"

    def implement_feature(self, feature: str, files: List[str]) -> Dict[str, Any]:
        """Implement a specific feature across files"""
        self.log(f"Implementing feature: {feature}")
        
        changes = []
        for file_path in files:
            if os.path.exists(os.path.join(self.project_root, file_path)):
                # Modify existing file
                change = self._modify_file(file_path, feature)
                changes.append({"file": file_path, "change": change})
            else:
                # Create new file
                change = self._create_file(file_path, feature)
                changes.append({"file": file_path, "change": "created"})
        
        self.save_result({"feature": feature, "changes": changes})
        return {"status": "complete", "changes": changes}

    def _modify_file(self, file_path: str, feature: str) -> str:
        # Placeholder for file modification
        return "modified"

    def _create_file(self, file_path: str, feature: str) -> str:
        # Placeholder for file creation
        return "created"

    def refactor(self, code: str, goal: str) -> str:
        """Refactor existing code"""
        self.log(f"Refactoring code for: {goal}")
        return code  # Placeholder - LLM would refactor the code