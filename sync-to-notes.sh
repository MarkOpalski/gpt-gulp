#!/bin/bash
# GPT Gulp Auto-Sync to Notes Repository
# This script runs after GPT Gulp exports conversations

# CONFIGURE THIS PATH TO YOUR NOTES REPOSITORY
NOTES_REPO="/path/to/your/notes/repository"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "🔄 Syncing AI conversations to notes repo..."

# Check if notes repo path is configured
if [ "$NOTES_REPO" = "/path/to/your/notes/repository" ]; then
    echo "❌ Please configure NOTES_REPO path in sync-to-notes.sh"
    echo "   Edit the script and set NOTES_REPO to your actual notes repository path"
    exit 1
fi

# Navigate to notes repository
cd "$NOTES_REPO" || exit 1
# GPT Gulp Auto-Sync to Monorepo
# This script runs after GPT Gulp exports conversations

NOTES_REPO="/Users/markopalski/Projects/Obsidian"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "🔄 Syncing AI conversations to notes repo..."

# Navigate to notes repository
cd "$NOTES_REPO" || exit 1

# Check if there are any changes
if [[ -n $(git status --porcelain) ]]; then
    echo "📝 New conversations detected, committing..."
    
    # Add AI conversation files
    git add Notes/AI-Conversations/
    
    # Commit with timestamp
    git commit -m "🤖 Auto-sync AI conversations - $TIMESTAMP"
    
    # Push to remote (if you want automatic push)
    # git push origin main
    
    echo "✅ AI conversations synced successfully!"
else
    echo "📭 No new conversations to sync"
fi
