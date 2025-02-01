import tkinter as tk


class CentralPanel(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self._create_widgets()

    def _create_widgets(self):
        """Создает элементы центральной панели"""
        self.config(bg="white")
        # Кнопка "Загрузить файл" по центру
        self.btn_load = tk.Button(self, text="Загрузить файл",command=self._on_file_load)
        self.btn_load.place(relx=0.5, rely=0.5, anchor="center")

    def _on_file_load(self):
        """Обработчик загрузки файла"""
        print("Файл загружен!")