# API Reference

## SelfLearningAI

Main class for the self-learning AI system.

### Constructor

```python
SelfLearningAI(config: Optional[Config] = None)
```

### Methods

#### set_goal(goal: str, priority: str = "medium") -> Dict

Set a learning goal for the AI.

```python
goal = ai.set_goal("Learn about ML", priority="high")
```

#### process_goal(goal_id: str) -> Dict

Process a goal through the AI pipeline.

#### approve_code(approval_id: str, approved: bool) -> Dict

Approve or reject pending code changes.

```python
ai.approve_code("approval_1", approved=True)
```

#### get_report(goal_id: Optional[str] = None) -> str

Generate a progress report.

```python
report = ai.get_report()  # Daily summary
report = ai.get_report("goal_123")  # Specific goal
```

#### learn_topic(topic: str) -> Dict

Learn about a specific topic.

```python
result = ai.learn_topic("reinforcement learning")
```

#### get_status() -> Dict

Get current system status.

```python
status = ai.get_status()
```

## MemorySystem

Memory storage and retrieval.

### Methods

#### add(type: str, content: str, metadata: Optional[Dict] = None) -> MemoryItem

Add an item to memory.

#### search(query: str, limit: int = 10) -> List[MemoryItem]

Search memory for relevant items.

#### get_goals() -> List[Dict]

Get all active goals.

#### add_goal(goal: str, priority: str = "medium") -> Dict

Add a new goal.

#### update_goal(goal_id: str, status: str, progress: str) -> Dict

Update goal progress.

## SafetyController

Safety enforcement and approval management.

### Methods

#### check_operation(operation: str) -> Dict

Check if an operation is safe.

#### request_approval(operation: str, context: Dict) -> str

Request human approval for an operation.

#### approve_operation(approval_id: str) -> bool

Approve a pending operation.

#### reject_operation(approval_id: str, reason: str = "") -> bool

Reject a pending operation.

#### get_pending_approvals() -> List[Dict]

Get all pending approvals.

## SandboxExecutor

Secure code execution.

### Methods

#### execute_code(code: str, language: str = "python") -> Dict

Execute code in sandbox.

#### test_file(file_path: str) -> Dict

Test an existing file.

#### cleanup() -> None

Clean up sandbox directory.