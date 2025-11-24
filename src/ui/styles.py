"""
Modern UI styles for SteganoGuard Pro
"""

def apply_dark_theme(root):
    """Apply dark theme to the application"""
    try:
        # Create style object
        style = ttk.Style()
        
        # Configure styles
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='#ffffff')
        style.configure('TButton', background='#3c3c3c', foreground='#ffffff')
        style.configure('TEntry', fieldbackground='#3c3c3c', foreground='#ffffff')
        style.configure('TCombobox', fieldbackground='#3c3c3c', foreground='#ffffff')
        style.configure('TLabelframe', background='#2b2b2b', foreground='#ffffff')
        style.configure('TLabelframe.Label', background='#2b2b2b', foreground='#ffffff')
        
        # Configure progress bar styles
        style.configure('success.Horizontal.TProgressbar', 
                       background='#4CAF50')
        style.configure('warning.Horizontal.TProgressbar', 
                       background='#FF9800')
        style.configure('danger.Horizontal.TProgressbar', 
                       background='#F44336')
        
        # Set window background
        root.configure(bg='#2b2b2b')
        
    except Exception as e:
        print(f"Theme application warning: {e}")
        # Fallback: basic dark background
        root.configure(bg='#2b2b2b')