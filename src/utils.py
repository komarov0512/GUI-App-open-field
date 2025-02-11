import src.config as cfg
from tkinter import filedialog


def center_window(window):
    """Центрирование окна"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    # Центрирование
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def file_load():
    """Обработчик загрузки файла"""
    file_path = filedialog.askopenfilename(
        title="Выберите видео",
        filetypes=[("Video files", "*.mp4")]
    )
    if file_path:
        cfg.set_file_path(file_path)
        return file_path