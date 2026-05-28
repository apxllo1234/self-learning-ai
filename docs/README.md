# Self-Learning AI - Deployment Guide

## Option 1: GitHub Pages (Frontend Only) ⚠️

GitHub Pages can only serve static files - **no backend server**.

### What You Get
- ✅ Beautiful chat interface
- ✅ Settings panel
- ✅ Statistics dashboard

### What You DON'T Get (without backend)
- ❌ AI responses
- ❌ Memory persistence
- ❌ Training sessions
- ❌ Learnings storage

### To Make It Work

**You need a separate backend server.** You have two options:

#### Option A: Run Backend on Your Computer
```bash
# 1. Run the backend
cd self-learning-ai
pip install -r requirements.txt
python -m src.web.app

# 2. Open docs/index.html in your browser
# The UI will connect to localhost:5000
```

#### Option B: Deploy Backend to Cloud
Deploy to Render, Railway, or any cloud platform:
```bash
# Use Render.com (free tier available)
# Point to src/web/app.py
# Set PORT environment variable
```

Then change the API URL in the Settings panel to your deployed backend URL.

---

## Option 2: Self-Host with Docker (Recommended) ✅

This runs everything - frontend + backend + database.

### On Your VPS/Server

```bash
# SSH into your server
ssh user@your-server

# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone the repo
git clone https://github.com/apxllo1234/self-learning-ai.git
cd self-learning-ai

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your-openai-key-here
SECRET_KEY=$(openssl rand -hex 32)
EOF

# Start the server
docker-compose -f docker/docker-compose.web.yml up -d

# Access at http://your-server-ip:5000
```

### On Render.com (Free Tier)

1. Create account at render.com
2. New → Web Service
3. Connect your GitHub repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m src.web.app`
   - **Environment Variables:** Add `OPENAI_API_KEY`
5. Deploy!

Access at: `https://your-app.onrender.com`

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Pages                              │
│                    (docs/index.html)                         │
│                         │                                   │
│              ┌──────────┴──────────┐                       │
│              │                     │                       │
│         Static UI            Settings Panel                  │
│         (HTML/CSS/JS)         (API URL config)               │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ API Calls
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend Server                            │
│                    (Flask + SQLite)                         │
│                         │                                   │
│              ┌──────────┴──────────┐                       │
│              │                     │                       │
│         AI Core              Database                       │
│     (SelfLearningAI)         (learnings,                    │
│                              conversations,                  │
│                              training_history)               │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ (Optional)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    OpenAI API                                │
│                    (or Claude/Ollama)                        │
└─────────────────────────────────────────────────────────────┘
```

## Quick Comparison

| Feature | GitHub Pages Only | Docker Self-Host |
|---------|------------------|------------------|
| Cost | Free | VPS (~$5/mo) |
| Setup | Easy | Medium |
| AI Responses | ❌ Need backend | ✅ Works |
| Memory | ❌ Need backend | ✅ Works |
| Training | ❌ Need backend | ✅ Works |
| Your Data | None | All on your server |

## Recommended Setup

1. **For Testing**: Open `docs/index.html` locally with backend running
2. **For Production**: Use Docker on a VPS or deploy to Render

The `docs/index.html` file is designed to work with both scenarios - it just needs the API URL configured in the Settings panel.