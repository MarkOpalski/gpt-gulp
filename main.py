"""
GPT Gulp - AI Conversation Archive System
Main application entry point
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from collectors.vscode_collector import VSCodeCollector
from collectors.browser_collector import BrowserCollector
from processors.conversation_processor import ConversationProcessor
from storage.conversation_storage import ConversationStorage

class GPTGulp:
    def __init__(self, config_path: str = "config/config.json"):
        self.config = self._load_config(config_path)
        self.collectors = {}
        self.processor = ConversationProcessor(self.config)
        self.storage = ConversationStorage(self.config)
        self.setup_logging()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Config file not found: {config_path}")
            return {}
    
    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gpt-gulp.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize_collectors(self):
        """Initialize all enabled collectors"""
        platforms = self.config.get('platforms', {})
        
        if platforms.get('vscode', {}).get('enabled'):
            self.collectors['vscode'] = VSCodeCollector(self.config)
            
        browser_platforms = ['claude_ai', 'chatgpt', 'gemini', 'perplexity']
        browser_configs = {k: v for k, v in platforms.items() 
                          if k in browser_platforms and v.get('enabled')}
        
        if browser_configs:
            self.collectors['browser'] = BrowserCollector(browser_configs)
    
    async def start_collection(self):
        """Start all collectors"""
        self.logger.info("Starting GPT Gulp conversation collection...")
        
        self.initialize_collectors()
        
        # Start all collectors concurrently
        tasks = []
        for name, collector in self.collectors.items():
            self.logger.info(f"Starting {name} collector...")
            tasks.append(asyncio.create_task(collector.start()))
        
        if tasks:
            await asyncio.gather(*tasks)
        else:
            self.logger.warning("No collectors enabled")
    
    async def process_conversations(self):
        """Process collected conversations"""
        conversations = await self.storage.get_unprocessed_conversations()
        
        for conversation in conversations:
            try:
                processed = await self.processor.process(conversation)
                await self.storage.save_processed_conversation(processed)
                await self.export_to_obsidian(processed)
                
            except Exception as e:
                self.logger.error(f"Error processing conversation: {e}")
    
    async def export_to_obsidian(self, conversation: Dict):
        """Export processed conversation to Obsidian vault"""
        obsidian_config = self.config.get('obsidian', {})
        vault_path = Path(obsidian_config.get('vault_path', ''))
        
        if not vault_path.exists():
            self.logger.warning(f"Obsidian vault not found: {vault_path}")
            return
        
        # Create AI conversations folder if it doesn't exist
        ai_folder = vault_path / obsidian_config.get('ai_conversations_folder', 'AI Conversations')
        ai_folder.mkdir(exist_ok=True)
        
        # Generate filename
        date_str = conversation['timestamp'].strftime('%Y-%m-%d')
        platform = conversation['platform']
        topic = conversation.get('topic', 'conversation')[:50]  # Limit length
        
        filename = f"{date_str}_{platform}_{topic}.md"
        filepath = ai_folder / filename
        
        # Generate markdown content
        markdown_content = self._generate_markdown(conversation)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        self.logger.info(f"Exported conversation to: {filepath}")
    
    def _generate_markdown(self, conversation: Dict) -> str:
        """Generate markdown content for Obsidian"""
        content = f"""# {conversation['title']}

## Metadata
- **Platform**: {conversation['platform']}
- **Date**: {conversation['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
- **Duration**: {conversation.get('duration', 'Unknown')}
- **Project**: {conversation.get('project', 'General')}

## Tags
{' '.join([f'#{tag}' for tag in conversation.get('tags', [])])}

## Summary
{conversation['summary']}

## Key Points
"""
        
        for point in conversation.get('key_points', []):
            content += f"- {point}\n"
        
        content += f"""
## Files/Resources Referenced
"""
        
        for resource in conversation.get('resources', []):
            content += f"- [[{resource}]]\n"
        
        if conversation.get('include_full_conversation'):
            content += f"""
## Full Conversation
{conversation['full_content']}
"""
        
        return content

    async def run(self):
        """Main run loop"""
        self.logger.info("GPT Gulp starting...")
        
        # Start collection and processing concurrently
        collection_task = asyncio.create_task(self.start_collection())
        
        # Process conversations periodically
        while True:
            await self.process_conversations()
            
            # Wait for sync interval
            sync_interval = self.config.get('sync', {}).get('interval_minutes', 30)
            await asyncio.sleep(sync_interval * 60)

if __name__ == "__main__":
    app = GPTGulp()
    asyncio.run(app.run())
