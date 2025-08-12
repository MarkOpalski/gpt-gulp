"""
VS Code Conversation Collector
Monitors VS Code for AI assistant conversations
"""

import asyncio
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class VSCodeConversationHandler(FileSystemEventHandler):
    """File system event handler for VS Code conversations"""
    
    def __init__(self, collector):
        self.collector = collector
        
    def on_modified(self, event):
        if not event.is_directory:
            self.collector.handle_file_change(event.src_path)

class VSCodeCollector:
    """Collects conversations from VS Code AI assistants"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.vscode_config = config.get('platforms', {}).get('vscode', {})
        self.conversations = []
        self.observer = None
        
        # VS Code paths (may vary by system)
        self.vscode_paths = self._get_vscode_paths()
        
    def _get_vscode_paths(self) -> List[Path]:
        """Get VS Code configuration and data paths"""
        home = Path.home()
        paths = []
        
        # macOS paths
        if os.name == 'posix' and 'darwin' in os.uname().sysname.lower():
            paths.extend([
                home / "Library/Application Support/Code/User/workspaceStorage",
                home / "Library/Application Support/Code/logs",
                home / "Library/Application Support/Code/CachedExtensions"
            ])
        
        # Linux paths
        elif os.name == 'posix':
            paths.extend([
                home / ".config/Code/User/workspaceStorage",
                home / ".config/Code/logs"
            ])
        
        # Windows paths
        elif os.name == 'nt':
            appdata = Path(os.environ.get('APPDATA', ''))
            paths.extend([
                appdata / "Code/User/workspaceStorage",
                appdata / "Code/logs"
            ])
        
        return [p for p in paths if p.exists()]
    
    def handle_file_change(self, filepath: str):
        """Handle file system changes that might contain conversations"""
        try:
            # Check if this might be a conversation file
            if self._is_conversation_file(filepath):
                conversation = self._extract_conversation(filepath)
                if conversation:
                    self.conversations.append(conversation)
                    
        except Exception as e:
            print(f"Error handling file change {filepath}: {e}")
    
    def _is_conversation_file(self, filepath: str) -> bool:
        """Check if file might contain AI conversation data"""
        filepath_lower = filepath.lower()
        
        # Look for patterns that might indicate AI conversations
        conversation_indicators = [
            'copilot', 'claude', 'gpt', 'ai', 'assistant',
            'chat', 'conversation', 'history'
        ]
        
        return any(indicator in filepath_lower for indicator in conversation_indicators)
    
    def _extract_conversation(self, filepath: str) -> Optional[Dict]:
        """Extract conversation data from file"""
        try:
            # This is a simplified extraction - would need to be customized
            # based on how each AI assistant stores conversation data
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Basic conversation detection
            if len(content) < 100:  # Too short to be meaningful
                return None
            
            # Create conversation object
            conversation = {
                'id': f"vscode_{int(time.time())}",
                'platform': 'vscode',
                'timestamp': datetime.now(),
                'source_file': filepath,
                'raw_content': content,
                'title': self._extract_title(content),
                'processed': False
            }
            
            return conversation
            
        except Exception as e:
            print(f"Error extracting conversation from {filepath}: {e}")
            return None
    
    def _extract_title(self, content: str) -> str:
        """Extract a title from conversation content"""
        lines = content.split('\n')
        
        # Look for first meaningful line
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 100:
                return line[:80] + "..." if len(line) > 80 else line
        
        return "VS Code Conversation"
    
    async def start(self):
        """Start monitoring VS Code for conversations"""
        print("Starting VS Code conversation monitoring...")
        
        # Set up file system watchers
        self.observer = Observer()
        handler = VSCodeConversationHandler(self)
        
        for path in self.vscode_paths:
            try:
                self.observer.schedule(handler, str(path), recursive=True)
                print(f"Watching: {path}")
            except Exception as e:
                print(f"Error watching {path}: {e}")
        
        if self.vscode_paths:
            self.observer.start()
            
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                self.observer.stop()
                
        self.observer.join()
    
    def get_conversations(self) -> List[Dict]:
        """Get collected conversations"""
        return self.conversations
    
    def clear_conversations(self):
        """Clear conversation buffer"""
        self.conversations = []
