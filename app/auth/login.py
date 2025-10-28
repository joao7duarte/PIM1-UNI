import tkinter as tk
from tkinter import ttk, messagebox

class Login():
    def create_login_interface(self):
            """Cria a interface inicial de login do sistema."""
            self.clear_interface()
            
            main_container = tk.Frame(self.root, bg=self.colors['secondary'])
            main_container.pack(fill='both', expand=True)
            
            center_frame = tk.Frame(main_container, bg=self.colors['secondary'])
            center_frame.place(relx=0.5, rely=0.5, anchor='center')
            
            card = tk.Frame(center_frame, bg=self.colors['card_bg'], relief='flat', 
                        width=500, height=450)  
            card.pack_propagate(False)
            card.pack(padx=20, pady=20)
            
            title = tk.Label(card, text="🎓 Sistema de Gestão Escolar",
                            font=('Segoe UI', 20, 'bold'), 
                            bg=self.colors['card_bg'],
                            fg=self.colors['text_light'])
            title.pack(pady=20)  
            
            icon_label = tk.Label(card, text="🔐", font=('Segoe UI', 36), 
                                bg=self.colors['card_bg'], fg=self.colors['primary'])
            icon_label.pack(pady=5)  
            
            login_text = tk.Label(card,
                            text="Selecione o tipo de usuário para continuar:",
                            font=('Segoe UI', 11),
                            bg=self.colors['card_bg'],
                            fg=self.colors['text_light'])
            login_text.pack(pady=12) 

            button_frame = tk.Frame(card, bg=self.colors['card_bg'])
            button_frame.pack(pady=15, padx=40, fill='both', expand=True)  
            
            button_config = {
                'fill': 'x',
                'pady': 5,  
                'ipady': 7 
            }
            
            professor_btn = ttk.Button(button_frame, text="👨‍🏫 Entrar como Professor", 
                                    style='Primary.TButton',
                                    command=lambda: self.login_user('professor'))
            professor_btn.pack(**button_config)
            
            aluno_btn = ttk.Button(button_frame, text="👨‍🎓 Entrar como Aluno", 
                                style='Success.TButton',
                                command=self.show_student_login)
            aluno_btn.pack(**button_config)
            
            sair_btn = ttk.Button(button_frame, text="❌ Sair do Sistema", 
                                style='Danger.TButton',
                                command=self.exit_system)
            sair_btn.pack(**button_config)
            
            self.root.update()

    def show_student_login(self):
        """Exibe o formulário de login para alunos."""
        self.clear_interface()
        
        login_frame = tk.Frame(self.root, bg=self.colors['secondary'])
        login_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        card = tk.Frame(login_frame, bg=self.colors['card_bg'], relief='flat')
        card.place(relx=0.5, rely=0.5, anchor='center', width=500, height=500)  
        
        title = tk.Label(card, text="👨‍🎓 Login do Aluno",
                        font=('Segoe UI', 24, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=25)  
        
        icon_label = tk.Label(card, text="🎓", font=('Segoe UI', 48),
                            bg=self.colors['card_bg'], fg=self.colors['primary'])
        icon_label.pack(pady=10)
        
        form_frame = tk.Frame(card, bg=self.colors['card_bg'])
        form_frame.pack(pady=15, padx=40, fill='x') 
        
        tk.Label(form_frame, text="📧 Email do Aluno:", 
                bg=self.colors['card_bg'], fg=self.colors['text_light'],
                font=('Segoe UI', 11, 'bold'), anchor='w').pack(fill='x', pady=(10, 5))
        
        self.student_email_entry = ttk.Entry(form_frame, width=35, 
                                    font=('Segoe UI', 11), style='Modern.TEntry')
        self.student_email_entry.pack(fill='x', pady=5)
        self.student_email_entry.focus()
        
        button_frame = tk.Frame(card, bg=self.colors['card_bg'])
        button_frame.pack(pady=20, padx=40, fill='x')  
        
        ttk.Button(button_frame, text="✅ Entrar", 
                style='Success.TButton',
                command=self.login_student).pack(fill='x', pady=8)  
        
        ttk.Button(button_frame, text="↩️ Voltar", 
                style='Warning.TButton',
                command=self.create_login_interface).pack(fill='x', pady=8)

    def login_student(self):
        """Autentica um aluno usando email."""
        email = self.student_email_entry.get().strip()
        
        if not email:
            messagebox.showerror("Erro", "Por favor, digite seu email!")
            return
        
        success, result = self.execute_c_command('list')
        
        if success:
            if email.lower() in result.lower():
                self.current_user = 'aluno'
                self.student_logged_email = email
                self.create_student_interface()
            else:
                messagebox.showerror("Erro", "Aluno não encontrado no sistema!")
        else:
            messagebox.showerror("Erro", f"Erro ao verificar aluno:\n{result}")

    def login_user(self, user_type):
        """Realiza login para um tipo específico de usuário."""
        self.current_user = user_type
        if user_type == 'professor':
            self.create_professor_interface()
        else:
            self.show_student_login()

    def logout(self):
        """Realiza logout do usuário atual."""
        self.current_user = None
        if hasattr(self, 'student_logged_email'):
            del self.student_logged_email
        self.create_login_interface()

    def exit_system(self):
        """Fecha o sistema com confirmação."""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            self.root.quit()
            self.root.destroy()
    

