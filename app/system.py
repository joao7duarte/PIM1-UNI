import tkinter as tk
import subprocess
import os

from app.utils.styles import setup_styles
from app.utils.responsive import Responsive
from app.auth.login import Login
from app.views.professor import Professor
from app.views.student import Student
from app.views.chatbot_interface import ChatbotInterface

class StudentManagementSystem(Responsive, Professor, Student, Login, ChatbotInterface):
    def __init__(self, root):
        """Inicializa o sistema de gestão escolar com interface gráfica."""
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

        setup_styles(self)
        
        self.root.bind('<Configure>', self.on_window_resize)

        self.root.after(100, self.initialize_responsive)
        
        self.create_login_interface()
 
    def show_frame(self, frame_to_show):
        """Exibe um frame específico e oculta os demais."""
        frames = []
        
        if hasattr(self, 'welcome_frame') and self.welcome_frame is not None:
            frames.append(self.welcome_frame)
        if hasattr(self, 'register_frame') and self.register_frame is not None:
            frames.append(self.register_frame)
        if hasattr(self, 'list_frame') and self.list_frame is not None:
            frames.append(self.list_frame)
        if hasattr(self, 'update_frame') and self.update_frame is not None:
            frames.append(self.update_frame)
        if hasattr(self, 'delete_frame') and self.delete_frame is not None:
            frames.append(self.delete_frame)
        if hasattr(self, 'grade_frame') and self.grade_frame is not None:
            frames.append(self.grade_frame)
        if hasattr(self, 'stats_frame') and self.stats_frame is not None:
            frames.append(self.stats_frame)
        if hasattr(self, 'student_grades_frame') and self.student_grades_frame is not None:
            frames.append(self.student_grades_frame)
        if hasattr(self, 'chatbot_frame') and self.chatbot_frame is not None:
            frames.append(self.chatbot_frame)
        
        for frame in frames:
            if frame is not None:
                frame.pack_forget()
        
        if frame_to_show is not None:
            frame_to_show.pack(fill='both', expand=True)

        self.update_responsive_layout()

    def clear_interface(self):
        """Remove todos os widgets da interface."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def toggle_sidebar(self):
        """Alterna a visibilidade da barra lateral."""
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side='right', fill='y', padx=(0, 15))
            self.sidebar_visible = True

    def clear_form_fields(self):
        """Limpa os campos de entrada de formulários."""
        self.email_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

    def execute_c_command(self, command, *args):
        """Executa comandos no sistema C compilado."""
        try:
            if not os.path.exists('system.exe'):
                compile_result = subprocess.run(
                    ['gcc', 'main.c', 'menualuno.c', 'menuprof.c', '-o', 'system.exe'], 
                    capture_output=True, text=True
                )
                if compile_result.returncode != 0:
                    return False, f"Erro na compilação: {compile_result.stderr}"
            
            input_data = ""
        
            if command == 'list':
                input_data = '1\n2\n0\n0\n' 
            elif command == 'add':
                input_data = f'1\n1\n{args[0]}\n{args[1]}\n{args[2]}\n0\n0\n'
            elif command == 'update':
                input_data = f'1\n3\n{args[0]}\n{args[1]}\n{args[2]}\n0\n0\n'
            elif command == 'delete':
                input_data = f'1\n4\n{args[0]}\n0\n0\n'
            elif command == 'grade':
                input_data = f'1\n5\n{args[0]}\n{args[1]}\n0\n0\n'
            elif command == 'view_grades':
                input_data = f'2\n1\n{args[0]}\n0\n0\n'
            else:
                return False, "Comando não reconhecido"
            
            result = subprocess.run(
                ['system.exe'], 
                input=input_data, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            return True, result.stdout
            
        except subprocess.TimeoutExpired:
            return False, "Timeout: O sistema demorou muito para responder"
        except Exception as e:
            return False, f"Erro ao executar sistema: {str(e)}"
            
    def create_welcome_screen(self):
        """Cria a tela de boas-vindas para usuários."""
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

    
    