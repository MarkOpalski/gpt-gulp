#!/bin/bash
# GPT Gulp Activation Script
# This script activates the virtual environment and provides easy access to GPT Gulp commands

cd "$(dirname "$0")"
source venv/bin/activate

if [ $# -eq 0 ]; then
    echo "🚀 GPT Gulp - AI Conversation Archive System"
    echo "============================================="
    echo ""
    echo "Available commands:"
    echo "  ./run.sh stats           - Show collection statistics"
    echo "  ./run.sh list            - List recent conversations"
    echo "  ./run.sh export          - Export conversations to Obsidian"
    echo "  ./run.sh export --sync   - Export and sync to notes repo"
    echo "  ./run.sh sync            - Sync conversations to notes repo"
    echo "  ./run.sh setup-obsidian  - Configure Obsidian integration"
    echo "  ./run.sh start           - Start conversation collection"
    echo "  ./run.sh test            - Run system test"
    echo ""
    echo "Examples:"
    echo "  ./run.sh list --limit 20"
    echo "  ./run.sh export --project portfolio"
    echo ""
else
    case "$1" in
        "test")
            python test_system.py
            ;;
        "start"|"stats"|"list"|"export"|"setup-obsidian")
            python cli.py "$@"
            # Auto-sync after export if --sync flag is present
            if [ "$1" = "export" ] && [ "$2" = "--sync" ]; then
                echo ""
                ./sync-to-notes.sh
            fi
            ;;
        "sync")
            ./sync-to-notes.sh
            ;;
        *)
            echo "Unknown command: $1"
            echo "Run './run.sh' to see available commands"
            ;;
    esac
fi
