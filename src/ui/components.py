"""
Modern UI components for SteganoGuard Pro
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class ModernButton(ttk.Button):
    """Modern button with different styles"""
    
    def __init__(self, parent, **kwargs):
        self.style_name = kwargs.pop('style', 'default')
        self.text = kwargs.pop('text', '')
        self.command = kwargs.pop('command', None)
        
        super().__init__(parent, **kwargs)
        
        if self.style_name != 'default':
            self.configure(style=f'{self.style_name}.TButton')

class CardFrame(ttk.Frame):
    """Modern card component with shadow effect"""
    
    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, style='Card.TFrame', **kwargs)
        
        if title:
            title_label = ttk.Label(self, text=title, font=('Arial', 12, 'bold'))
            title_label.pack(anchor='w', padx=15, pady=(15, 5))

class IconLabel(ttk.Label):
    """Label with icon support"""
    
    def __init__(self, parent, icon=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        if icon:
            self.set_icon(icon)
    
    def set_icon(self, icon_name):
        """Set icon for label"""
        # In a real app, you'd load actual icons
        pass

class ProgressRing(tk.Canvas):
    """Circular progress indicator"""
    
    def __init__(self, parent, size=60, **kwargs):
        super().__init__(parent, width=size, height=size, 
                        highlightthickness=0, **kwargs)
        self.size = size
        self.center = size // 2
        self.radius = (size - 10) // 2
        
    def set_progress(self, percentage):
        """Set progress percentage (0-100)"""
        self.delete("all")
        
        # Background circle
        self.create_oval(5, 5, self.size-5, self.size-5, 
                        outline='#3d3d3d', width=3)
        
        # Progress arc
        if percentage > 0:
            angle = 360 * percentage / 100
            self.create_arc(5, 5, self.size-5, self.size-5,
                          start=90, extent=-angle,
                          outline='#6366f1', width=3, style='arc')
        
        # Percentage text
        self.create_text(self.center, self.center, 
                        text=f"{int(percentage)}%", 
                        fill='white', font=('Arial', 10, 'bold'))

class FileDropZone(tk.Frame):
    """Modern file drop zone with drag & drop support"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='#2d2d2d', relief='raised', bd=2)
        
        # Drop zone content
        self.icon_label = ttk.Label(self, text="📁", font=('Arial', 24))
        self.icon_label.pack(pady=(20, 10))
        
        self.title_label = ttk.Label(self, text="Drop Image Here", 
                                   font=('Arial', 14, 'bold'))
        self.title_label.pack(pady=5)
        
        self.subtitle_label = ttk.Label(self, text="or click to browse", 
                                      foreground='#a0a0a0')
        self.subtitle_label.pack(pady=(0, 20))
        
        self.drop_handlers = []
    
    def add_drop_handler(self, handler):
        """Add file drop handler"""
        self.drop_handlers.append(handler)

class StatusBar(ttk.Frame):
    """Modern status bar with progress indicators"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Status message
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(side='left', padx=10)
        
        # Progress indicator
        self.progress = ttk.Progressbar(self, mode='indeterminate', length=100)
        
        # Capacity indicator
        self.capacity_var = tk.StringVar(value="")
        self.capacity_label = ttk.Label(self, textvariable=self.capacity_var,
                                      foreground='#a0a0a0')
        self.capacity_label.pack(side='right', padx=10)
    
    def set_status(self, message, show_progress=False):
        """Update status message"""
        self.status_var.set(message)
        
        if show_progress:
            self.progress.pack(side='right', padx=10)
            self.progress.start()
        else:
            self.progress.stop()
            self.progress.pack_forget()
    
    def set_capacity(self, used, total):
        """Update capacity information"""
        if total > 0:
            percentage = (used / total) * 100
            self.capacity_var.set(f"Capacity: {percentage:.1f}%")