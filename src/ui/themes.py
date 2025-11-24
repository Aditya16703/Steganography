"""
Modern dark theme for SteganoGuard Pro
"""

import tkinter as tk
from tkinter import ttk

class ModernTheme:
    """Modern dark theme with gradient accents"""
    
    COLORS = {
        # Dark theme palette
        'bg_primary': '#1a1a1a',
        'bg_secondary': '#2d2d2d',
        'bg_tertiary': '#3d3d3d',
        'accent_primary': '#6366f1',
        'accent_secondary': '#8b5cf6',
        'accent_success': '#10b981',
        'accent_warning': '#f59e0b',
        'accent_danger': '#ef4444',
        'text_primary': '#ffffff',
        'text_secondary': '#a0a0a0',
        'text_muted': '#666666',
        'border_light': '#404040',
        'border_dark': '#262626'
    }
    
    GRADIENTS = {
        'primary': ['#6366f1', '#8b5cf6'],
        'success': ['#10b981', '#34d399'],
        'warning': ['#f59e0b', '#fbbf24'],
        'danger': ['#ef4444', '#f87171']
    }
    
    @classmethod
    def apply_theme(cls, root):
        """Apply modern theme to the application"""
        style = ttk.Style()
        
        # Configure main styles
        style.configure('TFrame', background=cls.COLORS['bg_primary'])
        style.configure('TLabel', background=cls.COLORS['bg_primary'], 
                       foreground=cls.COLORS['text_primary'])
        style.configure('TButton', 
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('TButton',
                 background=[('active', cls.COLORS['accent_primary']),
                           ('pressed', cls.COLORS['accent_secondary'])])
        
        # Custom styles
        style.configure('Primary.TButton',
                       background=cls.COLORS['accent_primary'],
                       foreground='white')
        
        style.configure('Success.TButton',
                       background=cls.COLORS['accent_success'],
                       foreground='white')
        
        style.configure('Card.TFrame',
                       background=cls.COLORS['bg_secondary'],
                       relief='raised',
                       borderwidth=1)
        
        # Set window background
        root.configure(bg=cls.COLORS['bg_primary'])