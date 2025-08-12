#!/bin/bash
# GPT Gulp Release Script
# Helps with GitHub repository setup and release

set -e  # Exit on any error

echo "🚀 GPT Gulp Release Helper"
echo "=========================="
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the gpt-gulp directory"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Error: Git repository not initialized. Run 'git init' first."
    exit 1
fi

echo "📋 Pre-release checks..."

# Check if all files are committed
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes. Please commit them first."
    git status --short
    exit 1
fi

echo "✅ All files committed"

# Check if Python dependencies work
echo "🐍 Testing Python setup..."
if ! python3 -c "import watchdog" 2>/dev/null; then
    echo "❌ Error: Dependencies not installed. Run 'pip install -r requirements.txt'"
    exit 1
fi

echo "✅ Dependencies installed"

# Run quick test
echo "🧪 Running tests..."
if ! python3 test_system.py > /dev/null 2>&1; then
    echo "❌ Error: Tests failed. Please fix before release."
    exit 1
fi

echo "✅ Tests passed"

echo ""
echo "🎉 Ready for GitHub release!"
echo ""
echo "Next steps:"
echo "1. Create repository on GitHub.com:"
echo "   https://github.com/new"
echo "   Repository name: gpt-gulp"
echo "   Description: AI Conversation Archive System"
echo ""
echo "2. Add remote and push:"
echo "   git remote add origin https://github.com/MarkOpalski/gpt-gulp.git"
echo "   git push -u origin main"
echo ""
echo "3. Create release:"
echo "   - Go to: https://github.com/MarkOpalski/gpt-gulp/releases/new"
echo "   - Tag: v1.0.0"
echo "   - Title: GPT Gulp v1.0.0 - Initial Release"
echo "   - Use description from RELEASE_CHECKLIST.md"
echo ""
echo "4. Share with community! 🌟"
echo ""

# Ask if user wants to open GitHub
read -p "Open GitHub in browser to create repository? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v open &> /dev/null; then
        open "https://github.com/new"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "https://github.com/new"
    else
        echo "Please open: https://github.com/new"
    fi
fi
