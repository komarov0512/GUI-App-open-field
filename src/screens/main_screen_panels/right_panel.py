import tkinter as tk


class RightPanel(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self._create_widgets()

    def _create_widgets(self):
        """Создает элементы правой панели"""
        self.config(
            bg="#e0e0e0",
            width=int(self.app.winfo_screenwidth() * 0.2)
        )

        label = tk.Label(self, text="Правая панель", bg="#e0e0e0")
        label.pack(pady=20)