import tkinter as tk

class BaseScreen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

    def setup_window(self):
        """Настройка заголовка и размера окна. Переопределяется в дочерних классах."""
        pass

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()