import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class Student():
    def create_student_interface(self):
        """Cria a interface principal do aluno."""
        self.clear_interface()
        
        header_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=100)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        self.menu_button = tk.Button(header_frame, text="☰", 
                                    bg=self.colors['primary'],
                                    fg=self.colors['text_dark'],
                                    font=('Segoe UI', 14, 'bold'),
                                    command=self.toggle_sidebar,
                                    borderwidth=0,
                                    width=4,
                                    height=1)
        self.menu_button.pack(side='left', padx=10, pady=15)
        
        student_email = getattr(self, 'student_logged_email', 'Aluno')
        self.title_label = ttk.Label(header_frame, 
                                    text=f"👨‍🎓 Painel do Aluno - {student_email}", 
                                    style='Title.TLabel')
        self.title_label.pack(side='left', padx=20, pady=25)
        
        logout_btn = ttk.Button(header_frame, text="🚪 Sair", 
                                style='Danger.TButton',
                                command=self.logout)
        logout_btn.pack(side='right', padx=20, pady=25)
        
        main_container = tk.Frame(self.root, bg=self.colors['secondary'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_student_sidebar(main_container)
        self.create_content_area(main_container)
        
        self.root.after(100, self.update_responsive_layout)
    
    def create_student_sidebar(self, parent):
        """Cria o menu lateral do aluno."""
        self.sidebar = tk.Frame(parent, bg=self.colors['dark'], width=280)
        self.sidebar.pack(side='right', fill='y', padx=(0, 15))
        self.sidebar.pack_propagate(False)
        
        main_content = tk.Frame(self.sidebar, bg=self.colors['dark'])
        main_content.pack(fill='both', expand=True, padx=20, pady=20, anchor='nw')
        
        sidebar_title = tk.Label(main_content, text="Menu do Aluno", 
                                bg=self.colors['dark'], fg=self.colors['text_light'],
                                font=('Segoe UI', 16, 'bold'), anchor='w')
        sidebar_title.pack(fill='x', pady=(0, 25))
        
        buttons_data = [
            ("📊 Ver Minhas Notas", 'Primary.TButton', self.show_student_grades_view),
            ("🏠 Voltar para Home", 'Success.TButton', self.show_student_home)
        ]
        
        for text, style, command in buttons_data:
            btn_frame = tk.Frame(main_content, bg=self.colors['dark'])
            btn_frame.pack(fill='x', pady=8, anchor='w')
            
            btn = ttk.Button(btn_frame, text=text, style=style, command=command)
            btn.pack(fill='x', anchor='w')

    def show_student_home(self):
        """Exibe a tela inicial do aluno."""
        self.show_frame(self.welcome_frame)



    def show_student_grades_view(self):
        """Exibe a visualização de notas do aluno."""
        self.show_student_grades()
        self.show_frame(self.student_grades_frame)

    def create_student_grades_view(self):
        """Cria a interface de visualização de notas."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title_frame = tk.Frame(card, bg=self.colors['card_bg'])
        title_frame.pack(fill='x', pady=15)
        
        title = tk.Label(title_frame, text="📊 Minhas Notas",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(side='left', padx=20)
        
        refresh_btn = ttk.Button(title_frame, text="🔄 Atualizar Notas",
                                style='Primary.TButton',
                                command=self.show_student_grades)
        refresh_btn.pack(side='right', padx=20)
        
        text_frame = tk.Frame(card, bg=self.colors['card_bg'])
        text_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        self.student_grades_text = scrolledtext.ScrolledText(text_frame, 
                                                            wrap=tk.WORD,
                                                            font=('Consolas', 11),
                                                            bg=self.colors['dark'],
                                                            fg=self.colors['text_light'],
                                                            padx=15, pady=15)
        self.student_grades_text.pack(fill='both', expand=True)
        
        return frame

    def show_student_grades(self):
        """Carrega e exibe as notas do aluno logado."""
        if hasattr(self, 'student_logged_email'):
            email = self.student_logged_email
        else:
            messagebox.showerror("Erro", "Email do aluno não identificado!")
            return
        
        success, result = self.execute_c_command('view_grades', email)
        
        if success:
            self.student_grades_text.delete('1.0', tk.END)
            
            # CORREÇÃO: Verificar de forma mais abrangente se há nota
            if "Sua nota é:" in result or "Nota não lançada" in result or "Aluno não encontrado" in result:
                self.student_grades_text.insert('1.0', f"📊 SUAS NOTAS\n\n")
                self.student_grades_text.insert(tk.END, f"👤 Aluno: {email}\n")
                self.student_grades_text.insert(tk.END, f"📧 Email: {email}\n\n")
                self.student_grades_text.insert(tk.END, "="*50 + "\n")
                
                # Extrair apenas a parte relevante da resposta
                lines = result.split('\n')
                for line in lines:
                    if "Sua nota é:" in line or "Nota não lançada" in line or "Aluno não encontrado" in line or "Nenhuma nota registrada" in line:
                        self.student_grades_text.insert(tk.END, f"{line}\n")
                
                # Se não encontrou nenhuma das mensagens esperadas, mostrar resultado completo
                if "Sua nota é:" not in result and "Nota não lançada" not in result:
                    self.student_grades_text.insert(tk.END, f"\nResposta do sistema:\n{result}")
            else:
                self.student_grades_text.insert('1.0', f"📊 SUAS NOTAS\n\n")
                self.student_grades_text.insert(tk.END, f"👤 Aluno: {email}\n")
                self.student_grades_text.insert(tk.END, f"📧 Email: {email}\n\n")
                self.student_grades_text.insert(tk.END, "="*50 + "\n")
                self.student_grades_text.insert(tk.END, "Nenhuma nota registrada para seu email.\n")
                self.student_grades_text.insert(tk.END, "Entre em contato com o professor.")
        else:
            messagebox.showerror("Erro", f"Falha ao carregar notas:\n{result}")
            
