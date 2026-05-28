"""
Example: Using the Self-Learning AI
"""

from src.main import SelfLearningAI

def main():
    # Initialize the AI
    print("Initializing Self-Learning AI...")
    ai = SelfLearningAI()
    
    # Example 1: Set a learning goal
    print("\n=== Setting Learning Goal ===")
    goal = ai.set_goal(
        "Learn about reinforcement learning algorithms",
        priority="high"
    )
    print(f"Goal created: {goal['goal']}")
    print(f"Goal ID: {goal['id']}")
    
    # Example 2: Learn a specific topic
    print("\n=== Learning Topic ===")
    result = ai.learn_topic("neural networks")
    print(f"Topic: {result['topic']}")
    print(f"Materials found: {len(result.get('materials', []))}")
    
    # Example 3: Get current status
    print("\n=== System Status ===")
    status = ai.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Example 4: Generate a report
    print("\n=== Daily Report ===")
    report = ai.get_report()
    print(report)
    
    # Example 5: Goal-specific report
    print("\n=== Goal Progress Report ===")
    goal_report = ai.get_report(goal['id'])
    print(goal_report)

if __name__ == "__main__":
    main()