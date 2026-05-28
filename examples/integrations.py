"""
Integration example with external services
"""

from src.main import SelfLearningAI

def setup_with_openai():
    """Setup with OpenAI API"""
    import os
    os.environ["OPENAI_API_KEY"] = "your-key"
    os.environ["LLM_PROVIDER"] = "openai"
    os.environ["LLM_MODEL"] = "gpt-4"
    
    ai = SelfLearningAI()
    return ai

def setup_with_anthropic():
    """Setup with Anthropic (Claude)"""
    import os
    os.environ["ANTHROPIC_API_KEY"] = "your-key"
    os.environ["LLM_PROVIDER"] = "anthropic"
    os.environ["LLM_MODEL"] = "claude-3-sonnet-20240229"
    
    ai = SelfLearningAI()
    return ai

def setup_with_local():
    """Setup with local Ollama"""
    import os
    os.environ["LLM_PROVIDER"] = "local"
    os.environ["LLM_BASE_URL"] = "http://localhost:11434"
    
    ai = SelfLearningAI()
    return ai

def webhook_example():
    """Example webhook integration"""
    import json
    
    ai = SelfLearningAI()
    
    # Simulate webhook payload
    webhook_data = {
        "event": "new_learning_goal",
        "goal": "Learn about transformers",
        "priority": "high"
    }
    
    # Process webhook
    if webhook_data["event"] == "new_learning_goal":
        result = ai.set_goal(
            webhook_data["goal"],
            webhook_data["priority"]
        )
        return {"status": "processed", "goal_id": result["id"]}
    
    return {"status": "unknown_event"}

def scheduled_task_example():
    """Example of scheduled task"""
    ai = SelfLearningAI()
    
    # Daily learning routine
    topics = [
        "machine learning fundamentals",
        "deep learning architectures",
        "natural language processing"
    ]
    
    results = []
    for topic in topics:
        result = ai.learn_topic(topic)
        results.append(result)
    
    # Generate report
    report = ai.get_report()
    
    return {"topics": results, "report": report}

if __name__ == "__main__":
    # Run examples
    print("=== Webhook Example ===")
    print(webhook_example())
    
    print("\n=== Scheduled Task Example ===")
    result = scheduled_task_example()
    print(f"Learned {len(result['topics'])} topics")