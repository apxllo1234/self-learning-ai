# Architecture Documentation

## System Overview

The Self-Learning AI consists of:

1. **Main Orchestrator** - Coordinates all agents and manages workflow
2. **Memory System** - Stores knowledge, goals, and learning progress
3. **Agent System** - Specialized agents for different tasks
4. **Safety Controller** - Enforces safety rules and approval gates
5. **Sandbox Executor** - Safely runs generated code

## Component Details

### Main Orchestrator

Controls the flow between agents:

```
User Input → Orchestrator → Research → Code → Test → Train → Report
                   ↓
              Safety Check
                   ↓
              Memory System
```

### Memory System

Implements three-tier memory:

1. **Short-term**: Recent context (max 20 items)
2. **Long-term**: Consolidated important memories
3. **Goals**: Active objectives with progress tracking

### Agents

Each agent has:
- **run()**: Main execution method
- **think()**: LLM interaction
- **log()**: Activity logging
- **save_result()**: Memory storage

### Safety Controller

Enforces rules:
- Blocks destructive commands
- Requires approval for high-risk operations
- Logs all violations

### Sandbox Executor

- Validates code safety
- Runs in isolated environment
- Enforces timeouts
- Cleans up after execution

## Data Flow

```
1. User sets goal
2. Orchestrator creates goal in memory
3. Research agent gathers information
4. Code agent generates solution (pending approval)
5. Testing agent validates in sandbox
6. Training agent improves models (if needed)
7. Report agent summarizes results
8. User receives report
```

## Configuration

See `src/config/__init__.py` for all configuration options.