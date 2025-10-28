class Responsive:
    def on_window_resize(self, event):
        """Monitora o redimensionamento da janela."""
        if event.widget == self.root and event.width > 50 and event.height > 50:
            if event.widget == self.root:
                new_width = event.width
                new_height = event.height
            
                self.current_width = new_width
                self.current_height = new_height
                self.update_responsive_layout()

    def update_responsive_layout(self):
        """Atualiza o layout baseado no tamanho da tela."""
        width = self.current_width
        
        if width < 1000:
            if not self.is_mobile_mode:
                self.activate_mobile_mode()
        else:
            if self.is_mobile_mode:
                self.activate_desktop_mode()

        self.adjust_dynamic_elements()

    def adjust_dynamic_elements(self):
        """Ajusta elementos específicos baseado no tamanho atual."""
        width = self.current_width
        
        if hasattr(self, 'title_label'):
            if width < 1000:
                self.title_label.config(font=('Segoe UI', 20, 'bold'))
            else:
                self.title_label.config(font=('Segoe UI', 26, 'bold'))
        
        if hasattr(self, 'tree'):
            if width < 1000:
                self.tree.column('email', width=120)
                self.tree.column('nome', width=150)
                self.tree.column('idade', width=50)
                self.tree.column('nota', width=50)
            elif width < 1200:
                self.tree.column('email', width=180)
                self.tree.column('nome', width=220)
                self.tree.column('idade', width=70)
                self.tree.column('nota', width=70)
            else:
                self.tree.column('email', width=250)
                self.tree.column('nome', width=300)
                self.tree.column('idade', width=80)
                self.tree.column('nota', width=80)

        self.ensure_menu_button_visible()

    def ensure_menu_button_visible(self):
        """Garante que o botão do menu esteja sempre visível."""
        if hasattr(self, 'menu_button'):
            if not self.menu_button.winfo_ismapped():
                self.menu_button.pack(side='left', padx=10, pady=15)
            
            if self.is_mobile_mode:
                self.menu_button.config(bg=self.colors['primary'], fg=self.colors['text_dark'])
            else:
                self.menu_button.config(bg=self.colors['primary'], fg=self.colors['text_dark'])

    def initialize_responsive(self):
            """Inicializa o sistema responsivo após a janela ser renderizada."""
            self.current_width = self.root.winfo_width()
            self.current_height = self.root.winfo_height()
            self.update_responsive_layout()

    def activate_mobile_mode(self):
        """Ativa o modo de layout para dispositivos móveis."""
        self.is_mobile_mode = True
        
        if hasattr(self, 'sidebar') and self.sidebar.winfo_ismapped():
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        
        if hasattr(self, 'menu_button'):
            if not self.menu_button.winfo_ismapped():
                self.menu_button.pack(side='left', padx=10, pady=15)
        
        if hasattr(self, 'content_frame'):
            self.content_frame.configure(padx=5)

    def activate_desktop_mode(self):
        """Ativa o modo de layout para desktop."""
        self.is_mobile_mode = False

        if hasattr(self, 'menu_button') and self.menu_button.winfo_ismapped():
            self.menu_button.pack_forget()
        
        if hasattr(self, 'sidebar') and not self.sidebar.winfo_ismapped() and self.sidebar_visible:
            self.sidebar.pack(side='right', fill='y', padx=(0, 15))
        
        if hasattr(self, 'content_frame'):
            self.content_frame.configure(padx=10)
     
