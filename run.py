#!/usr/bin/env python3
"""
SteganoGuard Pro - Simple Launcher
"""

import sys
import os
import tkinter as tk
from src.ui.themes import ModernTheme

# Add user site-packages to path
user_site = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Python", "Python313", "site-packages")
if os.path.exists(user_site):
    sys.path.insert(0, user_site)

def main():
    """Main application entry point"""
    try:
        print("🚀 Starting SteganoGuard Pro...")
        
        # Add src to Python path
        src_path = os.path.join(os.path.dirname(__file__), 'src')
        if os.path.exists(src_path):
            sys.path.insert(0, src_path)
        else:
            print("❌ Error: 'src' directory not found")
            input("Press Enter to exit...")
            return
        
        # Import and start
        from src.ui.main_app import SteganoGuardApp
        
        root = tk.Tk()
        root.title("SteganoGuard Pro v2.1")
        root.geometry("1200x800")
        root.minsize(1000, 700)
        root.eval('tk::PlaceWindow . center')
        
        app = SteganoGuardApp(root)
        
        print("✅ Application started successfully!")
        print("💡 Close the window to exit")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n🔧 Installing required dependencies...")
        
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "numpy", "cryptography", "pycryptodome"])
            print("✅ Dependencies installed. Please run the application again.")
        except Exception as install_error:
            print(f"❌ Installation failed: {install_error}")
            print("💡 Try: pip install pillow numpy cryptography pycryptodome")
        
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()