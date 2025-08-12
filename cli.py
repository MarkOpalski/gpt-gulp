#!/usr/bin/env python3
"""
GPT Gulp CLI Tool
Command-line interface for managing AI conversation archives
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

from main import GPTGulp
from storage.conversation_storage import ConversationStorage

class GPTGulpCLI:
    def __init__(self):
        self.config_path = "config/config.json"
        self.storage = None
        
    def load_config(self):
        """Load configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {self.config_path}")
            return {}
    
    async def start_collection(self):
        """Start conversation collection"""
        print("🚀 Starting GPT Gulp conversation collection...")
        app = GPTGulp(self.config_path)
        await app.run()
    
    async def show_stats(self):
        """Show collection statistics"""
        config = self.load_config()
        storage = ConversationStorage(config)
        stats = await storage.get_storage_stats()
        
        print("📊 GPT Gulp Statistics")
        print("=" * 40)
        print(f"Total conversations: {stats['total_conversations']}")
        print(f"Processed: {stats['processed_conversations']}")
        print(f"Unprocessed: {stats['unprocessed_conversations']}")
        
        print("\n📱 By Platform:")
        for platform, count in stats['by_platform'].items():
            print(f"  {platform}: {count}")
        
        print("\n📁 By Project:")
        for project, count in stats['by_project'].items():
            print(f"  {project}: {count}")
    
    async def list_conversations(self, limit=10):
        """List recent conversations"""
        config = self.load_config()
        storage = ConversationStorage(config)
        conversations = await storage.get_recent_conversations(limit)
        
        print(f"💬 Recent Conversations (Last {len(conversations)})")
        print("=" * 60)
        
        for conv in conversations:
            timestamp = conv['timestamp'].strftime('%Y-%m-%d %H:%M')
            status = "✅" if conv['processed'] else "⏳"
            print(f"{status} [{timestamp}] {conv['platform']} - {conv['title'][:50]}...")
            if conv.get('project') and conv['project'] != 'general':
                print(f"    📁 Project: {conv['project']}")
            if conv.get('tags'):
                print(f"    🏷️  Tags: {', '.join(conv['tags'][:3])}")
            print()
    
    async def export_conversations(self, project=None):
        """Export conversations to Obsidian"""
        config = self.load_config()
        app = GPTGulp(self.config_path)
        storage = ConversationStorage(config)
        
        if project:
            conversations = await storage.get_conversations_by_project(project)
            print(f"📤 Exporting {len(conversations)} conversations for project '{project}'...")
        else:
            conversations = await storage.get_recent_conversations(100)
            print(f"📤 Exporting {len(conversations)} recent conversations...")
        
        for conv in conversations:
            await app.export_to_obsidian(conv)
        
        print("✅ Export complete!")
    
    async def setup_obsidian(self):
        """Set up Obsidian integration"""
        config = self.load_config()
        obsidian_config = config.get('obsidian', {})
        
        vault_path = input(f"Obsidian vault path [{obsidian_config.get('vault_path', '')}]: ").strip()
        if vault_path:
            obsidian_config['vault_path'] = vault_path
        
        ai_folder = input(f"AI conversations folder [{obsidian_config.get('ai_conversations_folder', 'AI Conversations')}]: ").strip()
        if ai_folder:
            obsidian_config['ai_conversations_folder'] = ai_folder
        
        config['obsidian'] = obsidian_config
        
        # Save updated config
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Obsidian configuration updated!")
        
        # Create folders if they don't exist
        vault_path = Path(obsidian_config['vault_path'])
        if vault_path.exists():
            ai_folder_path = vault_path / obsidian_config['ai_conversations_folder']
            ai_folder_path.mkdir(exist_ok=True)
            print(f"📁 Created folder: {ai_folder_path}")

def main():
    parser = argparse.ArgumentParser(description='GPT Gulp - AI Conversation Archive System')
    parser.add_argument('command', choices=[
        'start', 'stats', 'list', 'export', 'setup-obsidian'
    ], help='Command to execute')
    parser.add_argument('--project', help='Filter by project name')
    parser.add_argument('--limit', type=int, default=10, help='Limit number of results')
    
    args = parser.parse_args()
    
    cli = GPTGulpCLI()
    
    if args.command == 'start':
        asyncio.run(cli.start_collection())
    elif args.command == 'stats':
        asyncio.run(cli.show_stats())
    elif args.command == 'list':
        asyncio.run(cli.list_conversations(args.limit))
    elif args.command == 'export':
        asyncio.run(cli.export_conversations(args.project))
    elif args.command == 'setup-obsidian':
        asyncio.run(cli.setup_obsidian())

if __name__ == "__main__":
    main()
