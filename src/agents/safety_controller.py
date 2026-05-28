"""
Safety Controller - Ensures safe operation of the AI system
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
import json

@dataclass
class SafetyRule:
    name: str
    description: str
    check_function: Callable[[str], bool]
    severity: str  # low, medium, high, critical

class SafetyController:
    def __init__(self):
        self.rules: List[SafetyRule] = []
        self.blocked_operations: List[str] = []
        self.approval_queue: List[Dict] = []
        self._setup_default_rules()

    def _setup_default_rules(self):
        """Set up default safety rules"""
        self.rules = [
            SafetyRule(
                name="no_destructive_commands",
                description="Block dangerous shell commands",
                check_function=lambda x: not any(d in x.lower() for d in ["rm -rf", "drop", "delete all"]),
                severity="critical"
            ),
            SafetyRule(
                name="no_system_modifications",
                description="Block system-level modifications",
                check_function=lambda x: "sudo" not in x.lower(),
                severity="high"
            ),
            SafetyRule(
                name="cost_limit",
                description="Limit API costs",
                check_function=lambda x: True,  # Placeholder for cost checking
                severity="medium"
            ),
        ]

    def check_operation(self, operation: str) -> Dict[str, Any]:
        """Check if an operation is safe"""
        violations = []
        
        for rule in self.rules:
            if not rule.check_function(operation):
                violations.append({
                    "rule": rule.name,
                    "severity": rule.severity,
                    "description": rule.description
                })
        
        is_safe = len(violations) == 0
        
        return {
            "safe": is_safe,
            "violations": violations,
            "requires_approval": any(v["severity"] in ["high", "critical"] for v in violations)
        }

    def request_approval(self, operation: str, context: Dict) -> str:
        """Request human approval for an operation"""
        approval_id = f"approval_{len(self.approval_queue)}_{hash(operation) % 10000}"
        
        self.approval_queue.append({
            "id": approval_id,
            "operation": operation,
            "context": context,
            "status": "pending"
        })
        
        return approval_id

    def approve_operation(self, approval_id: str) -> bool:
        """Approve a pending operation"""
        for item in self.approval_queue:
            if item["id"] == approval_id:
                item["status"] = "approved"
                return True
        return False

    def reject_operation(self, approval_id: str, reason: str = "") -> bool:
        """Reject a pending operation"""
        for item in self.approval_queue:
            if item["id"] == approval_id:
                item["status"] = "rejected"
                item["rejection_reason"] = reason
                return True
        return False

    def get_pending_approvals(self) -> List[Dict]:
        """Get all pending approval requests"""
        return [item for item in self.approval_queue if item["status"] == "pending"]

    def add_rule(self, rule: SafetyRule):
        """Add a custom safety rule"""
        self.rules.append(rule)

    def log_violation(self, operation: str, violations: List[Dict]):
        """Log safety violations"""
        log_entry = {
            "timestamp": str(datetime.now()),
            "operation": operation,
            "violations": violations
        }
        print(f"[SAFETY] Blocked: {operation}")
        print(f"[SAFETY] Violations: {json.dumps(violations, indent=2)}")

from datetime import datetime