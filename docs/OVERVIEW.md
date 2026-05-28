# Self Learning AI

*Self-modifying AI agent system with memory, learning, and safety controls*

## Quick Links

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Safety](#safety)
- [Configuration](#configuration)
- [Development](#development)

## Overview

This is a controlled autonomous AI system that can:
- Learn from new data and experiences
- Research topics on the web
- Generate and modify code
- Train and improve itself
- Run tests and validate changes
- Report progress to you

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main system
python src/main.py
```

## Architecture

### Agents

| Agent | Description |
|-------|-------------|
| ResearchAgent | Searches the web and finds learning resources |
| CodeAgent | Generates and modifies code with safety checks |
| TrainingAgent | Trains models and improves performance |
| TestingAgent | Runs tests in sandboxed environment |
| ReportAgent | Generates progress reports |

### Memory System

- **Short-term**: Current context and recent learnings
- **Long-term**: Consolidated knowledge and experiences
- **Goals**: Active objectives and their progress

## Safety

The system includes multiple safety layers:

1. **Safety Controller**: Blocks dangerous operations
2. **Human Approval**: Critical changes require approval
3. **Sandboxed Execution**: Code runs in isolated environment
4. **Cost Controls**: Limits API spending

## Configuration

Configure via environment variables:

```bash
export OPENAI_API_KEY="your-key"
export LLM_PROVIDER="openai"
export LLM_MODEL="gpt-4"
```

## Development

```bash
# Run tests
pytest tests/

# Docker
docker-compose up
```

## Usage Example

```python
from src.main import SelfLearningAI

ai = SelfLearningAI()
ai.set_goal("Learn about AI safety")
report = ai.get_report()
```