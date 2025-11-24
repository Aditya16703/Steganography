import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
from typing import Optional

from .themes import ModernTheme
from .components import ModernButton, CardFrame, ProgressRing, FileDropZone, StatusBar

class SteganoGuardApp:
    """
    Modern SteganoGuard Pro Application with Beautiful UI
    """
    
    def __init__(self, root):
        self.root = root
        self.setup_app()
        
        # Initialize core components
        try:
            from src.core.stegano_engine import SteganoEngine
            from src.core.crypto_manager import CryptoManager
            self.stegano_engine = SteganoEngine()
            self.crypto_manager = CryptoManager()
        except ImportError as e:
            messagebox.showerror("Error", f"Failed to initialize core components: {e}")
            return
        
        # Application state
        self.current_image_path: Optional[str] = None
        self.current_stego_image: Optional[Image.Image] = None
        
        self.setup_ui()
        ModernTheme.apply_theme(self.root)
        
    def setup_app(self):
        """Configure main application window"""
        self.root.title("🔒 SteganoGuard Pro • Advanced Steganography")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Set window icon and properties
        self.root.configure(bg=ModernTheme.COLORS['bg_primary'])
        
        # Center window on screen
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_ui(self):
        """Setup the modern user interface"""
        self.create_sidebar()
        self.create_main_content()
        self.create_status_bar()
        
    def create_sidebar(self):
        """Create modern sidebar navigation"""
        self.sidebar = tk.Frame(self.root, bg=ModernTheme.COLORS['bg_secondary'], width=250)
        self.sidebar.pack(side='left', fill='y', padx=10, pady=10)
        self.sidebar.pack_propagate(False)
        
        # App logo/header
        header_frame = tk.Frame(self.sidebar, bg=ModernTheme.COLORS['bg_secondary'])
        header_frame.pack(fill='x', padx=20, pady=20)
        
        logo_label = tk.Label(header_frame, text="🔒 SteganoGuard", 
                            font=('Arial', 20, 'bold'), 
                            bg=ModernTheme.COLORS['bg_secondary'],
                            fg=ModernTheme.COLORS['text_primary'])
        logo_label.pack(anchor='w')
        
        version_label = tk.Label(header_frame, text="PRO v2.1", 
                               font=('Arial', 10), 
                               bg=ModernTheme.COLORS['bg_secondary'],
                               fg=ModernTheme.COLORS['accent_primary'])
        version_label.pack(anchor='w')
        
        # Navigation menu
        nav_frame = tk.Frame(self.sidebar, bg=ModernTheme.COLORS['bg_secondary'])
        nav_frame.pack(fill='x', padx=10, pady=20)
        
        # Navigation items
        nav_items = [
            ("📝 Text Steganography", self.show_text_tab),
            ("📁 File Steganography", self.show_file_tab),
            ("🔍 Image Analysis", self.show_analysis_tab),
            ("⚙️ Settings", self.show_settings_tab)
        ]
        
        self.nav_buttons = []
        for text, command in nav_items:
            btn = tk.Button(nav_frame, text=text, font=('Arial', 11),
                          bg=ModernTheme.COLORS['bg_secondary'],
                          fg=ModernTheme.COLORS['text_primary'],
                          bd=0, cursor='hand2', anchor='w',
                          command=command)
            btn.pack(fill='x', pady=8, padx=10)
            self.nav_buttons.append(btn)
        
        # Stats section
        stats_frame = tk.Frame(self.sidebar, bg=ModernTheme.COLORS['bg_secondary'])
        stats_frame.pack(side='bottom', fill='x', padx=10, pady=20)
        
        tk.Label(stats_frame, text="Quick Stats", font=('Arial', 12, 'bold'),
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_primary']).pack(anchor='w', pady=10)
        
        self.stats_labels = {}
        stats_data = [
            ("Images Processed", "0"),
            ("Success Rate", "100%"),
            ("Security Level", "High")
        ]
        
        for stat, value in stats_data:
            frame = tk.Frame(stats_frame, bg=ModernTheme.COLORS['bg_secondary'])
            frame.pack(fill='x', pady=3)
            
            tk.Label(frame, text=stat, font=('Arial', 9),
                   bg=ModernTheme.COLORS['bg_secondary'],
                   fg=ModernTheme.COLORS['text_secondary']).pack(side='left')
            
            value_label = tk.Label(frame, text=value, font=('Arial', 9, 'bold'),
                                 bg=ModernTheme.COLORS['bg_secondary'],
                                 fg=ModernTheme.COLORS['accent_primary'])
            value_label.pack(side='right')
            self.stats_labels[stat] = value_label
        
    def create_main_content(self):
        """Create main content area"""
        self.main_content = tk.Frame(self.root, bg=ModernTheme.COLORS['bg_primary'])
        self.main_content.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Create tab content
        self.text_tab_content = self.create_text_tab()
        self.file_tab_content = self.create_file_tab()
        self.analysis_tab_content = self.create_analysis_tab()
        self.settings_tab_content = self.create_settings_tab()
        
        # Show default tab
        self.show_text_tab()
        
    def create_text_tab(self):
        """Create modern text steganography tab"""
        container = tk.Frame(self.main_content, bg=ModernTheme.COLORS['bg_primary'])
        
        # Header
        header_frame = tk.Frame(container, bg=ModernTheme.COLORS['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="📝 Text Steganography", 
                font=('Arial', 24, 'bold'),
                bg=ModernTheme.COLORS['bg_primary'],
                fg=ModernTheme.COLORS['text_primary']).pack(anchor='w')
        
        tk.Label(header_frame, text="Hide and extract secret messages in images", 
                font=('Arial', 12),
                bg=ModernTheme.COLORS['bg_primary'],
                fg=ModernTheme.COLORS['text_secondary']).pack(anchor='w')
        
        # Main content grid
        content_frame = tk.Frame(container, bg=ModernTheme.COLORS['bg_primary'])
        content_frame.pack(fill='both', expand=True)
        
        # Left column - Image operations
        left_column = tk.Frame(content_frame, bg=ModernTheme.COLORS['bg_primary'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Image upload card
        upload_card = CardFrame(left_column, title="📁 Image Upload")
        upload_card.pack(fill='x', pady=(0, 15))
        
        self.drop_zone = FileDropZone(upload_card, height=200)
        self.drop_zone.pack(fill='x', padx=15, pady=15)
        self.drop_zone.bind('<Button-1>', lambda e: self.open_image())
        
        # Image info card
        info_card = CardFrame(left_column, title="📊 Image Information")
        info_card.pack(fill='x', pady=(0, 15))
        
        self.image_info_text = tk.Text(info_card, height=6, wrap=tk.WORD,
                                     bg=ModernTheme.COLORS['bg_tertiary'],
                                     fg=ModernTheme.COLORS['text_primary'],
                                     borderwidth=0, font=('Arial', 10))
        self.image_info_text.pack(fill='x', padx=15, pady=15)
        self.image_info_text.insert('1.0', "No image loaded")
        self.image_info_text.config(state='disabled')
        
        # Right column - Text operations
        right_column = tk.Frame(content_frame, bg=ModernTheme.COLORS['bg_primary'])
        right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Message card
        message_card = CardFrame(right_column, title="💬 Secret Message")
        message_card.pack(fill='both', expand=True, pady=(0, 15))
        
        self.text_input = scrolledtext.ScrolledText(message_card, wrap=tk.WORD,
                                                  bg=ModernTheme.COLORS['bg_tertiary'],
                                                  fg=ModernTheme.COLORS['text_primary'],
                                                  insertbackground=ModernTheme.COLORS['text_primary'],
                                                  borderwidth=0, font=('Consolas', 11))
        self.text_input.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Security card
        security_card = CardFrame(right_column, title="🔒 Security Settings")
        security_card.pack(fill='x', pady=(0, 15))
        
        security_content = tk.Frame(security_card, bg=ModernTheme.COLORS['bg_secondary'])
        security_content.pack(fill='x', padx=15, pady=15)
        
        # Encryption toggle
        self.encrypt_var = tk.BooleanVar(value=True)
        encrypt_check = tk.Checkbutton(security_content, text="Enable Encryption",
                                     variable=self.encrypt_var,
                                     bg=ModernTheme.COLORS['bg_secondary'],
                                     fg=ModernTheme.COLORS['text_primary'],
                                     selectcolor=ModernTheme.COLORS['bg_tertiary'],
                                     command=self.toggle_encryption,
                                     font=('Arial', 10))
        encrypt_check.pack(anchor='w', pady=5)
        
        # Password frame
        self.password_frame = tk.Frame(security_content, bg=ModernTheme.COLORS['bg_secondary'])
        
        tk.Label(self.password_frame, text="Password:", 
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_primary'],
                font=('Arial', 10)).pack(anchor='w')
        
        password_row = tk.Frame(self.password_frame, bg=ModernTheme.COLORS['bg_secondary'])
        password_row.pack(fill='x', pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(password_row, textvariable=self.password_var,
                                     show="•", font=('Arial', 10),
                                     bg=ModernTheme.COLORS['bg_tertiary'],
                                     fg=ModernTheme.COLORS['text_primary'],
                                     insertbackground=ModernTheme.COLORS['text_primary'],
                                     relief='flat')
        self.password_entry.pack(side='left', fill='x', expand=True)
        
        generate_btn = tk.Button(password_row, text="🎲", font=('Arial', 10),
                               bg=ModernTheme.COLORS['bg_tertiary'],
                               fg=ModernTheme.COLORS['text_primary'],
                               relief='flat', cursor='hand2',
                               command=self.generate_password)
        generate_btn.pack(side='right', padx=(5, 0))
        
        # Steganography settings
        settings_row = tk.Frame(security_content, bg=ModernTheme.COLORS['bg_secondary'])
        settings_row.pack(fill='x', pady=10)
        
        tk.Label(settings_row, text="LSB Bits:", 
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_primary'],
                font=('Arial', 10)).pack(side='left')
        
        self.lsb_var = tk.StringVar(value="2")
        lsb_menu = ttk.Combobox(settings_row, textvariable=self.lsb_var,
                              values=["1", "2", "3", "4"], 
                              state="readonly", width=8)
        lsb_menu.pack(side='left', padx=10)
        
        # Capacity indicator
        self.capacity_ring = ProgressRing(security_content, size=80)
        self.capacity_ring.pack(anchor='e', pady=10)
        
        # Action buttons
        action_frame = tk.Frame(security_card, bg=ModernTheme.COLORS['bg_secondary'])
        action_frame.pack(fill='x', padx=15, pady=15)
        
        hide_btn = tk.Button(action_frame, text="🕵️ Hide Text", 
                           font=('Arial', 11, 'bold'),
                           bg=ModernTheme.COLORS['accent_primary'],
                           fg='white', relief='flat', cursor='hand2',
                           command=self.hide_text)
        hide_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        extract_btn = tk.Button(action_frame, text="🔍 Extract Text",
                              font=('Arial', 11, 'bold'),
                              bg=ModernTheme.COLORS['accent_secondary'],
                              fg='white', relief='flat', cursor='hand2',
                              command=self.extract_text)
        extract_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
        
        return container
        
    def create_file_tab(self):
        """Create modern file steganography tab"""
        container = tk.Frame(self.main_content, bg=ModernTheme.COLORS['bg_primary'])
        
        # Header
        header_frame = tk.Frame(container, bg=ModernTheme.COLORS['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="📁 File Steganography", 
                font=('Arial', 24, 'bold'),
                bg=ModernTheme.COLORS['bg_primary'],
                fg=ModernTheme.COLORS['text_primary']).pack(anchor='w')
        
        tk.Label(header_frame, text="Hide and extract files within images", 
                font=('Arial', 12),
                bg=ModernTheme.COLORS['bg_primary'],
                fg=ModernTheme.COLORS['text_secondary']).pack(anchor='w')
        
        # Coming soon content
        content_frame = tk.Frame(container, bg=ModernTheme.COLORS['bg_primary'])
        content_frame.pack(fill='both', expand=True)
        
        coming_soon_card = CardFrame(content_frame, title="🚀 Coming Soon")
        coming_soon_card.pack(fill='both', expand=True, padx=100, pady=100)
        
        tk.Label(coming_soon_card, text="📦 File Steganography", 
                font=('Arial', 20, 'bold'),
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_primary']).pack(pady=20)
        
        tk.Label(coming_soon_card, text="Hide documents, archives, and other files within images\n\nThis advanced feature will be available in the next update!",
                font=('Arial', 12),
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_secondary'],
                justify='center').pack(pady=10)
        
        return container
        
    def create_analysis_tab(self):
        """Create modern analysis tab"""
        container = tk.Frame(self.main_content, bg=ModernTheme.COLORS['bg_primary'])
        
        # Header
        header_frame = tk.Frame(container, bg=ModernTheme.COLORS['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="🔍 Image Analysis", 
                font=('Arial', 24, 'bold'),
                bg=ModernTheme.COLORS['bg_primary'],
                fg=ModernTheme.COLORS['text_primary']).pack(anchor='w')
        
        tk.Label(header_frame, text="Analyze images for steganography capacity and security", 
                font=('Arial', 12),
                bg=ModernTheme.COLORS['bg_primary'],
                fg=ModernTheme.COLORS['text_secondary']).pack(anchor='w')
        
        # Analysis content
        content_frame = tk.Frame(container, bg=ModernTheme.COLORS['bg_primary'])
        content_frame.pack(fill='both', expand=True)
        
        # Analysis controls
        controls_card = CardFrame(content_frame, title="🛠️ Analysis Tools")
        controls_card.pack(fill='x', pady=(0, 15))
        
        controls_frame = tk.Frame(controls_card, bg=ModernTheme.COLORS['bg_secondary'])
        controls_frame.pack(fill='x', padx=15, pady=15)
        
        analyze_btn = tk.Button(controls_frame, text="🔍 Run Comprehensive Analysis", 
                              font=('Arial', 11, 'bold'),
                              bg=ModernTheme.COLORS['accent_primary'],
                              fg='white', relief='flat', cursor='hand2',
                              command=self.run_analysis)
        analyze_btn.pack(side='left')
        
        # Results area
        results_card = CardFrame(content_frame, title="📊 Analysis Results")
        results_card.pack(fill='both', expand=True)
        
        self.analysis_text = scrolledtext.ScrolledText(results_card, wrap=tk.WORD,
                                                     bg=ModernTheme.COLORS['bg_tertiary'],
                                                     fg=ModernTheme.COLORS['text_primary'],
                                                     insertbackground=ModernTheme.COLORS['text_primary'],
                                                     borderwidth=0, font=('Consolas', 10))
        self.analysis_text.pack(fill='both', expand=True, padx=15, pady=15)
        self.analysis_text.insert('1.0', "Load an image and run analysis to see results...")
        
        return container
        
    def create_settings_tab(self):
        """Create modern settings tab"""
        container = tk.Frame(self.main_content, bg=ModernTheme.COLORS['bg_primary'])
        
        # Header
        header_frame = tk.Frame(container, bg=ModernTheme.COLORS['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="⚙️ Settings", 
                font=('Arial', 24, 'bold'),
                bg=ModernTheme.COLORS['bg_primary'],
                fg=ModernTheme.COLORS['text_primary']).pack(anchor='w')
        
        tk.Label(header_frame, text="Configure application preferences and security", 
                font=('Arial', 12),
                bg=ModernTheme.COLORS['bg_primary'],
                fg=ModernTheme.COLORS['text_secondary']).pack(anchor='w')
        
        # Settings content
        content_frame = tk.Frame(container, bg=ModernTheme.COLORS['bg_primary'])
        content_frame.pack(fill='both', expand=True)
        
        # Security settings
        security_card = CardFrame(content_frame, title="🔒 Security Settings")
        security_card.pack(fill='x', pady=(0, 15))
        
        security_content = tk.Frame(security_card, bg=ModernTheme.COLORS['bg_secondary'])
        security_content.pack(fill='x', padx=15, pady=15)
        
        # Add settings options here
        tk.Label(security_content, text="Security settings will be available in the next update",
                font=('Arial', 11),
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_secondary']).pack(pady=20)
        
        return container
        
    def create_status_bar(self):
        """Create modern status bar"""
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side='bottom', fill='x', padx=10, pady=5)
        
    # Navigation methods
    def show_text_tab(self):
        self.hide_all_tabs()
        self.text_tab_content.pack(fill='both', expand=True)
        self.update_nav_highlight(0)
        
    def show_file_tab(self):
        self.hide_all_tabs()
        self.file_tab_content.pack(fill='both', expand=True)
        self.update_nav_highlight(1)
        
    def show_analysis_tab(self):
        self.hide_all_tabs()
        self.analysis_tab_content.pack(fill='both', expand=True)
        self.update_nav_highlight(2)
        
    def show_settings_tab(self):
        self.hide_all_tabs()
        self.settings_tab_content.pack(fill='both', expand=True)
        self.update_nav_highlight(3)
        
    def hide_all_tabs(self):
        for tab in [self.text_tab_content, self.file_tab_content, 
                   self.analysis_tab_content, self.settings_tab_content]:
            tab.pack_forget()
            
    def update_nav_highlight(self, index):
        """Update navigation button highlights"""
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.configure(bg=ModernTheme.COLORS['accent_primary'])
            else:
                btn.configure(bg=ModernTheme.COLORS['bg_secondary'])

    # Core functionality methods (same as before, but with modern UI)
    def open_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path: str):
        self.current_image_path = file_path
        image = Image.open(file_path)
        
        # Update image info
        info_text = f"""📊 Image Information:

• File: {os.path.basename(file_path)}
• Dimensions: {image.size[0]} x {image.size[1]}
• Format: {image.format}
• Mode: {image.mode}
• Size: {os.path.getsize(file_path) / 1024:.1f} KB"""

        self.image_info_text.config(state='normal')
        self.image_info_text.delete('1.0', tk.END)
        self.image_info_text.insert('1.0', info_text)
        self.image_info_text.config(state='disabled')
        
        # Update capacity info
        self.update_capacity_info()
        
        # Update drop zone appearance
        self.drop_zone.icon_label.configure(text="✅")
        self.drop_zone.title_label.configure(text="Image Loaded")
        self.drop_zone.subtitle_label.configure(text=os.path.basename(file_path))

    def update_capacity_info(self):
        if self.current_image_path:
            try:
                analysis = self.stegano_engine.analyze_capacity(self.current_image_path)
                bits = int(self.lsb_var.get())
                capacity_info = analysis['capacity_analysis'][f'{bits}_bit_lsb']
                
                # Update progress ring
                used_kb = 1  # Placeholder - you'd calculate actual usage
                total_kb = capacity_info['kilobytes']
                percentage = min((used_kb / total_kb) * 100, 100) if total_kb > 0 else 0
                self.capacity_ring.set_progress(percentage)
                
            except Exception as e:
                self.capacity_ring.set_progress(0)

    def toggle_encryption(self):
        if self.encrypt_var.get():
            self.password_frame.pack(fill='x', pady=5)
        else:
            self.password_frame.pack_forget()

    def generate_password(self):
        try:
            password = self.crypto_manager.generate_secure_password()
            self.password_var.set(password)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {e}")

    def hide_text(self):
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        secret_text = self.text_input.get("1.0", tk.END).strip()
        if not secret_text:
            messagebox.showwarning("Warning", "Please enter text to hide")
            return
        
        try:
            password = self.password_var.get() if self.encrypt_var.get() else ""
            bits = int(self.lsb_var.get())
            
            stego_array, metadata = self.stegano_engine.embed_data_secure(
                self.current_image_path,
                secret_text.encode('utf-8'),
                password,
                bits
            )
            
            self.current_stego_image = Image.fromarray(stego_array)
            
            messagebox.showinfo("Success", 
                f"✅ Text hidden successfully!\n"
                f"Security: {'🔒 Encrypted' if password else '🔓 Not encrypted'}")
                
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to hide text: {e}")

    def extract_text(self):
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            password = self.password_var.get() if self.encrypt_var.get() else ""
            bits = int(self.lsb_var.get())
            
            extracted_data, metadata = self.stegano_engine.extract_data_secure(
                self.current_image_path,
                password,
                bits
            )
            
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", extracted_data.decode('utf-8'))
            
            messagebox.showinfo("Success", "✅ Text extracted successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to extract text: {e}")

    def save_stego_image(self):
        if not self.current_stego_image:
            messagebox.showwarning("Warning", "No stego image to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Stego Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        
        if file_path:
            try:
                self.current_stego_image.save(file_path)
                messagebox.showinfo("Success", f"✅ Image saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Failed to save image: {e}")

    def run_analysis(self):
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            analysis = self.stegano_engine.analyze_capacity(self.current_image_path)
            
            result_text = "=== 🕵️ IMAGE ANALYSIS REPORT ===\n\n"
            
            result_text += "📊 BASIC INFORMATION:\n"
            result_text += f"• Dimensions: {analysis['image_info']['dimensions']}\n"
            result_text += f"• Total Pixels: {analysis['image_info']['total_pixels']:,}\n"
            result_text += f"• Channels: {analysis['image_info']['channels']}\n\n"
            
            result_text += "💾 CAPACITY ANALYSIS:\n"
            for bits, info in analysis['capacity_analysis'].items():
                result_text += f"• {bits}: {info['kilobytes']} KB ({info['megabytes']} MB)\n"
            
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert("1.0", result_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Analysis failed: {e}")