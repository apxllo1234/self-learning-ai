# Deployment Guide

## Local Deployment

### Prerequisites

- Python 3.9+
- pip
- OpenAI API key (or other LLM provider)

### Installation

```bash
git clone <repository>
cd self-learning-ai
pip install -r requirements.txt
```

### Configuration

```bash
export OPENAI_API_KEY="your-key"
python src/main.py
```

## Docker Deployment

### Build Image

```bash
docker build -t self-learning-ai .
```

### Run Container

```bash
docker run -it \
  -e OPENAI_API_KEY="your-key" \
  self-learning-ai python src/main.py
```

## Docker Compose

```yaml
version: '3.8'
services:
  self-learning-ai:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
```

## Production Considerations

1. **Security**: Never expose API keys in logs
2. **Costs**: Set max cost per run in config
3. **Backups**: Regular backup of memory data
4. **Monitoring**: Log all operations for auditing
5. **Approval**: Always require human approval for code changes

## Scaling

For larger deployments:
- Use vector database (ChromaDB/Weaviate)
- Add Redis for queue management
- Implement Celery workers for async tasks
- Add GPU support for training