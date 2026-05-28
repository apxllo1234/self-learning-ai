# Self-Learning AI Agent System

A controlled autonomous AI agent with a modern web interface that learns, researches, codes, tests, and reports — while maintaining safety boundaries and human oversight.

## Features

- **🌐 Web UI**: Modern chat interface for interacting with the AI
- **🧠 Self-Learning Memory**: Persistent memory system that consolidates short-term and long-term knowledge
- **🎓 Training System**: Manual and scheduled training sessions with progress tracking
- **⚙️ Configurable Settings**: Adjust AI provider, model, temperature, and training intervals
- **📊 Statistics Dashboard**: Track conversations, learnings, and training progress
- **🔒 Safety Controller**: Built-in safety checks and human approval gates
- **🐳 Docker Support**: Easy self-hosting with Docker
- **⏰ Auto Training**: GitHub Actions workflow for continuous learning

## Quick Start

### Using Docker (Recommended)

```bash
# Pull and run
docker-compose -f docker/docker-compose.web.yml up

# Access at http://localhost:5000
```

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web UI
cd src/web
flask run --host 0.0.0.0 --port 5000

# Or run the main CLI
python src/main.py
```

## Web UI Features

### Chat Interface
- Real-time conversation with AI
- Persistent memory across sessions
- Learning from every interaction

### Settings Panel
- **AI Provider**: OpenAI, Anthropic, or Local (Ollama)
- **Model**: Choose your preferred model
- **Temperature**: Adjust creativity level
- **Auto Training**: Enable/disable automatic training
- **Training Interval**: How often to train (hours)

### Training Sessions
- Manual training trigger
- Progress visualization
- Performance tracking
- Learning history

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Web UI (Flask)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│  │   Chat      │  │  Settings    │  │    Training       │  │
│  │   Interface  │  │  Panel      │  │    Sessions       │  │
│  └─────────────┘  └─────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Server                               │
│  /api/chat | /api/learn | /api/training | /api/settings    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     SQLite Database                          │
│  (conversations, learnings, training_history, preferences)  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     AI Core (SelfLearningAI)                 │
│  ├── Agents (Research, Code, Training, Testing, Report)     │
│  └── Memory System (Short-term + Long-term)                 │
└─────────────────────────────────────────────────────────────┘
```

## GitHub Actions Auto-Training

The repository includes workflows that run training automatically:

- **train.yml**: Daily training at 2 AM UTC + manual trigger
- **learn.yml**: Continuous learning every 6 hours

Set `OPENAI_API_KEY` in GitHub Secrets to enable automatic training.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | Your API key |
| `LLM_PROVIDER` | openai | AI provider |
| `LLM_MODEL` | gpt-4 | Model name |
| `AUTO_TRAIN` | true | Enable auto training |
| `TRAINING_INTERVAL` | 6 | Training interval (hours) |
| `SECRET_KEY` | dev-secret | Flask secret key |
| `PORT` | 5000 | Web server port |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Send message, get AI response |
| `/api/history` | GET | Get conversation history |
| `/api/learn` | POST | Add a learning |
| `/api/learnings` | GET | Get all learnings |
| `/api/training` | POST | Trigger training session |
| `/api/training/history` | GET | Get training history |
| `/api/settings` | GET/POST | Get/set AI settings |
| `/api/clear` | POST | Clear conversation history |

## Self-Hosting Guide

### Basic VPS Setup

```bash
# SSH into your VPS
ssh user@your-server

# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone your repo
git clone https://github.com/apxllo1234/self-learning-ai.git
cd self-learning-ai

# Create .env file
echo "OPENAI_API_KEY=your-key" > .env
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

# Run with Docker
docker-compose -f docker/docker-compose.web.yml up -d

# Access at http://your-server-ip:5000
```

## License

MIT License
