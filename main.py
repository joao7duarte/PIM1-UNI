import tkinter as tk
from app.system import StudentManagementSystem

def main():
    """Função principal que inicia a aplicação."""
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()