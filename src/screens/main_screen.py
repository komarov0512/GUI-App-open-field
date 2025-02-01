from src.screens.base_screen import BaseScreen
from src.screens.main_screen_panels.top_panel import TopPanel
from src.screens.main_screen_panels.left_panel import LeftPanel
from src.screens.main_screen_panels.right_panel import RightPanel
from src.screens.main_screen_panels.central_panel import CentralPanel
from src.utils import center_window
import tkinter as tk

class MainScreen(BaseScreen):
    def __init__(self, master, app):
        super().__init__(master, app)
        self._create_layout()

    def setup_window(self):
        self.app.title("Главное меню")
        self.app.geometry("800x600")
        self.app.resizable(True, True)
        center_window(self.app)

    def _create_layout(self):
        """Создает макет экрана"""
        # Верхняя панель
        self.top_panel = TopPanel(self, self.app)
        self.top_panel.pack(side="top", fill="x", expand=False)

        # Основной контейнер для левой/центральной/правой панелей
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Левая панель (5%)
        self.left_panel = LeftPanel(container, self.app)
        self.left_panel.pack(side="left", fill="y", expand=False)

        # Центральная панель
        self.central_panel = CentralPanel(container, self.app)
        self.central_panel.pack(side="left", fill="both", expand=True)

        # Правая панель (20%)
        self.right_panel = RightPanel(container, self.app)
        self.right_panel.pack(side="left", fill="y", expand=False)