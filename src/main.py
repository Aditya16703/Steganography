#!/usr/bin/env python3
"""
SteganoGuard Pro - Advanced Secure Steganography Application
Main entry point with enhanced security features
"""

import tkinter as tk
from ui.main_app import SteganoGuardApp

def main():
    """Launch the main application"""
    try:
        root = tk.Tk()
        app = SteganoGuardApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Failed to start application: {e}")

if __name__ == "__main__":
    main()