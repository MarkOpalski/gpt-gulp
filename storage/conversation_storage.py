"""
Conversation Storage
Manages storage and retrieval of conversation data
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class ConversationStorage:
    """Manages conversation data storage and retrieval"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.db_path = Path("storage/conversations.db")
        self.setup_database()
        
    def setup_database(self):
        """Initialize SQLite database for conversation storage"""
        self.db_path.parent.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                platform TEXT,
                timestamp TEXT,
                title TEXT,
                summary TEXT,
                project TEXT,
                topic TEXT,
                tags TEXT,  -- JSON array
                resources TEXT,  -- JSON array
                key_points TEXT,  -- JSON array
                raw_content TEXT,
                processed BOOLEAN DEFAULT FALSE,
                processed_at TEXT,
                source_file TEXT,
                url TEXT,
                duration TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    async def save_conversation(self, conversation: Dict):
        """Save a new conversation to storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO conversations 
            (id, platform, timestamp, title, summary, project, topic, tags, 
             resources, key_points, raw_content, processed, processed_at, 
             source_file, url, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            conversation['id'],
            conversation['platform'],
            conversation['timestamp'].isoformat(),
            conversation.get('title', ''),
            conversation.get('summary', ''),
            conversation.get('project', ''),
            conversation.get('topic', ''),
            json.dumps(conversation.get('tags', [])),
            json.dumps(conversation.get('resources', [])),
            json.dumps(conversation.get('key_points', [])),
            conversation.get('raw_content', ''),
            conversation.get('processed', False),
            conversation.get('processed_at', datetime.now()).isoformat() if conversation.get('processed_at') else None,
            conversation.get('source_file', ''),
            conversation.get('url', ''),
            conversation.get('duration', '')
        ))
        
        conn.commit()
        conn.close()
    
    async def get_unprocessed_conversations(self) -> List[Dict]:
        """Get conversations that haven't been processed yet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE processed = FALSE 
            ORDER BY timestamp DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversation = self._row_to_dict(row)
            conversations.append(conversation)
        
        return conversations
    
    async def save_processed_conversation(self, conversation: Dict):
        """Update conversation with processed data"""
        await self.save_conversation(conversation)
    
    async def get_conversations_by_project(self, project: str) -> List[Dict]:
        """Get conversations for a specific project"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE project = ? 
            ORDER BY timestamp DESC
        """, (project,))
        
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversation = self._row_to_dict(row)
            conversations.append(conversation)
        
        return conversations
    
    async def get_recent_conversations(self, limit: int = 50) -> List[Dict]:
        """Get recent conversations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversation = self._row_to_dict(row)
            conversations.append(conversation)
        
        return conversations
    
    def _row_to_dict(self, row) -> Dict:
        """Convert database row to conversation dictionary"""
        columns = [
            'id', 'platform', 'timestamp', 'title', 'summary', 'project', 
            'topic', 'tags', 'resources', 'key_points', 'raw_content', 
            'processed', 'processed_at', 'source_file', 'url', 'duration', 
            'created_at'
        ]
        
        conversation = {}
        for i, column in enumerate(columns):
            value = row[i]
            
            # Parse JSON fields
            if column in ['tags', 'resources', 'key_points'] and value:
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    value = []
            
            # Parse datetime fields
            elif column in ['timestamp', 'processed_at', 'created_at'] and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    pass
            
            # Parse boolean fields
            elif column == 'processed':
                value = bool(value)
            
            conversation[column] = value
        
        return conversation
    
    async def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total conversations
        cursor.execute("SELECT COUNT(*) FROM conversations")
        total = cursor.fetchone()[0]
        
        # Processed conversations
        cursor.execute("SELECT COUNT(*) FROM conversations WHERE processed = TRUE")
        processed = cursor.fetchone()[0]
        
        # Conversations by platform
        cursor.execute("SELECT platform, COUNT(*) FROM conversations GROUP BY platform")
        by_platform = dict(cursor.fetchall())
        
        # Conversations by project
        cursor.execute("SELECT project, COUNT(*) FROM conversations GROUP BY project")
        by_project = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_conversations': total,
            'processed_conversations': processed,
            'unprocessed_conversations': total - processed,
            'by_platform': by_platform,
            'by_project': by_project
        }
