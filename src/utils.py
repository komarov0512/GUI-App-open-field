import tkinter as tk


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    # Центрирование
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")