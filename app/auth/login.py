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
            
            alunos_cadastrados = self.check_students_exist()
            
            if alunos_cadastrados:
                aluno_btn = ttk.Button(button_frame, text="👨‍🎓 Entrar como Aluno", 
                                    style='Success.TButton',
                                    command=self.show_student_login)
                aluno_btn.pack(**button_config)
            else:
                aluno_btn = ttk.Button(button_frame, text="👨‍🎓 Entrar como Aluno (Nenhum aluno cadastrado)", 
                                    style='Danger.TButton',
                                    state='disabled',
                                    command=self.show_student_login)
                aluno_btn.pack(**button_config)
                self.create_tooltip(aluno_btn, "Não há alunos cadastrados no sistema. O professor deve cadastrar alunos primeiro.")
            
            sair_btn = ttk.Button(button_frame, text="❌ Sair do Sistema", 
                                style='Danger.TButton',
                                command=self.exit_system)
            sair_btn.pack(**button_config)
            
            self.root.update()

    def check_students_exist(self):
        """Verifica se existem alunos cadastrados no sistema."""
        try:
            import os
            if os.path.exists('database/alunos.txt'):
                with open('database/alunos.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and ';' in line:
                            parts = line.split(';')
                            if len(parts) >= 4:
                                for part in parts:
                                    if '@' in part and '.' in part:
                                        return True
            return False
        except:
            return False

    def create_tooltip(self, widget, text):
        """Cria um tooltip para widgets desabilitados."""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, background="yellow", 
                           relief='solid', borderwidth=1, font=('Segoe UI', 9))
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def show_student_login(self):
        """Exibe o formulário de login para alunos."""
        if not self.check_students_exist():
            messagebox.showerror("Acesso Bloqueado", 
                               "Não há alunos cadastrados no sistema!\n\n"
                               "O professor deve cadastrar alunos primeiro "
                               "antes que possam fazer login.")
            return
            
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
        
        email_exists = self.check_email_exists(email)
        
        if not email_exists:
            messagebox.showerror("Acesso Negado", 
                               "Email não encontrado no sistema!\n\n"
                               "Verifique se:\n"
                               "• O email está correto\n"
                               "• Você está cadastrado no sistema\n"
                               "• O professor realizou seu cadastro")
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

    def check_email_exists(self, email):
        """Verifica se um email específico existe no sistema."""
        try:
            import os
            if os.path.exists('database/alunos.txt'):
                with open('database/alunos.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and ';' in line:
                            parts = line.split(';')
                            for part in parts:
                                if part.strip() == email:
                                    return True
            return False
        except:
            return False

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