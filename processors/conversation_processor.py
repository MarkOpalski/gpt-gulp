"""
Conversation Processor
Processes and summarizes AI conversations
"""

import re
from datetime import datetime
from typing import Dict, List

class ConversationProcessor:
    """Processes AI conversations for summarization and categorization"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.processing_config = config.get('processing', {})
        
    async def process(self, conversation: Dict) -> Dict:
        """Process a conversation and return enhanced version"""
        
        # Create processed conversation
        processed = conversation.copy()
        
        # Generate summary
        processed['summary'] = self._generate_summary(conversation)
        
        # Extract key points
        processed['key_points'] = self._extract_key_points(conversation)
        
        # Detect project/topic
        processed['project'] = self._detect_project(conversation)
        processed['topic'] = self._extract_topic(conversation)
        
        # Generate tags
        processed['tags'] = self._generate_tags(conversation)
        
        # Extract referenced files/resources
        processed['resources'] = self._extract_resources(conversation)
        
        # Calculate duration (if available)
        processed['duration'] = self._calculate_duration(conversation)
        
        # Mark as processed
        processed['processed'] = True
        processed['processed_at'] = datetime.now()
        
        return processed
    
    def _generate_summary(self, conversation: Dict) -> str:
        """Generate a summary of the conversation"""
        content = conversation.get('raw_content', '')
        
        # Simple extractive summarization
        # In a real implementation, you might use an AI model here
        
        lines = content.split('\n')
        important_lines = []
        
        # Look for lines that seem like key statements
        for line in lines:
            line = line.strip()
            if len(line) > 20 and len(line) < 200:
                # Look for question or important statement patterns
                if (line.endswith('?') or 
                    line.startswith('I need') or 
                    line.startswith('How') or
                    line.startswith('Can you') or
                    'implement' in line.lower() or
                    'create' in line.lower() or
                    'build' in line.lower()):
                    important_lines.append(line)
        
        if important_lines:
            return ' '.join(important_lines[:3])  # First 3 important lines
        else:
            # Fallback to first few lines
            meaningful_lines = [l.strip() for l in lines if len(l.strip()) > 20]
            return ' '.join(meaningful_lines[:2]) if meaningful_lines else "AI conversation"
    
    def _extract_key_points(self, conversation: Dict) -> List[str]:
        """Extract key points from the conversation"""
        content = conversation.get('raw_content', '')
        key_points = []
        
        # Look for action items, decisions, or important statements
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Look for bullet points or numbered lists
            if (re.match(r'^[-*•]\s+', line) or 
                re.match(r'^\d+\.\s+', line) or
                'TODO:' in line.upper() or
                'ACTION:' in line.upper()):
                key_points.append(line)
        
        # If no explicit points found, extract important sentences
        if not key_points:
            sentences = re.split(r'[.!?]+', content)
            for sentence in sentences:
                sentence = sentence.strip()
                if (len(sentence) > 30 and 
                    ('will' in sentence or 'should' in sentence or 'need' in sentence)):
                    key_points.append(sentence)
                    if len(key_points) >= 5:  # Limit to 5 points
                        break
        
        return key_points[:10]  # Max 10 key points
    
    def _detect_project(self, conversation: Dict) -> str:
        """Detect which project this conversation relates to"""
        content = conversation.get('raw_content', '').lower()
        source_file = conversation.get('source_file', '').lower()
        
        # Common project indicators
        project_patterns = {
            'portfolio': ['portfolio', 'personal website', 'resume'],
            'todo-app': ['todo', 'task', 'reminder'],
            'consulting': ['consulting', 'client', 'business'],
            'mlb': ['baseball', 'mlb', 'home run', 'sports'],
            'water-cycle': ['water', 'cycle', 'environment'],
            'case-study': ['case study', 'analysis', 'research']
        }
        
        for project, keywords in project_patterns.items():
            if any(keyword in content or keyword in source_file for keyword in keywords):
                return project
        
        return 'general'
    
    def _extract_topic(self, conversation: Dict) -> str:
        """Extract the main topic/subject"""
        title = conversation.get('title', '')
        content = conversation.get('raw_content', '')
        
        # Try to extract from title first
        if title and len(title) > 5:
            return title[:50]
        
        # Extract from content
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 100:
                return line[:50]
        
        return 'conversation'
    
    def _generate_tags(self, conversation: Dict) -> List[str]:
        """Generate relevant tags for the conversation"""
        content = conversation.get('raw_content', '').lower()
        platform = conversation.get('platform', '')
        project = conversation.get('project', 'general')
        
        tags = [platform, project]
        
        # Technology tags
        tech_keywords = {
            'python': ['python', 'py', 'django', 'flask'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue'],
            'web': ['html', 'css', 'web', 'frontend', 'backend'],
            'ai': ['ai', 'artificial intelligence', 'machine learning', 'ml'],
            'data': ['data', 'analysis', 'visualization', 'csv'],
            'git': ['git', 'github', 'version control'],
            'deployment': ['deploy', 'netlify', 'aws', 'hosting']
        }
        
        for tag, keywords in tech_keywords.items():
            if any(keyword in content for keyword in keywords):
                tags.append(tag)
        
        # Activity tags
        if any(word in content for word in ['create', 'build', 'develop']):
            tags.append('development')
        if any(word in content for word in ['fix', 'debug', 'error', 'issue']):
            tags.append('debugging')
        if any(word in content for word in ['help', 'how', 'question']):
            tags.append('help')
        
        return list(set(tags))  # Remove duplicates
    
    def _extract_resources(self, conversation: Dict) -> List[str]:
        """Extract referenced files, URLs, or resources"""
        content = conversation.get('raw_content', '')
        resources = []
        
        # Extract file paths
        file_patterns = [
            r'[a-zA-Z0-9_/-]+\.[a-zA-Z]{2,4}',  # Files with extensions
            r'`[^`]+`',  # Code blocks might contain filenames
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, content)
            resources.extend(matches)
        
        # Extract URLs
        url_pattern = r'https?://[^\s<>"\']+|www\.[^\s<>"\']+\.[a-zA-Z]{2,}'
        urls = re.findall(url_pattern, content)
        resources.extend(urls)
        
        # Clean and filter resources
        clean_resources = []
        for resource in resources:
            resource = resource.strip('`"\'')
            if len(resource) > 3 and resource not in clean_resources:
                clean_resources.append(resource)
        
        return clean_resources[:20]  # Limit to 20 resources
    
    def _calculate_duration(self, conversation: Dict) -> str:
        """Calculate conversation duration if possible"""
        # This would need timestamp data from the conversation
        # For now, return placeholder
        return "Unknown"
