#!/usr/bin/env python3
"""
GPT Gulp Setup Script
Sets up the environment and dependencies
"""

import os
import subprocess
import sys
from pathlib import Path

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "watchdog"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    print("📁 Setting up directories...")
    
    directories = [
        "storage",
        "output",
        "logs"
    ]
    
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"   Created: {dir_name}/")
    
    print("✅ Directories created")

def check_obsidian_path():
    """Check if Obsidian vault path exists"""
    print("🔍 Checking Obsidian configuration...")
    
    # Common Obsidian vault locations
    common_paths = [
        Path.home() / "Documents" / "Obsidian Vault",
        Path.home() / "Documents" / "Obsidian",
        Path.home() / "Obsidian",
        Path.home() / "vault"
    ]
    
    for path in common_paths:
        if path.exists():
            print(f"✅ Found potential Obsidian vault: {path}")
            return str(path)
    
    print("⚠️  Obsidian vault not found in common locations")
    print("   You can configure this later using: python cli.py setup-obsidian")
    return None

def main():
    """Main setup function"""
    print("🚀 Setting up GPT Gulp...")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup directories
    setup_directories()
    
    # Check Obsidian
    obsidian_path = check_obsidian_path()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Configure Obsidian: python cli.py setup-obsidian")
    print("2. Test the system: python test_system.py")
    print("3. Start collection: python cli.py start")
    print("\nFor help: python cli.py --help")

if __name__ == "__main__":
    main()
