from src.screens.base_screen import BaseScreen
from src.screens.main_screen_panels.top_panel import TopPanel
from src.screens.main_screen_panels.left_panel import LeftPanel
from src.screens.main_screen_panels.right_panel import RightPanel
from src.screens.main_screen_panels.central_panel import CentralPanel
from src.core.image_processor import ImageProcessor
from src.utils import center_window, debounce
import tkinter as tk

class MainScreen(BaseScreen):
    def __init__(self, master, app):
        super().__init__(master, app)
        self.img_proc = ImageProcessor()
        self._create_layout()
        self._is_processing_resize = False
        self._update_img_proc()

    def setup_window(self):
        self.app.title("Главное меню")
        self.app.geometry("1400x800")
        self.app.resizable(True, True)
        center_window(self.app)

    def _create_layout(self):
        """Создает адаптивный макет экрана"""
        # Верхняя панель
        self.top_panel = TopPanel(self, self.app)
        self.top_panel.pack(side="top", fill="x", expand=False)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Отключаем автоматическое изменение размера контейнера
        container.pack_propagate(False)
        container.grid_propagate(False)

        # Веса колонок: 1:5:1 (с минимальными размерами)
        container.grid_columnconfigure(0, weight=1, minsize=200)  # Левая панель
        container.grid_columnconfigure(1, weight=5, minsize=600)  # Центральная
        container.grid_columnconfigure(2, weight=1, minsize=200)  # Правая
        container.grid_rowconfigure(0, weight=1)

        # Левая панель
        self.left_panel = LeftPanel(container, self.app, self.img_proc, None, None)
        self.left_panel.grid(row=0, column=0, sticky="nsew")

        # Центральная панель
        self.central_panel = CentralPanel(container, self.app, self.img_proc, self.left_panel)
        self.central_panel.grid(row=0, column=1, sticky="nsew")

        # Правая панель
        self.right_panel = RightPanel(container, self.app, self.img_proc, self.central_panel)
        self.right_panel.grid(row=0, column=2, sticky="nsew")

        # Обновляем ссылки на панели
        self.left_panel.central_panel = self.central_panel
        self.left_panel.right_panel = self.right_panel

    def _update_img_proc(self):
        self.app.bind("<Configure>", self.on_resize)
        # Отвязываем от других виджетов (на всякий случай)
        self.unbind("<Configure>")
        self.left_panel.unbind("<Configure>")
        self.right_panel.unbind("<Configure>")
        self.central_panel.unbind("<Configure>")

    @debounce(1.0)
    def on_resize(self, event):
        print(f"Событие от: {event.widget}")
        if event.widget != self.app:
            print("Игнорируем событие от вложенного виджета")
            return
        if self._is_processing_resize:
            print("рекурсия")
            return
        self._is_processing_resize = True

        # Логика обработки
        self.central_panel._show_image()

        self._is_processing_resize = False