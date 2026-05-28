"""
Report Agent - Generates reports and communicates with user
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from .base import BaseAgent

class ReportAgent(BaseAgent):
    def __init__(self, memory, llm_config: Dict):
        super().__init__("ReportAgent", memory, llm_config)

    def run(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        self.log(f"Generating report: {task}")
        
        # Gather data from memory
        report_data = self._gather_report_data(task)
        
        # Generate report
        report = self._generate_report(report_data, task)
        
        return {"status": "complete", "report": report}

    def _gather_report_data(self, task: str) -> Dict[str, Any]:
        """Gather relevant data for the report"""
        memories = self.memory.search(task, limit=50)
        goals = self.memory.get_goals()
        
        return {
            "memories": [m.content for m in memories],
            "goals": goals,
            "learned_topics": self.memory.learned_topics,
            "timestamp": datetime.now().isoformat()
        }

    def _generate_report(self, data: Dict, task: str) -> str:
        """Generate a formatted report"""
        report = f"""
# Self-Learning AI Report
Generated: {data['timestamp']}
Topic: {task}

## Summary
- Memories analyzed: {len(data['memories'])}
- Active goals: {len(data['goals'])}
- Topics learned: {len(data['learned_topics'])}

## Goals Progress
"""
        for goal in data['goals']:
            report += f"- [{goal['status'].upper()}] {goal['goal']} (Priority: {goal['priority']})\n"
        
        report += """
## Learned Topics
"""
        for topic, resources in data['learned_topics'].items():
            report += f"- {topic}: {len(resources)} resources\n"
        
        report += """
## Recent Activity
"""
        for memory in data['memories'][:10]:
            report += f"- {memory}\n"
        
        return report

    def daily_summary(self) -> str:
        """Generate daily summary report"""
        self.log("Generating daily summary")
        
        all_data = self.memory.get_all()
        
        report = f"""
# Daily Summary - {datetime.now().strftime('%Y-%m-%d')}

## System Status
- Short-term memories: {len(all_data['short_term'])}
- Long-term memories: {len(all_data['long_term'])}
- Active goals: {len(all_data['goals'])}

## In Progress
"""
        for goal in all_data['goals']:
            if goal['status'] in ['pending', 'in_progress']:
                report += f"- {goal['goal']}\n"
        
        return report

    def progress_report(self, goal_id: str) -> str:
        """Generate progress report for a specific goal"""
        goals = self.memory.get_goals()
        for goal in goals:
            if goal['id'] == goal_id:
                report = f"""
# Progress Report: {goal['goal']}

Status: {goal['status']}
Priority: {goal['priority']}
Created: {goal['created_at']}

## Progress Updates
"""
                for update in goal.get('progress', []):
                    report += f"- [{update['timestamp']}] {update['update']}\n"
                
                return report
        
        return "Goal not found"