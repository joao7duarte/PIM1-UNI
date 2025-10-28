import tkinter as tk
from tkinter import ttk

def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        self.colors = {
            'primary': '#89b4fa',
            'secondary': '#1e1e2e',
            'success': '#a6e3a1',
            'warning': '#f9e2af',
            'danger': '#f38ba8',
            'light': '#cdd6f4',
            'dark': '#181825',
            'card_bg': '#313244',
            'text_light': '#cdd6f4',
            'text_dark': '#1e1e2e'
        }
        
        style.configure('Primary.TButton', 
                       background=self.colors['primary'],
                       foreground=self.colors['text_dark'],
                       padding=(25, 12),
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['text_dark'],
                       padding=(25, 12),
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground=self.colors['text_dark'],
                       padding=(25, 12),
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground=self.colors['text_dark'],
                       padding=(25, 12),
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)
        
        style.configure('Title.TLabel',
                       background=self.colors['secondary'],
                       foreground=self.colors['text_light'],
                       font=('Segoe UI', 26, 'bold'))
        
        style.configure('Card.TFrame',
                       background=self.colors['card_bg'],
                       relief='flat',
                       borderwidth=0)

        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['card_bg'],
                       foreground=self.colors['text_light'],
                       borderwidth=2,
                       relief='flat',
                       padding=(10, 8))
