import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading

class ChatbotInterface():
    def create_chatbot_interface(self):
        """Cria a interface do chatbot."""
        frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        
        card = tk.Frame(frame, bg=self.colors['card_bg'], relief='flat')
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        title_frame = tk.Frame(card, bg=self.colors['card_bg'])
        title_frame.pack(fill='x', pady=15)
        
        if self.current_user == 'professor':
            title_text = "🤖 Chatbot de Ajuda - Professor"
        else:
            title_text = "🤖 Chatbot de Ajuda - Aluno"
            
        title = tk.Label(title_frame, text=title_text,
                        font=('Segoe UI', 20, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_light'])
        title.pack(side='left', padx=20)
        
        clear_btn = ttk.Button(title_frame, text="🗑️ Limpar Chat",
                              style='Danger.TButton',
                              command=self.clear_chat)
        clear_btn.pack(side='right', padx=10)
        
        info_btn = ttk.Button(title_frame, text="ℹ️ Ajuda",
                             style='Warning.TButton',
                             command=self.show_chatbot_help)
        info_btn.pack(side='right', padx=10)
        
        chat_container = tk.Frame(card, bg=self.colors['card_bg'])
        chat_container.pack(fill='both', expand=True, padx=20, pady=15)
        
        self.chat_history = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            bg=self.colors['dark'],
            fg=self.colors['text_light'],
            padx=15,
            pady=15,
            state='disabled',
            height=15
        )
        self.chat_history.pack(fill='both', expand=True, pady=(0, 10))
        
        input_frame = tk.Frame(chat_container, bg=self.colors['card_bg'])
        input_frame.pack(fill='x', pady=10)
        
        self.chat_input = ttk.Entry(
            input_frame,
            font=('Segoe UI', 11),
            style='Modern.TEntry'
        )
        self.chat_input.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.chat_input.bind('<Return>', lambda e: self.send_message())
        
        send_btn = ttk.Button(
            input_frame,
            text="📤 Enviar",
            style='Primary.TButton',
            command=self.send_message
        )
        send_btn.pack(side='right')
        
        example_frame = tk.Frame(chat_container, bg=self.colors['card_bg'])
        example_frame.pack(fill='x', pady=5)
        
        if self.current_user == 'professor':
            examples = [
                "Como cadastrar aluno?",
                "Como lançar notas?",
                "Como ver estatísticas?",
                "Como excluir aluno?"
            ]
        else:
            examples = [
                "Como ver minhas notas?",
                "Quando saem as notas?",
                "Como entrar em contato com o professor?",
                "O que fazer se minha nota estiver errada?"
            ]
        
        for i, example in enumerate(examples):
            btn = ttk.Button(
                example_frame,
                text=example,
                style='Success.TButton' if i % 2 == 0 else 'Warning.TButton',
                command=lambda ex=example: self.insert_example(ex)
            )
            btn.pack(side='left', padx=5, fill='x', expand=True)
        
        if self.current_user == 'professor':
            welcome_message = "Olá, Professor! Sou seu assistente virtual. Como posso ajudar você com a gestão escolar hoje?"
        else:
            student_email = getattr(self, 'student_logged_email', 'Aluno')
            welcome_message = f"Olá, {student_email}! Sou seu assistente virtual. Como posso ajudar você com suas dúvidas acadêmicas?"
        
        self.add_bot_message(welcome_message)
        
        return frame

    def insert_example(self, example):
        """Insere um exemplo no campo de entrada."""
        self.chat_input.delete(0, tk.END)
        self.chat_input.insert(0, example)

    def send_message(self):
        """Envia a mensagem do usuário para o chatbot."""
        message = self.chat_input.get().strip()
        if not message:
            return
        
        self.add_user_message(message)
        self.chat_input.delete(0, tk.END)
        
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()

    def chat(self, prompt):
        """Função principal para comunicação com o modelo de IA."""
        contexto = (
            "Você é um assistente dentro de um Sistema Acadêmico Colaborativo com apoio de Inteligência Artificial. "
            "O sistema foi desenvolvido em C, possui interface em Tkinter e integração com um chatbot. "
            "Os usuários podem ser alunos ou professores, e o chatbot deve ajudar tirando dúvidas sobre o uso do sistema, "
            "como login, cadastro, lançamento de notas e visualização de desempenho."
        )

        system_prompt = f"Responda sempre em português do Brasil de forma natural, clara e educada." f"{contexto}\nUsuário: {prompt}"

        result = subprocess.run(
            ["C:\\Users\\guilhermeam\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", "gemma3:1b", system_prompt],
            capture_output=True, text=True, encoding='utf-8'
        )
        
        return result.stdout.strip()

    def process_message(self, message):
        """Processa a mensagem usando o chatbot."""
        try:
            self.show_typing_indicator()
            
            response = self.chat(message)
            
            self.hide_typing_indicator()
            
            if response:
                self.add_bot_message(response)
            else:
                self.add_bot_message("Desculpe, não consegui processar sua mensagem. Poderia reformular?")
                
        except subprocess.TimeoutExpired:
            self.hide_typing_indicator()
            self.add_bot_message("Tempo de resposta excedido. Tente novamente.")
        except Exception as e:
            self.hide_typing_indicator()
            self.add_bot_message("Erro de conexão com o chatbot. Verifique se o Ollama está rodando.")
            print(f"Erro no chatbot: {e}")

    def add_user_message(self, message):
        """Adiciona mensagem do usuário ao histórico."""
        self.chat_history.config(state='normal')
        if self.current_user == 'professor':
            self.chat_history.insert(tk.END, f"\n👨‍🏫 Professor: {message}\n")
        else:
            self.chat_history.insert(tk.END, f"\n👨‍🎓 Aluno: {message}\n")
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

    def add_bot_message(self, message):
        """Adiciona mensagem do bot ao histórico."""
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, f"🤖 Assistente: {message}\n")
        self.chat_history.insert(tk.END, "─" * 50 + "\n")
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

    def show_typing_indicator(self):
        """Mostra indicador de que o bot está digitando."""
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, f"🤖 Assistente está digitando...\n")
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

    def hide_typing_indicator(self):
        """Remove o indicador de digitação."""
        self.chat_history.config(state='normal')
        lines = self.chat_history.get('1.0', tk.END).split('\n')
        if lines and "está digitando" in lines[-2]:
            content = '\n'.join(lines[:-2]) + '\n'
            self.chat_history.delete('1.0', tk.END)
            self.chat_history.insert('1.0', content)
        self.chat_history.config(state='disabled')

    def clear_chat(self):
        """Limpa o histórico do chat."""
        if messagebox.askyesno("Limpar Chat", "Tem certeza que deseja limpar o histórico do chat?"):
            self.chat_history.config(state='normal')
            self.chat_history.delete('1.0', tk.END)
            self.chat_history.config(state='disabled')
            
            if self.current_user == 'professor':
                welcome_message = "Olá, Professor! Sou seu assistente virtual. Como posso ajudar você com a gestão escolar hoje?"
            else:
                student_email = getattr(self, 'student_logged_email', 'Aluno')
                welcome_message = f"Olá, {student_email}! Sou seu assistente virtual. Como posso ajudar você com suas dúvidas acadêmicas?"
            
            self.add_bot_message(welcome_message)

    def show_chatbot_help(self):
        """Mostra informações de ajuda sobre o chatbot."""
        if self.current_user == 'professor':
            help_text = """🤖 CHATBOT DE AJUDA - PROFESSOR

Este chatbot usa inteligência artificial para ajudar você com:

📚 Funcionalidades do Sistema:
• Cadastro e gerenciamento de alunos
• Lançamento e consulta de notas
• Estatísticas e relatórios
• Navegação no sistema

💡 Dicas de Uso:
• Faça perguntas específicas sobre gestão escolar
• Use os botões de exemplo para perguntas comuns
• O bot pode ajudar com dúvidas sobre funcionalidades administrativas

⚙️ Requisitos:
• Ollama instalado e rodando
• Modelo gemma3:1b carregado

Digite 'sair' para encerrar a conversa com o bot."""
        else:
            help_text = """🤖 CHATBOT DE AJUDA - ALUNO

Este chatbot usa inteligência artificial para ajudar você com:

📚 Dúvidas Acadêmicas:
• Consulta de notas e desempenho
• Informações sobre prazos e procedimentos
• Contato com professores
• Dúvidas sobre o sistema

💡 Dicas de Uso:
• Faça perguntas sobre suas notas e atividades
• Use os botões de exemplo para perguntas comuns
• Para questões administrativas, entre em contato com o professor

⚙️ Requisitos:
• Ollama instalado e rodando
• Modelo gemma3:1b carregado
"""
        
        messagebox.showinfo("Ajuda do Chatbot", help_text)