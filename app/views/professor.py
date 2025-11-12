import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time

class Professor():
    def create_professor_interface(self):
        """Cria a interface principal do professor."""
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
        
        if self.current_width < 1000:
            self.menu_button.pack(side='left', padx=10, pady=15)
        
        self.title_label = ttk.Label(header_frame, text="👨‍🏫 Painel do Professor", style='Title.TLabel')
        self.title_label.pack(side='left', padx=20, pady=25)
        
        logout_btn = ttk.Button(header_frame, text="🚪 Sair", 
                                style='Danger.TButton',
                                command=self.logout)
        logout_btn.pack(side='right', padx=20, pady=25)
        
        main_container = tk.Frame(self.root, bg=self.colors['secondary'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_content_area(main_container)
        self.create_professor_sidebar(main_container)
        
        self.root.after(100, self.update_responsive_layout)

    def create_professor_sidebar(self, parent):
        """Cria o menu lateral do professor."""
        self.sidebar = tk.Frame(parent, bg=self.colors['dark'], width=280)
        self.sidebar.pack(side='right', fill='y', padx=(0, 15))
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
            ("📊 Lançar Nota", 'Primary.TButton', self.show_grade_form)
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



    def show_register_form(self):
        """Exibe o formulário de cadastro de aluno."""
        self.show_frame(self.register_frame)

    def create_register_form(self):
        """Cria o formulário de cadastro de aluno."""
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
        button_frame.pack(pady=30)
        
        ttk.Button(button_frame, text="✅ Cadastrar Aluno", 
                    style='Success.TButton',
                    command=self.register_student).pack(side='left', padx=10)
        
        ttk.Button(button_frame, text="🗑️ Limpar Campos", 
                    style='Danger.TButton',
                    command=self.clear_form_fields).pack(side='left', padx=10)
        
        return frame

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

    def show_students_list(self):
        """Exibe a lista de alunos cadastrados."""
        self.load_students()
        self.show_frame(self.list_frame)

    def create_students_list(self):
        """Cria a interface de listagem de alunos."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title_frame = tk.Frame(card, bg=self.colors['card_bg'])
        title_frame.pack(fill='x', pady=15)
        
        title = tk.Label(title_frame, text="👥 Lista de Alunos Cadastrados",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(side='left', padx=20)
        
        refresh_btn = ttk.Button(title_frame, text="🔄 Atualizar Lista",
                                style='Primary.TButton',
                                command=self.load_students)
        refresh_btn.pack(side='right', padx=20)
        
        dashboard_btn = ttk.Button(title_frame, text="📊 Ver Dashboard",
                                    style='Warning.TButton',
                                    command=self.show_statistics)
        dashboard_btn.pack(side='right', padx=10)
        
        tree_frame = tk.Frame(card, bg=self.colors['card_bg'])
        tree_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        columns = ('nome', 'email', 'idade', 'nota')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('nome', text='👤 Nome Completo')
        self.tree.heading('email', text='📧 Email')
        self.tree.heading('idade', text='🎂 Idade')
        self.tree.heading('nota', text='📊 Nota') 
        
        self.tree.column('email', width=250)
        self.tree.column('nome', width=300)
        self.tree.column('idade', width=80)
        self.tree.column('nota', width=80) 
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.pack(side='left', fill='both', expand=True)
        
        return frame

    def load_students(self):
        """Carrega e exibe a lista de alunos do sistema."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            with open('database/alunos.txt', 'r', encoding='utf-8') as f:
                students_found = False
                for line in f:
                    line = line.strip()
                    if line and ';' in line:
                        parts = line.split(';')
                        if len(parts) >= 4:
                            email = parts[0].strip()
                            nome = parts[1].strip()
                            idade = parts[2].strip()
                            nota_str = parts[3].strip()
                            
                            try:
                                nota_float = float(nota_str)
                                if nota_float == -1.0:
                                    nota_display = "N/A"  
                                else:
                                    nota_display = f"{nota_float:.2f}"
                            except ValueError:
                                nota_display = "N/A"
                            
                            if email and nome and idade:
                                self.tree.insert('', tk.END, values=(nome, email, idade, nota_display))
                                students_found = True
                
                if students_found:
                    return
        except FileNotFoundError:
            pass
        
        success, result = self.execute_c_command('list')
        
        if success:
            lines = result.split('\n')
            students_found = False
            
            for line in lines:
                line = line.strip()
                
                if 'Nome:' in line and 'Email:' not in line:
                    try:
                        nome = line.replace('Nome:', '').strip()
                        
                        idx = lines.index(line)
                        email = ""
                        idade = ""
                        nota = "N/A"
                        
                        for i in range(idx + 1, min(idx + 6, len(lines))):
                            if 'Email:' in lines[i]:
                                email = lines[i].replace('Email:', '').strip()
                            if 'Idade:' in lines[i]:
                                idade_line = lines[i].replace('Idade:', '').strip()
                                idade = idade_line.split()[0] if idade_line.split() else ""
                            if 'Nota:' in lines[i]:
                                nota_line = lines[i].replace('Nota:', '').strip()
                                if 'Não lançada' in nota_line:
                                    nota = "N/A"
                                else:
                                    import re
                                    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", nota_line)
                                    if numbers:
                                        nota = f"{float(numbers[0]):.2f}"
                        
                        if email and nome and idade:
                            self.tree.insert('', tk.END, values=(email, nome, idade, nota))
                            students_found = True
                            
                    except (IndexError, ValueError) as e:
                        print(f"Erro ao processar linha: {line} - {e}")
                        continue
            
            if not students_found:
                self.tree.insert('', tk.END, values=("Nenhum aluno", "cadastrado", "no sistema", ""))
        else:
            self.tree.insert('', tk.END, values=("Erro ao", "carregar dados", "", result[:50]))
            
    def show_update_form(self):
        """Exibe o formulário de atualização de aluno."""
        self.show_frame(self.update_frame)

    def create_update_form(self):
        """Cria o formulário de atualização de aluno."""
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
        
        tk.Label(search_frame, text="🔍 Buscar Aluno por Email:", 
                bg=self.colors['card_bg'], fg=self.colors['text_light'],
                font=('Segoe UI', 11, 'bold'), anchor='w').pack(fill='x', pady=(10, 5))
        
        self.search_email_entry = ttk.Entry(search_frame, width=35, 
                                            font=('Segoe UI', 11), style='Modern.TEntry')
        self.search_email_entry.pack(fill='x', pady=5)
        
        search_button = ttk.Button(search_frame, text="🔎 Buscar Aluno", 
                                    style='Primary.TButton',
                                    command=self.search_student)
        search_button.pack(fill='x', pady=10)
        
        self.update_form_frame = tk.Frame(card, bg=self.colors['card_bg'])
        
        tk.Label(self.update_form_frame, text="👤 Novo Nome:", 
                bg=self.colors['card_bg'], fg=self.colors['text_light'],
                font=('Segoe UI', 11, 'bold'), anchor='w').pack(fill='x', pady=(10, 5))
        
        self.update_name_entry = ttk.Entry(self.update_form_frame, width=35, 
                                            font=('Segoe UI', 11), style='Modern.TEntry')
        self.update_name_entry.pack(fill='x', pady=5)
        
        tk.Label(self.update_form_frame, text="🎂 Nova Idade:", 
                bg=self.colors['card_bg'], fg=self.colors['text_light'],
                font=('Segoe UI', 11, 'bold'), anchor='w').pack(fill='x', pady=(10, 5))
        
        self.update_age_entry = ttk.Entry(self.update_form_frame, width=35, 
                                        font=('Segoe UI', 11), style='Modern.TEntry')
        self.update_age_entry.pack(fill='x', pady=5)
        
        update_button = ttk.Button(self.update_form_frame, text="💾 Atualizar Dados", 
                                    style='Success.TButton',
                                    command=self.update_student)
        update_button.pack(fill='x', pady=15)
        
        return frame

    def search_student(self):
        """Busca um aluno por email para edição."""
        email = self.search_email_entry.get().strip()
        if not email:
            messagebox.showerror("Erro", "Digite um email para buscar!")
            return
        
        # Primeiro tentar buscar no arquivo diretamente
        try:
            with open('database/alunos.txt', 'r', encoding='utf-8') as f:
                aluno_encontrado = False
                for line in f:
                    line = line.strip()
                    if line and ';' in line:
                        parts = line.split(';')
                        if len(parts) >= 4:
                            # Verificar em ambas as posições possíveis para o email
                            email_possivel_1 = parts[0].strip()
                            email_possivel_2 = parts[1].strip() if len(parts) > 1 else ""
                            
                            # Verificar qual campo contém o email (tem @)
                            if '@' in email_possivel_1 and email_possivel_1 == email:
                                nome = parts[1].strip()
                                idade = parts[2].strip()
                                aluno_encontrado = True
                                break
                            elif '@' in email_possivel_2 and email_possivel_2 == email:
                                nome = parts[0].strip()
                                idade = parts[2].strip()
                                aluno_encontrado = True
                                break
                
                if aluno_encontrado:
                    self.update_name_entry.delete(0, tk.END)
                    self.update_name_entry.insert(0, nome)
                    self.update_age_entry.delete(0, tk.END)
                    self.update_age_entry.insert(0, idade)
                    
                    self.update_form_frame.pack(pady=20, padx=50, fill='x')
                    messagebox.showinfo("Sucesso", "Aluno encontrado! Preencha os novos dados.")
                    return
            
            # Se não encontrou no arquivo, tentar via comando C
            success, result = self.execute_c_command('list')
            if success:
                lines = result.split('\n')
                for i, line in enumerate(lines):
                    if email in line and 'Email:' in line:
                        # Encontrou o email, agora buscar nome e idade
                        nome = ""
                        idade = ""
                        
                        # Procurar nome (linha anterior)
                        for j in range(max(0, i-2), i):
                            if 'Nome:' in lines[j] and 'Email:' not in lines[j]:
                                nome = lines[j].replace('Nome:', '').strip()
                                break
                        
                        # Procurar idade (linha posterior)
                        for j in range(i+1, min(i+3, len(lines))):
                            if 'Idade:' in lines[j]:
                                idade_line = lines[j].replace('Idade:', '').strip()
                                idade = idade_line.split()[0] if idade_line.split() else ""
                                break
                        
                        if nome and idade:
                            self.update_name_entry.delete(0, tk.END)
                            self.update_name_entry.insert(0, nome)
                            self.update_age_entry.delete(0, tk.END)
                            self.update_age_entry.insert(0, idade)
                            
                            self.update_form_frame.pack(pady=20, padx=50, fill='x')
                            messagebox.showinfo("Sucesso", "Aluno encontrado! Preencha os novos dados.")
                            return
            
            messagebox.showerror("Erro", "Aluno não encontrado!")
            
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de alunos não encontrado!")
        
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
        
        # Primeiro tentar via comando C
        success, result = self.execute_c_command('update', email, novo_nome, nova_idade)
        
        if success and "atualizado com sucesso" in result.lower():
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
            self.search_email_entry.delete(0, tk.END)
            self.update_name_entry.delete(0, tk.END)
            self.update_age_entry.delete(0, tk.END)
            self.update_form_frame.pack_forget()
        else:
            # Fallback: atualização manual no arquivo
            try:
                with open('database/alunos.txt', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                aluno_encontrado = False
                with open('database/alunos.txt', 'w', encoding='utf-8') as f:
                    for line in lines:
                        if ';' in line:
                            parts = line.strip().split(';')
                            if len(parts) >= 4:
                                # Verificar em ambas as posições possíveis para o email
                                email_possivel_1 = parts[0].strip()
                                email_possivel_2 = parts[1].strip() if len(parts) > 1 else ""
                                
                                # Verificar qual campo contém o email (tem @)
                                if '@' in email_possivel_1 and email_possivel_1 == email:
                                    # Email está na primeira posição
                                    new_line = f"{email};{novo_nome};{nova_idade};{parts[3]}\n"
                                    f.write(new_line)
                                    aluno_encontrado = True
                                elif '@' in email_possivel_2 and email_possivel_2 == email:
                                    # Email está na segunda posição
                                    new_line = f"{novo_nome};{email};{nova_idade};{parts[3]}\n"
                                    f.write(new_line)
                                    aluno_encontrado = True
                                else:
                                    f.write(line)
                            else:
                                f.write(line)
                        else:
                            f.write(line)
                
                if aluno_encontrado:
                    messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
                    self.search_email_entry.delete(0, tk.END)
                    self.update_name_entry.delete(0, tk.END)
                    self.update_age_entry.delete(0, tk.END)
                    self.update_form_frame.pack_forget()
                else:
                    messagebox.showerror("Erro", "Aluno não encontrado no sistema!")
                    
            except FileNotFoundError:
                messagebox.showerror("Erro", "Arquivo de alunos não encontrado!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar aluno: {str(e)}")

    def show_delete_form(self):
        """Exibe o formulário de exclusão de aluno."""
        self.show_frame(self.delete_frame)

    def create_delete_form(self):
        """Cria o formulário de exclusão de aluno."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title = tk.Label(card, text="🗑️ Excluir Aluno",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=20)
        
        form_frame = tk.Frame(card, bg=self.colors['card_bg'])
        form_frame.pack(pady=15, padx=40, fill='x')
        
        tk.Label(form_frame, text="📧 Email do Aluno a Excluir:", 
                bg=self.colors['card_bg'], fg=self.colors['text_light'],
                font=('Segoe UI', 11, 'bold'), anchor='w').pack(fill='x', pady=(10, 5))
        
        self.delete_email_entry = ttk.Entry(form_frame, width=35, 
                                            font=('Segoe UI', 11), style='Modern.TEntry')
        self.delete_email_entry.pack(fill='x', pady=5)
        
        delete_button = ttk.Button(form_frame, text="🗑️ Excluir Aluno", 
                                    style='Danger.TButton',
                                    command=self.delete_student)
        delete_button.pack(fill='x', pady=15)
        
        return frame

    def delete_student(self):
        """Exclui um aluno do sistema."""
        email = self.delete_email_entry.get().strip()
        if not email:
            messagebox.showerror("Erro", "Digite um email para excluir!")
            return
        
        if messagebox.askyesno("Confirmar Exclusão", 
                                f"Tem certeza que deseja excluir o aluno com email:\n{email}?\n\nEsta ação não pode ser desfeita!"):
            
            success, result = self.execute_c_command('delete', email)
            
            if success and ("excluido com sucesso" in result.lower() or "excluído com sucesso" in result.lower()):
                messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
                self.delete_email_entry.delete(0, tk.END)
            else:
                try:
                    with open('database/alunos.txt', 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    with open('database/alunos.txt', 'w', encoding='utf-8') as f:
                        aluno_encontrado = False
                        for line in lines:
                            if ';' in line:
                                parts = line.split(';')
                                if len(parts) >= 2:
                                    file_email = parts[0].strip() if '@' in parts[0] else parts[1].strip() if len(parts) > 1 and '@' in parts[1] else ""
                                    if file_email != email:
                                        f.write(line)
                                    else:
                                        aluno_encontrado = True
                                else:
                                    f.write(line)
                            else:
                                f.write(line)
                        
                        if aluno_encontrado:
                            messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
                            self.delete_email_entry.delete(0, tk.END)
                        else:
                            messagebox.showerror("Erro", "Aluno não encontrado no sistema!")
                            
                except FileNotFoundError:
                    messagebox.showerror("Erro", "Arquivo de alunos não encontrado!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao excluir aluno: {str(e)}")



    def show_grade_form(self):
        """Exibe o formulário de lançamento de notas."""
        self.show_frame(self.grade_frame)

    def create_grade_form(self):
        """Cria o formulário de lançamento de notas."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title = tk.Label(card, text="📊 Lançar Nota para Aluno",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(pady=20)
        
        form_frame = tk.Frame(card, bg=self.colors['card_bg'])
        form_frame.pack(pady=15, padx=40, fill='x')
        
        tk.Label(form_frame, text="📧 Email do Aluno:", 
                bg=self.colors['card_bg'], fg=self.colors['text_light'],
                font=('Segoe UI', 11, 'bold'), anchor='w').pack(fill='x', pady=(10, 5))
        
        self.grade_email_entry = ttk.Entry(form_frame, width=35, 
                                            font=('Segoe UI', 11), style='Modern.TEntry')
        self.grade_email_entry.pack(fill='x', pady=5)
        
        tk.Label(form_frame, text="📝 Nota (0-10):", 
                bg=self.colors['card_bg'], fg=self.colors['text_light'],
                font=('Segoe UI', 11, 'bold'), anchor='w').pack(fill='x', pady=(10, 5))
        
        self.grade_entry = ttk.Entry(form_frame, width=35, 
                                    font=('Segoe UI', 11), style='Modern.TEntry')
        self.grade_entry.pack(fill='x', pady=5)
        
        grade_button = ttk.Button(form_frame, text="📊 Lançar Nota", 
                                style='Primary.TButton',
                                command=self.assign_grade)
        grade_button.pack(fill='x', pady=15)
        
        return frame

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
        
        # Primeiro tentar via comando C
        success, result = self.execute_c_command('grade', email, nota)
        
        if success and "nota registrada" in result.lower():
            messagebox.showinfo("Sucesso", "Nota atribuída com sucesso!")
            self.grade_email_entry.delete(0, tk.END)
            self.grade_entry.delete(0, tk.END)
        else:
            # Fallback: atribuição manual de nota
            try:
                with open('database/alunos.txt', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                aluno_encontrado = False
                with open('database/alunos.txt', 'w', encoding='utf-8') as f:
                    for line in lines:
                        if ';' in line:
                            parts = line.strip().split(';')
                            if len(parts) >= 4:
                                # Verificar email (pode estar em diferentes posições)
                                file_email = ""
                                for part in parts:
                                    if '@' in part and '.' in part:
                                        file_email = part.strip()
                                        break
                                
                                if file_email == email:
                                    # Reconstruir a linha com a nova nota
                                    new_line = f"{parts[0]};{parts[1]};{parts[2]};{nota_float:.2f}\n"
                                    f.write(new_line)
                                    aluno_encontrado = True
                                else:
                                    f.write(line)
                            else:
                                f.write(line)
                        else:
                            f.write(line)
                
                if aluno_encontrado:
                    messagebox.showinfo("Sucesso", "Nota atribuída com sucesso!")
                    self.grade_email_entry.delete(0, tk.END)
                    self.grade_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Erro", "Aluno não encontrado no sistema!")
                    
            except FileNotFoundError:
                messagebox.showerror("Erro", "Arquivo de alunos não encontrado!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atribuir nota: {str(e)}")

    def show_statistics(self):
        """Exibe as estatísticas do sistema."""
        self.update_statistics()
        self.show_frame(self.stats_frame)

    def create_statistics(self):
        """Cria a interface de estatísticas."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title_frame = tk.Frame(card, bg=self.colors['card_bg'])
        title_frame.pack(fill='x', pady=15)
        
        title = tk.Label(title_frame, text="📊 Dashboard do Sistema",
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(side='left', padx=20)
        
        refresh_btn = ttk.Button(title_frame, text="🔄 Atualizar",
                                style='Primary.TButton',
                                command=self.update_statistics)
        refresh_btn.pack(side='right', padx=20)
        
        back_btn = ttk.Button(title_frame, text="↩️ Voltar para Lista",
                                style='Warning.TButton',
                                command=self.show_students_list)
        back_btn.pack(side='right', padx=10)
        
        text_frame = tk.Frame(card, bg=self.colors['card_bg'])
        text_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        self.stats_text = scrolledtext.ScrolledText(text_frame, 
                                                    wrap=tk.WORD,
                                                    font=('Consolas', 11),
                                                    bg=self.colors['dark'],
                                                    fg=self.colors['text_light'],
                                                    padx=15, pady=15)
        self.stats_text.pack(fill='both', expand=True)
        
        return frame

    def update_statistics(self):
        """Atualiza e exibe as estatísticas do sistema."""
        self.stats_text.delete('1.0', tk.END)
        
        try:
            with open('database/alunos.txt', 'r', encoding='utf-8') as f:
                alunos = []
                for line in f:
                    line = line.strip()
                    if line and ';' in line:
                        parts = line.split(';')
                        if len(parts) >= 4:
                            nome = parts[0].strip()
                            email = parts[1].strip()
                            idade_str = parts[2].strip()
                            nota_str = parts[3].strip()
                            
                            try:
                                idade = int(idade_str)
                                alunos.append({
                                    'nome': nome,
                                    'email': email,
                                    'idade': idade,
                                    'nota': nota_str
                                })
                            except ValueError:
                                continue
                
                if alunos:
                    total_alunos = len(alunos)
                    idades = [aluno['idade'] for aluno in alunos]
                    idade_media = sum(idades) / len(idades) if idades else 0
                    idade_min = min(idades) if idades else 0
                    idade_max = max(idades) if idades else 0
                    
                    alunos_com_nota = 0
                    notas = []
                    for aluno in alunos:
                        try:
                            nota = float(aluno['nota'])
                            if nota >= 0:
                                alunos_com_nota += 1
                                notas.append(nota)
                        except ValueError:
                            continue
                    
                    media_notas = sum(notas) / len(notas) if notas else 0
                    
                    stats = f"""=== DASHBOARD DO SISTEMA ===

📊 ESTATÍSTICAS GERAIS:
• Total de Alunos: {total_alunos}
• Alunos com Nota: {alunos_com_nota}
• Idade Média: {idade_media:.1f} anos
• Aluno Mais Jovem: {idade_min} anos
• Aluno Mais Velho: {idade_max} anos
• Média Geral das Notas: {media_notas:.2f}

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
                    
                    stats += f"\n\n🎯 DISTRIBUIÇÃO DE NOTAS:"
                    ranges = {
                        '0-4.9': 0,
                        '5.0-6.9': 0,
                        '7.0-8.9': 0,
                        '9.0-10.0': 0
                    }
                    
                    for nota in notas:
                        if 0 <= nota <= 4.9:
                            ranges['0-4.9'] += 1
                        elif 5.0 <= nota <= 6.9:
                            ranges['5.0-6.9'] += 1
                        elif 7.0 <= nota <= 8.9:
                            ranges['7.0-8.9'] += 1
                        elif 9.0 <= nota <= 10.0:
                            ranges['9.0-10.0'] += 1
                    
                    for range_nota, quantidade in ranges.items():
                        if alunos_com_nota > 0:
                            percentual = (quantidade / alunos_com_nota) * 100
                            stats += f"\n• {range_nota}: {quantidade} alunos ({percentual:.1f}%)"
                        else:
                            stats += f"\n• {range_nota}: 0 alunos (0%)"
                    
                else:
                    stats = "Nenhum aluno cadastrado no sistema."
                
                stats += f"\n\n🔄 Última atualização: {time.strftime('%d/%m/%Y %H:%M:%S')}"
                
                self.stats_text.insert('1.0', stats)
                
        except FileNotFoundError:
            success, result = self.execute_c_command('list')
            
            if success:
                lines = result.split('\n')
                total_alunos = 0
                idades = []
                
                for line in lines:
                    if 'Nome:' in line and 'Email:' not in line:
                        try:
                            nome = line.replace('Nome:', '').strip()
                            
                            idx = lines.index(line)
                            email = ""
                            idade = ""
                            
                            for i in range(idx + 1, min(idx + 5, len(lines))):
                                if 'Email:' in lines[i]:
                                    email = lines[i].replace('Email:', '').strip()
                                if 'Idade:' in lines[i]:
                                    idade_str = lines[i].replace('Idade:', '').strip()
                                    try:
                                        idade = int(idade_str.split()[0])
                                    except ValueError:
                                        idade = 0
                            
                            if email and nome and idade:
                                total_alunos += 1
                                idades.append(idade)
                                
                        except (IndexError, ValueError):
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
                
                self.stats_text.insert('1.0', stats)
            else:
                self.stats_text.insert('1.0', f"Erro ao carregar estatísticas:\n{result}")
        except Exception as e:
            self.stats_text.insert('1.0', f"Erro ao processar estatísticas:\n{str(e)}")