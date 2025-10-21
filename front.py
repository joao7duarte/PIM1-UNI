import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import tempfile
import time
import math
import sys

class StudentManagementSystem:
    """Sistema de Gestão Escolar com interface responsiva e integração com backend em C."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão Escolar")
        self.root.geometry("1400x800")
        self.root.configure(bg='#1e1e2e')
        self.root.minsize(900, 600)
        
        self.current_user = None
        self.sidebar_visible = True
        self.current_width = 1400
        self.current_height = 800
        self.is_mobile_mode = False
        self.student_logged_email = None
        
        self.root.bind('<Configure>', self.on_window_resize)
        self.setup_styles()
        self.create_login_interface()

    def setup_styles(self):
        """Configura os estilos visuais da aplicação."""
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

    def create_login_interface(self):
        """Cria a interface de login inicial."""
        self.clear_interface()
        
        login_frame = tk.Frame(self.root, bg=self.colors['secondary'])
        login_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        card = tk.Frame(login_frame, bg=self.colors['card_bg'], relief='flat')
        card.place(relx=0.5, rely=0.5, anchor='center', width=500, height=400)
        
        title = tk.Label(card, text="🎓 Sistema de Gestão Escolar",
                        font=('Segoe UI', 24, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=30)
        
        icon_label = tk.Label(card, text="🔐", font=('Segoe UI', 48),
                             bg=self.colors['card_bg'], fg=self.colors['primary'])
        icon_label.pack(pady=10)
        
        login_text = tk.Label(card,
                           text="Selecione o tipo de usuário para continuar:",
                           font=('Segoe UI', 12),
                           bg=self.colors['card_bg'],
                           fg=self.colors['text_light'])
        login_text.pack(pady=20)
        
        button_frame = tk.Frame(card, bg=self.colors['card_bg'])
        button_frame.pack(pady=20, padx=40, fill='x')
        
        # Botão Professor
        professor_btn = ttk.Button(button_frame, text="👨‍🏫 Entrar como Professor", 
                                  style='Primary.TButton',
                                  command=lambda: self.login_user('professor'))
        professor_btn.pack(fill='x', pady=10)
        
        # Botão Aluno
        aluno_btn = ttk.Button(button_frame, text="👨‍🎓 Entrar como Aluno", 
                              style='Success.TButton',
                              command=self.show_student_login)
        aluno_btn.pack(fill='x', pady=10)
        
        # Botão Sair
        sair_btn = ttk.Button(button_frame, text="❌ Sair do Sistema", 
                             style='Danger.TButton',
                             command=self.exit_system)
        sair_btn.pack(fill='x', pady=10)

    def show_student_login(self):
        """Mostra a tela de login específica para alunos."""
        self.clear_interface()
        
        login_frame = tk.Frame(self.root, bg=self.colors['secondary'])
        login_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        card = tk.Frame(login_frame, bg=self.colors['card_bg'], relief='flat')
        card.place(relx=0.5, rely=0.5, anchor='center', width=500, height=450)
        
        title = tk.Label(card, text="👨‍🎓 Login do Aluno",
                        font=('Segoe UI', 24, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=30)
        
        icon_label = tk.Label(card, text="🎓", font=('Segoe UI', 48),
                            bg=self.colors['card_bg'], fg=self.colors['primary'])
        icon_label.pack(pady=10)
        
        form_frame = tk.Frame(card, bg=self.colors['card_bg'])
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Campo de email
        tk.Label(form_frame, text="📧 Email do Aluno:", 
                bg=self.colors['card_bg'], fg=self.colors['text_light'],
                font=('Segoe UI', 11, 'bold'), anchor='w').pack(fill='x', pady=(10, 5))
        
        self.student_email_entry = ttk.Entry(form_frame, width=35, 
                                    font=('Segoe UI', 11), style='Modern.TEntry')
        self.student_email_entry.pack(fill='x', pady=5)
        self.student_email_entry.focus()
        
        # Botões
        button_frame = tk.Frame(card, bg=self.colors['card_bg'])
        button_frame.pack(pady=20, padx=40, fill='x')
        
        ttk.Button(button_frame, text="✅ Entrar", 
                style='Success.TButton',
                command=self.login_student).pack(fill='x', pady=10)
        
        # Adicione este botão para entrar sem verificação (para teste)
        ttk.Button(button_frame, text="👤 Entrar como Visitante", 
                style='Primary.TButton',
                command=lambda: self.direct_student_login()).pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="↩️ Voltar", 
                style='Warning.TButton',
              command=self.create_login_interface).pack(fill='x', pady=5)
    
    def login_student(self):
        """Realiza o login do aluno verificando se o email existe."""
        email = self.student_email_entry.get().strip()
        
        if not email:
            messagebox.showerror("Erro", "Por favor, digite seu email!")
            return
        
        # Verificar se o aluno existe no sistema
        success, result = self.execute_c_command('list')
        
        if success:
            if email.lower() in result.lower():
                self.current_user = 'aluno'
                self.student_logged_email = email  # Salvar email do aluno logado
                self.create_student_interface()
            else:
                messagebox.showerror("Erro", "Aluno não encontrado no sistema!\nVerifique o email digitado.")
        else:
            messagebox.showerror("Erro", f"Erro ao verificar aluno:\n{result}")

    def login_user(self, user_type):
        """Realiza o login do usuário."""
        self.current_user = user_type
        if user_type == 'professor':
            self.create_professor_interface()
        else:
            # Para aluno, vamos para a tela de login específica
            self.show_student_login()

    def logout(self):
        """Realiza logout e volta para a tela inicial."""
        self.current_user = None
        # Remover email do aluno se existir
        if hasattr(self, 'student_logged_email'):
            del self.student_logged_email
        self.create_login_interface()

    def exit_system(self):
        """Fecha o sistema."""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            self.root.quit()
            self.root.destroy()

    def create_professor_interface(self):
        """Cria a interface do professor."""
        self.clear_interface()
        
        header_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=100)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        self.menu_button = tk.Button(header_frame, text="☰", 
                                   bg=self.colors['primary'],
                                   fg=self.colors['text_dark'],
                                   font=('Segoe UI', 14, 'bold'),
                                   command=self.toggle_sidebar,
                                   borderwidth=0)
        self.menu_button.pack(side='left', padx=10, pady=15)
        
        self.title_label = ttk.Label(header_frame, text="👨‍🏫 Painel do Professor", style='Title.TLabel')
        self.title_label.pack(side='left', padx=20, pady=25)
        
        logout_btn = ttk.Button(header_frame, text="🚪 Sair", 
                               style='Danger.TButton',
                               command=self.logout)
        logout_btn.pack(side='right', padx=20, pady=25)
        
        main_container = tk.Frame(self.root, bg=self.colors['secondary'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_professor_sidebar(main_container)
        self.create_content_area(main_container)
        
        self.sidebar_visible = True

    def create_student_interface(self):
        """Cria a interface do aluno."""
        self.clear_interface()
        
        header_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=100)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Mostrar email do aluno logado
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

    def create_professor_sidebar(self, parent):
        """Cria o painel lateral do professor."""
        self.sidebar = tk.Frame(parent, bg=self.colors['dark'], width=280)
        self.sidebar.pack(side='left', fill='y', padx=(0, 15))
        self.sidebar.pack_propagate(False)
        
        main_content = tk.Frame(self.sidebar, bg=self.colors['dark'])
        main_content.pack(fill='both', expand=True, padx=20, pady=20, anchor='nw')
        
        sidebar_title = tk.Label(main_content, text="Menu do Professor", 
                                bg=self.colors['dark'], fg=self.colors['text_light'],
                                font=('Segoe UI', 16, 'bold'), anchor='w')
        sidebar_title.pack(fill='x', pady=(0, 25))
        
        buttons_data = [
            ("📝 Cadastrar Aluno", 'Primary.TButton', self.show_register_form),
            ("👥 Listar Alunos", 'Success.TButton', self.show_students_list),
            ("✏️ Editar Aluno", 'Warning.TButton', self.show_update_form),
            ("🗑️ Excluir Aluno", 'Danger.TButton', self.show_delete_form),
            ("📊 Lançar Nota", 'Primary.TButton', self.show_grade_form),
            ("📈 Dashboard", 'Success.TButton', self.show_statistics),
            ("🔄 Atualizar", 'Warning.TButton', self.refresh_system)
        ]
        
        for text, style, command in buttons_data:
            btn_frame = tk.Frame(main_content, bg=self.colors['dark'])
            btn_frame.pack(fill='x', pady=8, anchor='w')
            
            btn = ttk.Button(btn_frame, text=text, style=style, command=command)
            btn.pack(fill='x', anchor='w')

    def create_student_sidebar(self, parent):
        """Cria o painel lateral do aluno."""
        self.sidebar = tk.Frame(parent, bg=self.colors['dark'], width=280)
        self.sidebar.pack(side='left', fill='y', padx=(0, 15))
        self.sidebar.pack_propagate(False)
        
        main_content = tk.Frame(self.sidebar, bg=self.colors['dark'])
        main_content.pack(fill='both', expand=True, padx=20, pady=20, anchor='nw')
        
        sidebar_title = tk.Label(main_content, text="Menu do Aluno", 
                                bg=self.colors['dark'], fg=self.colors['text_light'],
                                font=('Segoe UI', 16, 'bold'), anchor='w')
        sidebar_title.pack(fill='x', pady=(0, 25))
        
        buttons_data = [
            ("📊 Ver Minhas Notas", 'Primary.TButton', self.show_student_grades),
            ("🏠 Voltar para Home", 'Success.TButton', self.show_student_home),
            ("🔄 Atualizar", 'Warning.TButton', self.refresh_system)
        ]
        
        for text, style, command in buttons_data:
            btn_frame = tk.Frame(main_content, bg=self.colors['dark'])
            btn_frame.pack(fill='x', pady=8, anchor='w')
            
            btn = ttk.Button(btn_frame, text=text, style=style, command=command)
            btn.pack(fill='x', anchor='w')

    def create_content_area(self, parent):
        """Cria a área de conteúdo principal."""
        self.content_frame = tk.Frame(parent, bg=self.colors['secondary'])
        self.content_frame.pack(side='left', fill='both', expand=True)
        
        self.welcome_frame = self.create_welcome_screen()
        self.register_frame = self.create_register_form()
        self.list_frame = self.create_students_list()
        self.update_frame = self.create_update_form()
        self.delete_frame = self.create_delete_form()
        self.grade_frame = self.create_grade_form()
        self.stats_frame = self.create_statistics()
        self.student_grades_frame = self.create_student_grades_view()
        
        self.show_frame(self.welcome_frame)

    def show_frame(self, frame_to_show):
        """Mostra um frame específico e esconde os outros."""
        frames = [self.welcome_frame, self.register_frame, self.list_frame, 
                 self.update_frame, self.delete_frame, self.grade_frame,
                 self.stats_frame, self.student_grades_frame]
        
        for frame in frames:
            frame.pack_forget()
        
        frame_to_show.pack(fill='both', expand=True)

    def clear_interface(self):
        """Limpa toda a interface atual."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_window_resize(self, event):
        """Atualiza o layout quando a janela é redimensionada."""
        if event.widget == self.root:
            new_width = event.width
            new_height = event.height
            
            if abs(new_width - self.current_width) > 50 or abs(new_height - self.current_height) > 30:
                self.current_width = new_width
                self.current_height = new_height
                self.update_responsive_layout()

    def update_responsive_layout(self):
        """Atualiza o layout baseado no tamanho atual da tela."""
        width = self.current_width
        
        if width < 1000:
            if not self.is_mobile_mode:
                self.activate_mobile_mode()
        else:
            if self.is_mobile_mode:
                self.activate_desktop_mode()

    def activate_mobile_mode(self):
        """Ativa o modo mobile com layout adaptado."""
        self.is_mobile_mode = True
        
        if hasattr(self, 'sidebar'):
            self.sidebar.pack_forget()
        if hasattr(self, 'menu_button'):
            self.menu_button.pack(side='left', padx=10, pady=15)
        
        if hasattr(self, 'tree'):
            self.tree.column('email', width=200)
            self.tree.column('nome', width=250)
            self.tree.column('idade', width=80)
        
        if hasattr(self, 'title_label'):
            self.title_label.config(font=('Segoe UI', 18, 'bold'))

    def activate_desktop_mode(self):
        """Ativa o modo desktop com layout completo."""
        self.is_mobile_mode = False
        
        if hasattr(self, 'menu_button'):
            self.menu_button.pack_forget()
        if hasattr(self, 'sidebar'):
            self.sidebar.pack(side='left', fill='y', padx=(0, 15))
            self.sidebar_visible = True
        
        if hasattr(self, 'tree'):
            self.tree.column('email', width=300)
            self.tree.column('nome', width=400)
            self.tree.column('idade', width=100)
        
        if hasattr(self, 'title_label'):
            self.title_label.config(font=('Segoe UI', 26, 'bold'))

    def toggle_sidebar(self):
        """Alterna a visibilidade do sidebar no modo mobile."""
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side='left', fill='y', padx=(0, 10))
            self.sidebar_visible = True

    # Métodos de funcionalidades do sistema
    def register_student(self):
        """Cadastra um novo aluno no sistema."""
        email = self.email_entry.get().strip()
        nome = self.name_entry.get().strip()
        idade = self.age_entry.get().strip()
        
        if not all([email, nome, idade]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        try:
            idade_int = int(idade)
            if idade_int < 0 or idade_int > 150:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser um número válido (0-150)!")
            return
        
        success, result = self.execute_c_command('add', email, nome, idade)
        
        if success and "cadastrado com sucesso" in result.lower():
            messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado com sucesso!")
            self.clear_form_fields()
        else:
            messagebox.showerror("Erro", f"Falha ao cadastrar aluno:\n{result}")

    def clear_form_fields(self):
        """Limpa os campos do formulário de cadastro."""
        self.email_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

    def load_students(self):
        """Carrega a lista de alunos do sistema."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        success, result = self.execute_c_command('list')
        
        if success:
            lines = result.split('\n')
            students_found = False
            
            for line in lines:
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        email = parts[0].split(':')[1].strip()
                        nome = parts[1].split(':')[1].strip()
                        idade = parts[2].split(':')[1].strip()
                        self.tree.insert('', tk.END, values=(email, nome, idade))
                        students_found = True
            
            if not students_found:
                self.tree.insert('', tk.END, values=("Nenhum aluno", "cadastrado", "no sistema"))
        else:
            self.tree.insert('', tk.END, values=("Erro ao", "carregar dados", result[:50]))

    def search_student(self):
        """Busca um aluno para atualização."""
        email = self.search_email_entry.get().strip()
        if not email:
            messagebox.showerror("Erro", "Digite um email para buscar!")
            return
        
        success, result = self.execute_c_command('list')
        
        if success:
            lines = result.split('\n')
            aluno_encontrado = False
            
            for line in lines:
                if '|' in line and email in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        nome = parts[1].split(':')[1].strip()
                        idade = parts[2].split(':')[1].strip()
                        
                        self.update_name_entry.delete(0, tk.END)
                        self.update_name_entry.insert(0, nome)
                        self.update_age_entry.delete(0, tk.END)
                        self.update_age_entry.insert(0, idade)
                        
                        self.update_form_frame.pack(pady=20, padx=50)
                        aluno_encontrado = True
                        break
            
            if aluno_encontrado:
                messagebox.showinfo("Sucesso", "Aluno encontrado! Preencha os novos dados.")
            else:
                messagebox.showerror("Erro", "Aluno não encontrado!")
        else:
            messagebox.showerror("Erro", f"Erro ao buscar aluno: {result}")

    def update_student(self):
        """Atualiza os dados de um aluno existente."""
        email = self.search_email_entry.get().strip()
        novo_nome = self.update_name_entry.get().strip()
        nova_idade = self.update_age_entry.get().strip()
        
        if not all([email, novo_nome, nova_idade]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        try:
            idade_int = int(nova_idade)
            if idade_int < 0 or idade_int > 150:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser um número válido!")
            return
        
        success, result = self.execute_c_command('update', email, novo_nome, nova_idade)
        
        if success and "atualizado com sucesso" in result.lower():
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
            self.search_email_entry.delete(0, tk.END)
            self.update_name_entry.delete(0, tk.END)
            self.update_age_entry.delete(0, tk.END)
            self.update_form_frame.pack_forget()
        else:
            messagebox.showerror("Erro", f"Falha ao atualizar aluno:\n{result}")

    def delete_student(self):
        """Exclui um aluno do sistema."""
        email = self.delete_email_entry.get().strip()
        if not email:
            messagebox.showerror("Erro", "Digite um email para excluir!")
            return
        
        if messagebox.askyesno("Confirmar Exclusão", 
                             f"Tem certeza que deseja excluir o aluno com email:\n{email}?\n\nEsta ação não pode ser desfeita!"):
            
            success, result = self.execute_c_command('delete', email)
            
            if success and "excluido com sucesso" in result.lower():
                messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
                self.delete_email_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", f"Falha ao excluir aluno:\n{result}")

    def assign_grade(self):
        """Atribui uma nota a um aluno."""
        email = self.grade_email_entry.get().strip()
        nota = self.grade_entry.get().strip()
        
        if not all([email, nota]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        try:
            nota_float = float(nota)
            if nota_float < 0 or nota_float > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Nota deve ser um número entre 0 e 10!")
            return
        
        success, result = self.execute_c_command('grade', email, nota)
        
        if success and "nota registrada" in result.lower():
            messagebox.showinfo("Sucesso", "Nota atribuída com sucesso!")
            self.grade_email_entry.delete(0, tk.END)
            self.grade_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", f"Falha ao atribuir nota:\n{result}")

    def show_student_grades(self):
        """Mostra as notas do aluno logado."""
        if hasattr(self, 'student_logged_email'):
            email = self.student_logged_email
        else:
            # Fallback para demonstração
            email = "aluno@escola.com"
        
        success, result = self.execute_c_command('view_grades', email)
        
        if success:
            self.student_grades_text.delete('1.0', tk.END)
            
            # Formatar a exibição das notas
            if "Sua nota é:" in result:
                self.student_grades_text.insert('1.0', f"📊 SUAS NOTAS\n\n")
                self.student_grades_text.insert(tk.END, f"👤 Aluno: {email}\n")
                self.student_grades_text.insert(tk.END, f"📧 Email: {email}\n\n")
                self.student_grades_text.insert(tk.END, "="*50 + "\n")
                self.student_grades_text.insert(tk.END, result)
            else:
                self.student_grades_text.insert('1.0', f"📊 SUAS NOTAS\n\n")
                self.student_grades_text.insert(tk.END, f"👤 Aluno: {email}\n")
                self.student_grades_text.insert(tk.END, f"📧 Email: {email}\n\n")
                self.student_grades_text.insert(tk.END, "="*50 + "\n")
                self.student_grades_text.insert(tk.END, "Nenhuma nota registrada para seu email.\n")
                self.student_grades_text.insert(tk.END, "Entre em contato com o professor.")
        else:
            messagebox.showerror("Erro", f"Falha ao carregar notas:\n{result}")

    def update_statistics(self):
        """Atualiza as estatísticas do sistema."""
        success, result = self.execute_c_command('list')
        
        if success:
            lines = result.split('\n')
            total_alunos = 0
            idades = []
            
            for line in lines:
                if '|' in line:
                    total_alunos += 1
                    parts = line.split('|')
                    if len(parts) >= 3:
                        try:
                            idade = int(parts[2].split(':')[1].strip())
                            idades.append(idade)
                        except ValueError:
                            continue
            
            if idades:
                idade_media = sum(idades) / len(idades)
                idade_min = min(idades)
                idade_max = max(idades)
            else:
                idade_media = idade_min = idade_max = 0
            
            stats = f"""=== DASHBOARD DO SISTEMA ===

📊 ESTATÍSTICAS GERAIS:
• Total de Alunos: {total_alunos}
• Idade Média: {idade_media:.1f} anos
• Aluno Mais Jovem: {idade_min} anos
• Aluno Mais Velho: {idade_max} anos

📈 DISTRIBUIÇÃO POR IDADE:"""
            
            faixas = {
                '17-20 anos': 0,
                '21-25 anos': 0,
                '26-30 anos': 0,
                '31+ anos': 0
            }
            
            for idade in idades:
                if 17 <= idade <= 20:
                    faixas['17-20 anos'] += 1
                elif 21 <= idade <= 25:
                    faixas['21-25 anos'] += 1
                elif 26 <= idade <= 30:
                    faixas['26-30 anos'] += 1
                else:
                    faixas['31+ anos'] += 1
            
            for faixa, quantidade in faixas.items():
                if total_alunos > 0:
                    percentual = (quantidade / total_alunos) * 100
                    stats += f"\n• {faixa}: {quantidade} alunos ({percentual:.1f}%)"
                else:
                    stats += f"\n• {faixa}: 0 alunos (0%)"
            
            stats += f"\n\n🔄 Última atualização: {time.strftime('%d/%m/%Y %H:%M:%S')}"
            
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', stats)
        else:
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', f"Erro ao carregar estatísticas:\n{result}")

    def execute_c_command(self, command, *args):
        """
        Executa comandos no sistema backend em C.
        
        Args:
            command: Comando a ser executado
            *args: Argumentos adicionais para o comando
            
        Returns:
            Tuple (success, result): Indica sucesso e contém o resultado
        """
        try:
            if not os.path.exists('system.exe'):
                compile_result = subprocess.run(['gcc', 'main.c', 'menualuno.c', 'menuprof.c', '-o', 'system.exe'], 
                                              capture_output=True, text=True)
                if compile_result.returncode != 0:
                    return False, f"Erro na compilação: {compile_result.stderr}"
            
            if command == 'list':
                result = subprocess.run(['system.exe'], input='1\n2\n0\n0\n', 
                                      capture_output=True, text=True, timeout=10)
                return True, result.stdout
            elif command == 'add':
                input_data = f'1\n1\n{args[0]}\n{args[1]}\n{args[2]}\n0\n0\n'
                result = subprocess.run(['system.exe'], input=input_data, 
                                      capture_output=True, text=True, timeout=10)
                return True, result.stdout
            elif command == 'update':
                input_data = f'1\n3\n{args[0]}\n{args[1]}\n{args[2]}\n0\n0\n'
                result = subprocess.run(['system.exe'], input=input_data, 
                                      capture_output=True, text=True, timeout=10)
                return True, result.stdout
            elif command == 'delete':
                input_data = f'1\n4\n{args[0]}\n0\n0\n'
                result = subprocess.run(['system.exe'], input=input_data, 
                                      capture_output=True, text=True, timeout=10)
                return True, result.stdout
            elif command == 'grade':
                input_data = f'1\n5\n{args[0]}\n{args[1]}\n0\n0\n'
                result = subprocess.run(['system.exe'], input=input_data, 
                                      capture_output=True, text=True, timeout=10)
                return True, result.stdout
            elif command == 'view_grades':
                input_data = f'2\n1\n{args[0]}\n0\n0\n'
                result = subprocess.run(['system.exe'], input=input_data, 
                                      capture_output=True, text=True, timeout=10)
                return True, result.stdout
            
        except subprocess.TimeoutExpired:
            return False, "Timeout: O sistema demorou muito para responder"
        except Exception as e:
            return False, f"Erro ao executar sistema: {str(e)}"
        
        return False, "Comando não reconhecido"

    # Métodos de criação de interfaces
    def create_welcome_screen(self):
        """Cria a tela de boas-vindas."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat', borderwidth=0)
        card.pack(expand=True, fill='both', padx=20, pady=20)
        
        if self.current_user == 'professor':
            welcome_title = "Bem-vindo, Professor!"
            icon = "👨‍🏫"
            description = "Sistema completo de gestão escolar com todas as funcionalidades administrativas."
        else:
            student_email = getattr(self, 'student_logged_email', 'Aluno')
            welcome_title = f"Bem-vindo, {student_email}!"
            icon = "👨‍🎓"
            description = "Acesse suas notas e informações acadêmicas.\n\nVocê pode visualizar suas notas atribuídas e voltar para esta tela inicial."
        
        welcome_title_label = tk.Label(card, 
                                text=welcome_title,
                                font=('Segoe UI', 24, 'bold'),
                                bg=self.colors['card_bg'],
                                fg=self.colors['text_light'])
        welcome_title_label.pack(pady=30)
        
        icon_label = tk.Label(card, text=icon, font=('Segoe UI', 48),
                             bg=self.colors['card_bg'], fg=self.colors['primary'])
        icon_label.pack(pady=10)
        
        welcome_text = tk.Label(card,
                               text=description,
                               font=('Segoe UI', 11),
                               bg=self.colors['card_bg'],
                               fg=self.colors['text_light'],
                               justify='center')
        welcome_text.pack(pady=20, padx=40)
        
        return frame

    def create_register_form(self):
        """Cria o formulário de cadastro de alunos."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title = tk.Label(card, text="📝 Cadastrar Novo Aluno",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=20)
        
        form_container = tk.Frame(card, bg=self.colors['card_bg'])
        form_container.pack(expand=True, pady=15)
        
        form_frame = tk.Frame(form_container, bg=self.colors['card_bg'])
        form_frame.pack(pady=15, padx=40)
        
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=2)
        
        tk.Label(form_frame, text="📧 Email do Aluno:", bg=self.colors['card_bg'], 
                fg=self.colors['text_light'], font=('Segoe UI', 11, 'bold'),
                anchor='w').grid(row=0, column=0, sticky='w', pady=12, padx=(0, 15))
        
        self.email_entry = ttk.Entry(form_frame, width=35, font=('Segoe UI', 11), style='Modern.TEntry')
        self.email_entry.grid(row=0, column=1, sticky='ew', pady=12)
        
        tk.Label(form_frame, text="👤 Nome Completo:", bg=self.colors['card_bg'],
                fg=self.colors['text_light'], font=('Segoe UI', 11, 'bold'),
                anchor='w').grid(row=1, column=0, sticky='w', pady=12, padx=(0, 15))
        
        self.name_entry = ttk.Entry(form_frame, width=35, font=('Segoe UI', 11), style='Modern.TEntry')
        self.name_entry.grid(row=1, column=1, sticky='ew', pady=12)
        
        tk.Label(form_frame, text="🎂 Idade:", bg=self.colors['card_bg'],
                fg=self.colors['text_light'], font=('Segoe UI', 11, 'bold'),
                anchor='w').grid(row=2, column=0, sticky='w', pady=12, padx=(0, 15))
        
        self.age_entry = ttk.Entry(form_frame, width=35, font=('Segoe UI', 11), style='Modern.TEntry')
        self.age_entry.grid(row=2, column=1, sticky='ew', pady=12)
        
        button_frame = tk.Frame(card, bg=self.colors['card_bg'])
        button_frame.pack(pady=20)
        
        register_btn = ttk.Button(button_frame, text="🎯 Cadastrar Aluno", 
                                 style='Primary.TButton',
                                 command=self.register_student)
        register_btn.pack(pady=10)
        
        return frame

    def create_students_list(self):
        """Cria a interface de listagem de alunos."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title = tk.Label(card, text="👥 Lista de Alunos Cadastrados",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=15)
        
        tree_frame = tk.Frame(card, bg=self.colors['card_bg'])
        tree_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        columns = ('email', 'nome', 'idade')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=18)
        
        self.tree.heading('email', text='📧 Email')
        self.tree.heading('nome', text='👤 Nome Completo')
        self.tree.heading('idade', text='🎂 Idade')
        
        self.tree.column('email', width=300)
        self.tree.column('nome', width=400)
        self.tree.column('idade', width=100)
        
        style = ttk.Style()
        style.configure("Treeview", 
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_light'],
                       fieldbackground=self.colors['card_bg'],
                       font=('Segoe UI', 10))
        
        style.configure("Treeview.Heading",
                      background=self.colors['primary'],
                      foreground=self.colors['text_dark'],
                      font=('Segoe UI', 11, 'bold'))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        return frame

    def create_update_form(self):
        """Cria o formulário de atualização de alunos."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title = tk.Label(card, text="✏️ Atualizar Dados do Aluno",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=20)
        
        search_frame = tk.Frame(card, bg=self.colors['card_bg'])
        search_frame.pack(pady=15, padx=40, fill='x')
        
        tk.Label(search_frame, text="🔍 Buscar por Email:", bg=self.colors['card_bg'],
                fg=self.colors['text_light'], font=('Segoe UI', 11, 'bold'),
                anchor='w').pack(side='left', padx=(0, 15))
        
        self.search_email_entry = ttk.Entry(search_frame, width=30, font=('Segoe UI', 11), style='Modern.TEntry')
        self.search_email_entry.pack(side='left', fill='x', expand=True)
        
        search_btn = ttk.Button(search_frame, text="🔎 Buscar Aluno", 
                               style='Primary.TButton',
                               command=self.search_student)
        search_btn.pack(side='right', padx=(15, 0))
        
        self.update_form_frame = tk.Frame(card, bg=self.colors['card_bg'])
        
        tk.Label(self.update_form_frame, text="👤 Novo Nome:", bg=self.colors['card_bg'],
                fg=self.colors['text_light'], font=('Segoe UI', 11, 'bold'),
                anchor='w').grid(row=0, column=0, sticky='w', pady=12, padx=(0, 15))
        
        self.update_name_entry = ttk.Entry(self.update_form_frame, width=30, font=('Segoe UI', 11), style='Modern.TEntry')
        self.update_name_entry.grid(row=0, column=1, sticky='ew', pady=12)
        
        tk.Label(self.update_form_frame, text="🎂 Nova Idade:", bg=self.colors['card_bg'],
                fg=self.colors['text_light'], font=('Segoe UI', 11, 'bold'),
                anchor='w').grid(row=1, column=0, sticky='w', pady=12, padx=(0, 15))
        
        self.update_age_entry = ttk.Entry(self.update_form_frame, width=30, font=('Segoe UI', 11), style='Modern.TEntry')
        self.update_age_entry.grid(row=1, column=1, sticky='ew', pady=12)
        
        update_btn = ttk.Button(self.update_form_frame, text="💾 Atualizar Dados", 
                               style='Success.TButton',
                               command=self.update_student)
        update_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        return frame

    def create_delete_form(self):
        """Cria o formulário de exclusão de alunos."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title = tk.Label(card, text="🗑️ Excluir Aluno",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=20)
        
        form_frame = tk.Frame(card, bg=self.colors['card_bg'])
        form_frame.pack(pady=15, padx=40)
        
        tk.Label(form_frame, text="📧 Email do Aluno a Excluir:", bg=self.colors['card_bg'],
                fg=self.colors['text_light'], font=('Segoe UI', 11, 'bold'),
                anchor='w').grid(row=0, column=0, sticky='w', pady=12, padx=(0, 15))
        
        self.delete_email_entry = ttk.Entry(form_frame, width=35, font=('Segoe UI', 11), style='Modern.TEntry')
        self.delete_email_entry.grid(row=0, column=1, sticky='ew', pady=12)
        
        button_frame = tk.Frame(card, bg=self.colors['card_bg'])
        button_frame.pack(pady=20)
        
        delete_btn = ttk.Button(button_frame, text="⚠️ Excluir Aluno", 
                               style='Danger.TButton',
                               command=self.delete_student)
        delete_btn.pack(pady=10)
        
        return frame

    def create_grade_form(self):
        """Cria o formulário para lançar notas."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title = tk.Label(card, text="📊 Lançar Nota",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=20)
        
        form_frame = tk.Frame(card, bg=self.colors['card_bg'])
        form_frame.pack(pady=15, padx=40)
        
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=2)
        
        tk.Label(form_frame, text="📧 Email do Aluno:", bg=self.colors['card_bg'],
                fg=self.colors['text_light'], font=('Segoe UI', 11, 'bold'),
                anchor='w').grid(row=0, column=0, sticky='w', pady=12, padx=(0, 15))
        
        self.grade_email_entry = ttk.Entry(form_frame, width=35, font=('Segoe UI', 11), style='Modern.TEntry')
        self.grade_email_entry.grid(row=0, column=1, sticky='ew', pady=12)
        
        tk.Label(form_frame, text="📝 Nota (0-10):", bg=self.colors['card_bg'],
                fg=self.colors['text_light'], font=('Segoe UI', 11, 'bold'),
                anchor='w').grid(row=1, column=0, sticky='w', pady=12, padx=(0, 15))
        
        self.grade_entry = ttk.Entry(form_frame, width=35, font=('Segoe UI', 11), style='Modern.TEntry')
        self.grade_entry.grid(row=1, column=1, sticky='ew', pady=12)
        
        button_frame = tk.Frame(card, bg=self.colors['card_bg'])
        button_frame.pack(pady=20)
        
        grade_btn = ttk.Button(button_frame, text="🎯 Lançar Nota", 
                              style='Primary.TButton',
                              command=self.assign_grade)
        grade_btn.pack(pady=10)
        
        return frame

    def create_statistics(self):
        """Cria a interface de estatísticas."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title = tk.Label(card, text="📈 Dashboard do Sistema",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=15)
        
        self.stats_text = scrolledtext.ScrolledText(card, 
                                                   wrap=tk.WORD,
                                                   width=80,
                                                   height=25,
                                                   font=('Consolas', 10),
                                                   bg=self.colors['dark'],
                                                   fg=self.colors['text_light'],
                                                   relief='flat')
        self.stats_text.pack(fill='both', expand=True, padx=15, pady=10)
        
        return frame

    def create_student_grades_view(self):
        """Cria a visualização de notas para alunos."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title = tk.Label(card, text="📊 Minhas Notas",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=15)
        
        self.student_grades_text = scrolledtext.ScrolledText(card, 
                                                           wrap=tk.WORD,
                                                           width=80,
                                                           height=25,
                                                           font=('Consolas', 10),
                                                           bg=self.colors['dark'],
                                                           fg=self.colors['text_light'],
                                                           relief='flat')
        self.student_grades_text.pack(fill='both', expand=True, padx=15, pady=10)
        
        return frame

    # Métodos de navegação
    def show_register_form(self):
        """Mostra o formulário de cadastro."""
        self.show_frame(self.register_frame)
        self.title_label.config(text="📝 Cadastrar Aluno")

    def show_students_list(self):
        """Mostra a lista de alunos."""
        self.show_frame(self.list_frame)
        self.title_label.config(text="👥 Lista de Alunos")
        self.load_students()

    def show_update_form(self):
        """Mostra o formulário de atualização."""
        self.show_frame(self.update_frame)
        self.title_label.config(text="✏️ Atualizar Aluno")
        self.update_form_frame.pack_forget()

    def show_delete_form(self):
        """Mostra o formulário de exclusão."""
        self.show_frame(self.delete_frame)
        self.title_label.config(text="🗑️ Excluir Aluno")

    def show_grade_form(self):
        """Mostra o formulário de lançar notas."""
        self.show_frame(self.grade_frame)
        self.title_label.config(text="📊 Lançar Nota")

    def show_statistics(self):
        """Mostra as estatísticas do sistema."""
        self.show_frame(self.stats_frame)
        self.title_label.config(text="📈 Dashboard")
        self.update_statistics()

    def show_student_home(self):
        """Mostra a tela inicial do aluno."""
        self.show_frame(self.welcome_frame)
        self.title_label.config(text=f"👨‍🎓 Painel do Aluno - {getattr(self, 'student_logged_email', 'Aluno')}")

    def refresh_system(self):
        """Atualiza o sistema."""
        if self.current_user == 'professor':
            if self.list_frame.winfo_ismapped():
                self.load_students()
            elif self.stats_frame.winfo_ismapped():
                self.update_statistics()
            messagebox.showinfo("Sucesso", "Sistema atualizado!")
        else:
            if self.student_grades_frame.winfo_ismapped():
                self.show_student_grades()
            messagebox.showinfo("Sucesso", "Dados atualizados!")

    

def main():
    """Função principal que inicia a aplicação."""
    try:
        root = tk.Tk()
        app = StudentManagementSystem(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        messagebox.showerror("Erro", f"Falha ao iniciar sistema:\n{e}")

if __name__ == "__main__":
    main()