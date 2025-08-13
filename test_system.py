#!/usr/bin/env python3
"""
GPT Gulp Test Script
Simple test to verify the system is working
"""

import asyncio
import json
import time
from datetime import datetime

from storage.conversation_storage import ConversationStorage
from processors.conversation_processor import ConversationProcessor

import sys
if sys.platform == "win32":
    import os
    os.system('chcp 65001')
    sys.stdout.reconfigure(encoding='utf-8')

async def test_system():
    """Test the GPT Gulp system"""
    print("🧪 Testing GPT Gulp System...")
    
    # Load config
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    
    # Initialize components
    storage = ConversationStorage(config)
    processor = ConversationProcessor(config)
    
    # Create a test conversation
    test_conversation = {
        'id': f"test_{int(time.time())}",
        'platform': 'test',
        'timestamp': datetime.now(),
        'title': 'Test Conversation - Building a Portfolio Website',
        'raw_content': 'User: I need help creating a portfolio website using HTML, CSS, and JavaScript. Can you help me build a responsive design that showcases my projects?\n\nAssistant: I\'d be happy to help you create a responsive portfolio website! Let\'s start with the HTML structure and then add CSS for styling and JavaScript for interactivity.',
        'processed': False
    }
    
    print("✅ Created test conversation")
    
    # Save to storage
    await storage.save_conversation(test_conversation)
    print("✅ Saved conversation to storage")
    
    # Process the conversation
    processed_conversation = await processor.process(test_conversation)
    print("✅ Processed conversation")
    print(f"   Summary: {processed_conversation['summary']}")
    print(f"   Project: {processed_conversation['project']}")
    print(f"   Tags: {processed_conversation['tags']}")
    
    # Save processed version
    await storage.save_processed_conversation(processed_conversation)
    print("✅ Saved processed conversation")
    
    # Get statistics
    stats = await storage.get_storage_stats()
    print("\n📊 Storage Statistics:")
    print(f"   Total conversations: {stats['total_conversations']}")
    print(f"   Processed: {stats['processed_conversations']}")
    print(f"   By platform: {stats['by_platform']}")
    
    print("\n🎉 Test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_system())
