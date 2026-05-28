# Web UI for Self-Learning AI

A Flask-based web interface for chatting with and training the AI.

## Features

- **Chat Interface**: Real-time conversation with persistent memory
- **Learning System**: AI learns from conversations and stores knowledge
- **Training Sessions**: Manual or scheduled training with progress tracking
- **Settings Panel**: Configure AI provider, model, temperature, and training intervals
- **Statistics Dashboard**: Track conversations, learnings, and training sessions
- **Persistent Storage**: SQLite database stores all conversations and learnings

## Installation

```bash
pip install flask
```

## Running

```bash
# Development
cd src/web
flask run --host 0.0.0.0 --port 5000

# Production
export FLASK_DEBUG=false
python app.py
```

Or use Docker:

```bash
docker-compose up
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | dev-secret | Flask secret key |
| `PORT` | 5000 | Server port |
| `FLASK_DEBUG` | false | Enable debug mode |
| `OPENAI_API_KEY` | - | OpenAI API key |
| `LLM_PROVIDER` | openai | AI provider (openai/anthropic/local) |
| `LLM_MODEL` | gpt-4 | Model name |
| `AUTO_TRAIN` | true | Enable auto training |
| `TRAINING_INTERVAL` | 6 | Training interval in hours |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Send message and get AI response |
| `/api/history` | GET | Get conversation history |
| `/api/learn` | POST | Add a learning |
| `/api/learnings` | GET | Get all learnings |
| `/api/training` | POST | Trigger training session |
| `/api/training/history` | GET | Get training history |
| `/api/settings` | GET/POST | Get/set AI settings |
| `/api/preferences` | GET/POST | Get/set user preferences |
| `/api/clear` | POST | Clear conversation history |

## Database

SQLite database stored at `data/chat.db` with tables:

- `conversations`: Chat messages with session tracking
- `learnings`: Knowledge base with topics and content
- `training_history`: Record of training sessions
- `preferences`: User settings and configuration