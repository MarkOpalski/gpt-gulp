# GPT Gulp - AI Conversation Archive System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A comprehensive system for capturing, processing, and storing AI conversations from multiple sources into a centralized knowledge base.

## Overview

GPT Gulp automatically captures and summarizes conversations from:

- VS Code AI assistants (Copilot, Claude, etc.)
- Browser-based AI platforms (Claude.ai, ChatGPT, Gemini, Perplexity)
- Other AI tools and environments

All conversations are processed, summarized, and stored in Obsidian-compatible Markdown format for easy knowledge management.

## Features

- 🤖 Multi-platform AI conversation capture
- 📝 Automatic summarization and categorization
- 🗂️ Obsidian-compatible markdown output
- 🔍 Searchable conversation history
- 📊 Analytics and insights on AI usage
- 🔄 Real-time sync with your knowledge base

## Architecture

```
gpt-gulp/
├── collectors/          # Data collection modules
│   ├── vscode/         # VS Code conversation capture
│   ├── browser/        # Browser extension for web AI platforms
│   └── api/            # API integrations
├── processors/         # Content processing and summarization
├── storage/           # Data storage and organization
├── output/            # Generated markdown files for Obsidian
└── config/            # Configuration files
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Git

### Quick Install

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MarkOpalski/gpt-gulp.git
   cd gpt-gulp
   ```

2. **Set up virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Test the installation:**

   ```bash
   ./run.sh test
   ```

5. **Configure Obsidian integration:**
   ```bash
   ./run.sh setup-obsidian
   ```

## Quick Start

1. **Setup the environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install watchdog
   ```

2. **Test the system:**

   ```bash
   ./run.sh test
   ```

3. **Configure Obsidian integration:**

   ```bash
   ./run.sh setup-obsidian
   ```

4. **Start collecting conversations:**
   ```bash
   ./run.sh start
   ```

## Usage

### Command Line Interface

```bash
# Show collection statistics
./run.sh stats

# List recent conversations
./run.sh list
./run.sh list --limit 20

# Export conversations to Obsidian
./run.sh export
./run.sh export --sync    # Export and auto-commit to git

# Sync to notes repository
./run.sh sync

# Configure Obsidian
./run.sh setup-obsidian

# Start conversation collection
./run.sh start
```

### Integration with Notes Repository

GPT Gulp can integrate with your existing notes monorepo:

1. **Configure output path** to your notes repository
2. **Export conversations** using `./run.sh export --sync`
3. **Auto-commit** conversations to git with timestamps
4. **Leverage existing backup** - your notes auto-backup will include AI conversations

```bash
# One-command export and sync
./run.sh export --sync
```

### Python API

```python
from main import GPTGulp
from storage.conversation_storage import ConversationStorage

# Initialize the system
app = GPTGulp()

# Get conversation statistics
storage = ConversationStorage(app.config)
stats = await storage.get_storage_stats()

# Export to Obsidian
conversations = await storage.get_recent_conversations()
for conv in conversations:
    await app.export_to_obsidian(conv)
```

## Configuration

Edit `config/config.json` to customize:

- **Obsidian vault path**: Where to save conversation files
- **Platform settings**: Enable/disable specific AI platforms
- **Processing options**: Summarization and categorization settings
- **Output format**: Markdown structure and metadata

## Browser Extension (Coming Soon)

The browser extension will automatically capture conversations from:

- Claude.ai
- ChatGPT
- Google Gemini
- Perplexity
- Other AI platforms

## Obsidian Integration

Conversations are exported as markdown files with:

- **Metadata**: Platform, date, project, tags
- **Summary**: Key points and overview
- **Full content**: Complete conversation (optional)
- **Links**: Referenced files and resources
- **Tags**: Auto-generated for easy organization

## Status

✅ Core system implemented
✅ VS Code conversation capture
✅ Conversation processing and summarization
✅ Obsidian export functionality
✅ CLI interface
✅ Storage and retrieval system
🚧 Browser extension (in development)
🚧 Real-time VS Code integration (in development)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/gpt-gulp.git`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate it: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run tests: `./run.sh test`
7. Make your changes and submit a pull request!

### Roadmap

- [ ] Browser extension for web platforms
- [ ] Real-time VS Code API integration
- [ ] Advanced AI-powered summarization
- [ ] Web dashboard for conversation management
- [ ] Mobile app support
- [ ] Team collaboration features

## Security

Please review our [Security Policy](SECURITY.md) for reporting security vulnerabilities.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who help improve GPT Gulp
- Inspired by the need for better AI conversation management
- Built with ❤️ for the open source community

## Support

- 📖 [Documentation](https://github.com/MarkOpalski/gpt-gulp/wiki)
- 🐛 [Report Bug](https://github.com/MarkOpalski/gpt-gulp/issues)
- 💡 [Request Feature](https://github.com/MarkOpalski/gpt-gulp/issues)
- 💬 [Discussions](https://github.com/MarkOpalski/gpt-gulp/discussions)
