#!/usr/bin/env python3
"""
Quick demo script to show the AUC Archive Chatbot functionality
"""

from auc_archive_chatbot import AUCArchiveChatbot

def run_demo():
    """Run a demonstration of the chatbot."""
    print("🏛️  AUC Archive Chatbot Demo")
    print("=" * 50)
    
    chatbot = AUCArchiveChatbot()
    
    # Initialize
    print("Initializing...")
    if not chatbot.initialize():
        print("❌ Failed to initialize")
        return
    
    # Demo queries
    demo_queries = [
        "list collections",
        "browse p15795coll7", 
        "search revolution",
        "help"
    ]
    
    for query in demo_queries:
        print(f"\n📝 Query: {query}")
        print("🤖 Response:")
        response = chatbot.process_query(query)
        print(response)
        print("\n" + "-" * 50)

if __name__ == "__main__":
    run_demo()