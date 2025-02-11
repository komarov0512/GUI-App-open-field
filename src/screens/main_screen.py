from src.screens.base_screen import BaseScreen
from src.screens.main_screen_panels.top_panel import TopPanel
from src.screens.main_screen_panels.left_panel import LeftPanel
from src.screens.main_screen_panels.right_panel import RightPanel
from src.screens.main_screen_panels.central_panel import CentralPanel
from src.core.image_processor import ImageProcessor
from src.utils import center_window
import tkinter as tk

class MainScreen(BaseScreen):
    def __init__(self, master, app):
        super().__init__(master, app)
        self.img_proc = ImageProcessor()
        self._create_layout()

    def setup_window(self):
        self.app.title("Главное меню")
        self.app.geometry("1400x800")
        self.app.resizable(False, False)
        center_window(self.app)

    def _create_layout(self):
        """Создает макет экрана"""
        # Верхняя панель
        self.top_panel = TopPanel(self, self.app)
        self.top_panel.pack(side="top", fill="x", expand=False)

        # Основной контейнер для левой/центральной/правой панелей
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Левая панель
        self.left_panel = LeftPanel(container, self.app, self.img_proc, None, None)  # Создаем left_panel
        self.left_panel.place(x=0, y=0, width=200, height=800)

        # Центральная панель
        self.central_panel = CentralPanel(container, self.app, self.img_proc, self.left_panel)  # Передаем left_panel
        self.central_panel.place(x=200, y=0, width=1000, height=800)

        # Правая панель
        self.right_panel = RightPanel(container, self.app, self.img_proc, self.central_panel)
        self.right_panel.place(x=1200, y=0, width=200, height=800)

        # Обновляем ссылки на central_panel и right_panel в left_panel
        self.left_panel.central_panel = self.central_panel
        self.left_panel.right_panel = self.right_panel

