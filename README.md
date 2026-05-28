# Self-Learning AI Agent System (From Scratch)

A controlled autonomous AI agent with a modern web interface that learns from scratch using a Markov Chain algorithm — maintaining safety boundaries and human oversight without any pre-built AI models.

## Features

- **🌐 Web UI**: Modern chat interface for interacting with the AI
- **🧠 Scratch-Built Learning**: Uses a Markov Chain learner that improves from every interaction
- **🎓 Training System**: Manual and scheduled training sessions based on conversation history
- **⚙️ Configurable Settings**: Adjust learning algorithms and training intervals
- **📊 Statistics Dashboard**: Track conversations and learnings
- **🐳 Docker Support**: Easy self-hosting with Docker

## Quick Start

### Manual Setup

```bash
# Install dependencies
pip install flask numpy

# Run the web UI
python app.py
```

### Using Docker

```bash
docker-compose -f docker/docker-compose.web.yml up
```

## Architecture

The system uses a Markov Chain based "Scratch AI" core that tokenizes user input and builds a transition matrix to generate responses. It learns in real-time from every message received.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LEARNING_ALGO` | markov | Learning algorithm |
| `AUTO_TRAIN` | true | Enable auto training |
| `TRAINING_INTERVAL` | 6 | Training interval (hours) |
| `SECRET_KEY` | dev-secret | Flask secret key |
| `PORT` | 5000 | Web server port |

## License

MIT License
