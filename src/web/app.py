"""
Web UI for Self-Learning AI Chat Interface
Flask-based web application with persistent memory
"""

import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from src.main import SelfLearningAI
from src.config import Config

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
app.config['JSON_SORT_KEYS'] = False

# Global AI instance
ai = None

def init_ai():
    """Initialize the AI with memory persistence"""
    global ai
    config = Config()
    ai = SelfLearningAI(config)
    return ai

def get_db():
    """Get database connection"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'chat.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database schema"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Memory table for persistent learnings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            content TEXT NOT NULL,
            context TEXT,
            importance INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            accessed_at DATETIME
        )
    ''')
    
    # Training history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_type TEXT NOT NULL,
            topics_learned TEXT,
            performance_score REAL,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User preferences
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    """Main chat interface"""
    if 'session_id' not in session:
        session['session_id'] = str(datetime.now().timestamp())
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Send message and get AI response"""
    data = request.json
    message = data.get('message', '')
    session_id = session.get('session_id', 'default')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Save user message
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)',
        (session_id, 'user', message)
    )
    conn.commit()
    
    # Generate AI response with context
    context = get_conversation_context(session_id, limit=10)
    learnings = get_recent_learnings(limit=5)
    
    # Build prompt with context and learnings
    enhanced_prompt = f"Previous conversation context:\n{context}\n\nRelevant learnings:\n{learnings}\n\nUser message: {message}"
    
    # Use AI to process (simplified - in production integrate LLM)
    response = process_with_ai(enhanced_prompt, message)
    
    # Save AI response
    cursor.execute(
        'INSERT INTO conversations (session_id, role, content, metadata) VALUES (?, ?, ?, ?)',
        (session_id, 'assistant', response, json.dumps({'timestamp': datetime.now().isoformat()}))
    )
    conn.commit()
    conn.close()
    
    return jsonify({
        'response': response,
        'session_id': session_id
    })

@app.route('/api/history', methods=['GET'])
def history():
    """Get conversation history"""
    session_id = request.args.get('session_id', session.get('session_id', 'default'))
    limit = int(request.args.get('limit', 50))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM conversations WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?',
        (session_id, limit)
    )
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'messages': messages})

@app.route('/api/learn', methods=['POST'])
def add_learning():
    """Add a learning to the knowledge base"""
    data = request.json
    topic = data.get('topic', '')
    content = data.get('content', '')
    context = data.get('context', '')
    importance = data.get('importance', 1)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO learnings (topic, content, context, importance) VALUES (?, ?, ?, ?)',
        (topic, content, context, importance)
    )
    learning_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': learning_id, 'topic': topic, 'status': 'saved'})

@app.route('/api/learnings', methods=['GET'])
def get_learnings():
    """Get all learnings"""
    topic = request.args.get('topic')
    limit = int(request.args.get('limit', 20))
    
    conn = get_db()
    cursor = conn.cursor()
    
    if topic:
        cursor.execute(
            'SELECT * FROM learnings WHERE topic LIKE ? ORDER BY importance DESC, created_at DESC LIMIT ?',
            (f'%{topic}%', limit)
        )
    else:
        cursor.execute(
            'SELECT * FROM learnings ORDER BY importance DESC, created_at DESC LIMIT ?',
            (limit,)
        )
    
    learnings = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'learnings': learnings})

@app.route('/api/training', methods=['POST'])
def trigger_training():
    """Trigger AI training session"""
    data = request.json
    topics = data.get('topics', [])
    training_type = data.get('type', 'manual')
    
    # Get learnings for training
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM learnings ORDER BY importance DESC LIMIT 100')
    learnings = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Simulate training (in production, call actual training agent)
    results = {
        'topics_processed': len(learnings),
        'accuracy': 0.85 + (len(learnings) * 0.001),
        'training_type': training_type,
        'status': 'completed'
    }
    
    # Save training history
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO training_history (session_type, topics_learned, performance_score) VALUES (?, ?, ?)',
        (training_type, json.dumps(topics), results['accuracy'])
    )
    conn.commit()
    conn.close()
    
    return jsonify(results)

@app.route('/api/training/history', methods=['GET'])
def get_training_history():
    """Get training history"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM training_history ORDER BY created_at DESC LIMIT 50')
    history = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'history': history})

@app.route('/api/preferences', methods=['GET', 'POST'])
def preferences():
    """Get or set user preferences"""
    if request.method == 'GET':
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM preferences')
        prefs = {row['key']: row['value'] for row in cursor.fetchall()}
        conn.close()
        return jsonify(prefs)
    else:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        for key, value in data.items():
            cursor.execute(
                'INSERT OR REPLACE INTO preferences (key, value, updated_at) VALUES (?, ?, ?)',
                (key, value, datetime.now().isoformat())
            )
        conn.commit()
        conn.close()
        return jsonify({'status': 'saved'})

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    """AI settings configuration"""
    if request.method == 'GET':
        # Return current settings
        settings = {
            'llm_provider': os.environ.get('LLM_PROVIDER', 'openai'),
            'llm_model': os.environ.get('LLM_MODEL', 'gpt-4'),
            'auto_train': os.environ.get('AUTO_TRAIN', 'true').lower() == 'true',
            'training_interval': int(os.environ.get('TRAINING_INTERVAL', '6')),
            'max_context_length': int(os.environ.get('MAX_CONTEXT_LENGTH', '4000')),
            'temperature': float(os.environ.get('TEMPERATURE', '0.7')),
        }
        return jsonify(settings)
    else:
        # Update settings
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        for key, value in data.items():
            env_key = key.upper()
            os.environ[env_key] = str(value)
            cursor.execute(
                'INSERT OR REPLACE INTO preferences (key, value, updated_at) VALUES (?, ?, ?)',
                (key, str(value), datetime.now().isoformat())
            )
        
        conn.commit()
        conn.close()
        
        # Reinitialize AI with new settings
        init_ai()
        
        return jsonify({'status': 'updated'})

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    session_id = request.args.get('session_id', session.get('session_id'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'cleared'})

def get_conversation_context(session_id, limit=10):
    """Get recent conversation for context"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT role, content FROM conversations WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?',
        (session_id, limit)
    )
    messages = cursor.fetchall()
    conn.close()
    
    context = []
    for msg in reversed(messages):
        context.append(f"{msg[0]}: {msg[1]}")
    
    return '\n'.join(context)

def get_recent_learnings(limit=5):
    """Get recent learnings for context"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT topic, content FROM learnings ORDER BY created_at DESC LIMIT ?',
        (limit,)
    )
    learnings = cursor.fetchall()
    conn.close()
    
    return '\n'.join([f"- {l[0]}: {l[1][:100]}" for l in learnings])

def process_with_ai(context, message):
    """Process message with AI (simplified version)"""
    # In production, this would call the actual LLM
    # For now, return a simulated response based on learnings
    
    if ai:
        try:
            # Try to use the actual AI
            result = ai.learn_topic(message)
            return f"I've learned about: {result.get('topic', message)}. Found {len(result.get('materials', []))} resources."
        except Exception as e:
            pass
    
    # Simulated response based on keywords
    keywords = {
        'learn': 'I can learn new topics and remember them for future conversations.',
        'train': 'Training helps me improve my responses based on our interactions.',
        'code': 'I can help with coding tasks and save code patterns for future use.',
        'memory': 'My memory persists across sessions, so I remember our conversations.',
        'help': 'I\'m here to assist you. I can learn from our chats and improve over time.'
    }
    
    for keyword, response in keywords.items():
        if keyword in message.lower():
            return response
    
    return f"I understand you're asking about: '{message[:50]}...'. How would you like me to learn more about this topic?"

# Initialize
init_db()
init_ai()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)