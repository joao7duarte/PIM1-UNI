class Responsive:
    def on_window_resize(self, event):
            """Monitora o redimensionamento da janela."""
            if event.widget == self.root:
                new_width = event.width
                new_height = event.height
                
                if abs(new_width - self.current_width) > 50 or abs(new_height - self.current_height) > 30:
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

    def activate_mobile_mode(self):
        """Ativa o modo de layout para dispositivos móveis."""
        self.is_mobile_mode = True
        
        if hasattr(self, 'sidebar'):
            self.sidebar.pack_forget()
        if hasattr(self, 'menu_button'):
            self.menu_button.pack(side='left', padx=10, pady=15)
        
        if hasattr(self, 'tree'):
            self.tree.column('email', width=150)
            self.tree.column('nome', width=200)
            self.tree.column('idade', width=60)
            self.tree.column('nota', width=60)  

    def activate_desktop_mode(self):
        """Ativa o modo de layout para desktop."""
        self.is_mobile_mode = False
        
        if hasattr(self, 'menu_button'):
            self.menu_button.pack_forget()
        if hasattr(self, 'sidebar'):
            self.sidebar.pack(side='right', fill='y', padx=(0, 15))
            self.sidebar_visible = True
        
        if hasattr(self, 'tree'):
            self.tree.column('email', width=250)
            self.tree.column('nome', width=300)
            self.tree.column('idade', width=80)
            self.tree.column('nota', width=80) 
        
        if hasattr(self, 'title_label'):
            self.title_label.config(font=('Segoe UI', 26, 'bold'))