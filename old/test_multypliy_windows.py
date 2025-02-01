import tkinter as tk


def center_window(window, width, height):
    # Получаем ширину и высоту экрана
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Вычисляем координаты для центрирования окна
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Устанавливаем положение окна
    window.geometry(f"{width}x{height}+{x}+{y}")


def open_new_window():
    # Закрываем текущее окно
    root.destroy()

    # Создаем новое окно
    new_window = tk.Tk()
    new_window.title("Новое окно")

    # Центрируем новое окно
    center_window(new_window, 800, 600)

    label = tk.Label(new_window, text="Это новое окно!")
    label.pack(pady=20)

    new_window.mainloop()


# Создаем главное окно
root = tk.Tk()
root.title("Главное окно")

# Центрируем главное окно
center_window(root, 300, 200)

# Кнопка для перехода к новому окну
button = tk.Button(root, text="Перейти к новому окну", command=open_new_window)
button.pack(pady=20)

root.mainloop()