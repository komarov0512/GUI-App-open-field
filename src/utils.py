import src.config as cfg
from tkinter import filedialog
from functools import wraps
from typing import Callable, Optional


def debounce(wait: float) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def debounced(*args, **kwargs) -> None:
            if not args:
                return func(*args, **kwargs)

            self = args[0]
            root = getattr(self, 'app', None) or getattr(self, 'master', None)
            if not root:
                raise ValueError("Не удалось определить root")

            # Уникальный атрибут для хранения таймера
            timer_attr = f"_debounce_timer_{func.__name__}"
            timer_id = getattr(self, timer_attr, None)

            # Отменяем предыдущий таймер
            if timer_id:
                root.after_cancel(timer_id)

            # Создаем новый таймер
            new_timer_id = root.after(int(wait * 1000), lambda: func(*args, **kwargs))
            setattr(self, timer_attr, new_timer_id)

        return debounced
    return decorator

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