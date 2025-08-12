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
        'raw_content': '''User: I need help creating a portfolio website using HTML, CSS, and JavaScript. 
Can you help me build a responsive design that showcases my projects?
