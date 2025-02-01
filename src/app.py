from src.screens.login_screen import LoginScreen
from src.screens.main_screen import MainScreen
from src.utils import center_window
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200")
        center_window(self)

        # Словарь для хранения экранов
        self.screens = {}
        self.current_screen = None

        # Инициализация экранов
        self.init_screens()
        self.switch_screen("login")

    def init_screens(self):
        # Создаем экраны и добавляем их в словарь
        self.screens["login"] = LoginScreen(self, self)
        self.screens["main_screen_panels"] = MainScreen(self, self)

    def switch_screen(self, screen_name):
        # Скрываем текущий экран
        if self.current_screen:
            self.current_screen.pack_forget()

        # Показываем новый экран
        self.current_screen = self.screens[screen_name]
        self.current_screen.setup_window()
        self.current_screen.pack(fill=tk.BOTH, expand=True)