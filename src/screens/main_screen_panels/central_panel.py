import tkinter as tk
from src.utils import file_load


class CentralPanel(tk.Frame):
    def __init__(self, master, app, img_proc, left_panel):
        super().__init__(master)
        self.app = app
        self.left_panel = left_panel
        self._create_widgets()
        self.img_proc = img_proc

    def _create_widgets(self):
        """Создает элементы центральной панели"""
        self.config(bg="white")
        self.btn_load = tk.Button(self, text="Загрузить файл",command=self._open_image, width=50, height=3)
        self.btn_load.place(relx=0.5, rely=0.5, anchor="center")

    def _open_image(self):
        file_path = file_load()
        self.btn_load.destroy()

        # Панель для отображения изображения
        self.img_cont = tk.Label(self, bg="white")
        self.img_cont.pack(fill=tk.BOTH, expand=True)

        self.img_proc.load_image(file_path)
        self._show_image()

    def _show_image(self):
        self.img_proc.set_scale_factor(
            self.winfo_width(),
            self.winfo_height()
        )
        self.img_proc.show_image(self.img_cont)
        # Активируем кнопки в left_panel
        self.left_panel.enable_buttons()