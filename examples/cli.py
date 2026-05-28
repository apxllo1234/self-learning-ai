"""
CLI Interface for Self-Learning AI
"""

import sys
from src.main import SelfLearningAI

def main():
    ai = SelfLearningAI()
    print("Self-Learning AI CLI")
    print("Type 'help' for commands\n")
    
    while True:
        try:
            command = input("> ").strip()
            
            if command == "quit" or command == "exit":
                print("Goodbye!")
                break
            elif command == "help":
                print_help()
            elif command == "status":
                print_status(ai)
            elif command.startswith("goal "):
                goal_text = command[5:]
                set_goal(ai, goal_text)
            elif command == "report":
                print_report(ai)
            elif command.startswith("learn "):
                topic = command[6:]
                learn_topic(ai, topic)
            elif command == "pending":
                print_pending(ai)
            elif command.startswith("approve "):
                approval_id = command[8:]
                approve_code(ai, approval_id, True)
            elif command.startswith("reject "):
                approval_id = command[7:]
                approve_code(ai, approval_id, False)
            else:
                print("Unknown command. Type 'help' for available commands.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def print_help():
    print("""
Available Commands:
  goal <text>     - Set a learning goal
  learn <topic>   - Learn about a topic
  report          - Generate daily report
  status          - Show system status
  pending         - Show pending approvals
  approve <id>    - Approve code change
  reject <id>     - Reject code change
  help            - Show this help
  quit            - Exit the CLI
""")

def set_goal(ai, text):
    goal = ai.set_goal(text)
    print(f"Goal set: {goal['goal']} (ID: {goal['id']})")

def print_status(ai):
    status = ai.get_status()
    print("\n=== System Status ===")
    for key, value in status.items():
        print(f"  {key}: {value}")

def print_report(ai):
    report = ai.get_report()
    print(report)

def learn_topic(ai, topic):
    result = ai.learn_topic(topic)
    print(f"Learning {topic}...")
    print(f"  Materials: {len(result.get('materials', []))}")
    print(f"  Resources: {len(result.get('resources', []))}")

def print_pending(ai):
    pending = ai.safety.get_pending_approvals()
    if not pending:
        print("No pending approvals")
    else:
        print("\n=== Pending Approvals ===")
        for p in pending:
            print(f"  ID: {p['id']}")
            print(f"  Operation: {p['operation'][:50]}...")
            print()

def approve_code(ai, approval_id, approved):
    result = ai.approve_code(approval_id, approved)
    print(f"Code {result['status']}")

if __name__ == "__main__":
    main()