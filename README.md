# Self-Learning AI Agent System

A controlled autonomous AI agent that can learn, research, code, test, and report — while maintaining safety boundaries and human oversight.

## Features

- **Self-Learning Memory**: Persistent memory system that consolidates short-term and long-term knowledge
- **Multi-Agent System**: Specialized agents for research, coding, training, testing, and reporting
- **Safety Controller**: Built-in safety checks and human approval gates
- **Sandboxed Execution**: Code runs in isolated sandbox environment
- **Goal Management**: Set learning goals and track progress
- **Progress Reports**: Generate detailed reports on AI activities

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Main Orchestrator                        │
└─────────────────────────────────────────────────────────────┘
         │           │           │           │
         ▼           ▼           ▼           ▼
   ┌──────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
   │ Research │ │  Code  │ │Training│ │  Report  │
   │  Agent   │ │  Agent │ │  Agent │ │  Agent   │
   └──────────┘ └────────┘ └────────┘ └──────────┘
         │           │           │           │
         └───────────┴───────────┴───────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Memory System                             │
│  (Short-term + Long-term + Goals + Learned Topics)         │
└─────────────────────────────────────────────────────────────┘
```

## Agents

| Agent | Purpose |
|-------|---------|
| ResearchAgent | Searches web, finds learning resources, analyzes information |
| CodeAgent | Generates and modifies code with safety checks |
| TrainingAgent | Trains models and improves performance |
| TestingAgent | Runs tests and validates code safety |
| ReportAgent | Generates progress reports and summaries |
| SafetyController | Enforces safety rules and manages approvals |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.main import SelfLearningAI

# Initialize the AI
ai = SelfLearningAI()

# Set a learning goal
goal = ai.set_goal("Learn about machine learning", priority="high")

# Learn a topic
result = ai.learn_topic("reinforcement learning")

# Get a report
report = ai.get_report()

# Check status
status = ai.get_status()
print(status)
```

## Configuration

Set environment variables or modify `src/config/__init__.py`:

```python
export OPENAI_API_KEY="your-api-key"
export LLM_PROVIDER="openai"  # or "anthropic", "local"
export LLM_MODEL="gpt-4"
export VECTOR_DB="chroma"  # or "weaviate"
```

## Safety Features

- **Sandboxed code execution** - Code runs in isolated environment
- **Human approval gates** - Critical operations require approval
- **Safety rules** - Blocks dangerous commands and operations
- **Cost controls** - Limits API spending
- **Rollback capability** - Can revert changes through git

## Development

```bash
# Run tests
pytest tests/

# Run with Docker
docker-compose up
```

## Docker

```bash
# Build image
docker build -t self-learning-ai .

# Run container
docker run -it self-learning-ai python src/main.py
```

## Roadmap

- [ ] Add vector database integration (ChromaDB/Weaviate)
- [ ] Implement web search integration (Tavily/SerpAPI)
- [ ] Add local LLM support (Ollama)
- [ ] Create web dashboard
- [ ] Add Git-based version control for code changes
- [ ] Implement reinforcement learning feedback loop
- [ ] Add more sophisticated evaluation metrics

## License

MIT License

## Acknowledgments

Built based on concepts from LangGraph, CrewAI, and OpenDevin.