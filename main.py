import tkinter as tk
from app.system import StudentManagementSystem

def main():
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()