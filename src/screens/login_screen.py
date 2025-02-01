from src.screens.base_screen import BaseScreen
from src.utils import center_window
import tkinter as tk
from tkinter import messagebox


class LoginScreen(BaseScreen):
    def __init__(self, master, app):
        super().__init__(master, app)
        self.create_widgets()

    def setup_window(self):
        self.app.title("Авторизация")
        self.app.geometry("300x200")
        self.app.resizable(False, False)
        center_window(self.app)

    def create_widgets(self):
        # Метка и поле для логина
        self.label_login = tk.Label(self, text="Логин:")
        self.label_login.pack(pady=5)

        self.entry_login = tk.Entry(self)
        self.entry_login.pack(pady=5)

        # Метка и поле для пароля
        self.label_password = tk.Label(self, text="Пароль:")
        self.label_password.pack(pady=5)

        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        # Кнопка авторизации
        self.login_button = tk.Button(self, text="Войти", command=self.authenticate)
        self.login_button.pack(pady=10)

        # Привязка Enter к методу authenticate
        self.entry_password.bind("<Return>", lambda event: self.authenticate())

    def authenticate(self):
        # Проверка логина и пароля (заглушка)
        login = self.entry_login.get()
        password = self.entry_password.get()

        if login == "admin" and password == "admin":
            self.app.switch_screen("main_screen_panels")
        else:
            tk.messagebox.showerror("Ошибка", "Неверный логин или пароль")