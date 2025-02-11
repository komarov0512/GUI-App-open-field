import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk
from image_processor import ImageProcessor, Quadrilateral, Circle


class ImageAnnotationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotation Tool")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height - 70}+0+0")

        self.image_processor = ImageProcessor()
        self.selected_figure = None
        self.scale_factor = 1.0  # Коэффициент масштабирования

        self.create_widgets()

    def create_widgets(self):
        # Основной фрейм для изображения и боковой панели
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм для изображения
        self.image_frame = tk.Frame(main_frame)
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Панель для отображения изображения
        self.panel = tk.Label(self.image_frame, bg="gray")
        self.panel.pack(fill=tk.BOTH, expand=True)

        # Боковая панель для отображения нарисованных объектов
        self.side_panel = tk.Frame(main_frame, width=300, bg="lightgray")
        self.side_panel.pack(side=tk.RIGHT, fill=tk.Y)

        # Фрейм для кнопок (фиксированный внизу)
        self.button_frame = tk.Frame(self.root, bg="black")
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Кнопка для выбора файла
        select_button = tk.Button(self.button_frame, text="Выбрать изображение", command=self.select_file, bg="black",
                                  fg="white", font=("Arial", 12), borderwidth=0, highlightthickness=0)
        select_button.pack(side=tk.LEFT, padx=10)

        # Кнопка для начала рисования четырехугольника
        quadrilateral_button = tk.Button(self.button_frame, text="Нарисовать четырехугольник",
                                         command=self.start_drawing_quadrilateral, bg="black", fg="white",
                                         font=("Arial", 12), borderwidth=0, highlightthickness=0)
        quadrilateral_button.pack(side=tk.LEFT, padx=10)

        # Кнопка для начала рисования круга
        circle_button = tk.Button(self.button_frame, text="Нарисовать круг", command=self.start_drawing_circle, bg="black",
                                  fg="white", font=("Arial", 12), borderwidth=0, highlightthickness=0)
        circle_button.pack(side=tk.LEFT, padx=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            # filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")]
        )
        if file_path:
            self.image_processor.load_image(file_path)
            self.show_image(self.image_processor.get_current_image())

    def show_image(self, image):
        # Преобразуем изображение в формат, подходящий для Tkinter
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # Рассчитываем доступную область для изображения
        available_width = self.image_frame.winfo_width() - 20  # Учитываем отступы
        available_height = self.image_frame.winfo_height() - 20

        # Масштабируем изображение, чтобы оно помещалось в доступную область
        img_width, img_height = image.size
        self.scale_factor = min(available_width / img_width, available_height / img_height)
        new_width = int(img_width * self.scale_factor)
        new_height = int(img_height * self.scale_factor)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Отображаем масштабированное изображение
        self.tk_image = ImageTk.PhotoImage(image)
        self.panel.configure(image=self.tk_image)
        self.panel.image = self.tk_image

    def start_drawing_quadrilateral(self):
        self.image_processor.start_drawing_quadrilateral(self.panel, self.update_side_panel, self.scale_factor)

    def start_drawing_circle(self):
        self.image_processor.start_drawing_circle(self.panel, self.update_side_panel, self.scale_factor)

    def update_side_panel(self):
        for widget in self.side_panel.winfo_children():
            widget.destroy()

        tk.Label(self.side_panel, text="Нарисованные объекты", font=("Arial", 14), bg="lightgray").pack(pady=10)

        for i, quadrilateral in enumerate(self.image_processor.quadrilaterals):
            frame = tk.Frame(self.side_panel, bg="lightgray")
            frame.pack(fill=tk.X)

            label = tk.Label(frame, text=f"Quadrilateral {i + 1}", bg="lightgray")
            label.pack(side=tk.LEFT, padx=5)
            label.bind("<Button-1>", lambda event, idx=i: self.highlight_quadrilateral(idx))

            delete_button = tk.Button(frame, text="Удалить", command=lambda idx=i: self.delete_quadrilateral(idx))
            delete_button.pack(side=tk.RIGHT, padx=5)

            if self.selected_figure == ("quadrilateral", i):
                label.config(bg="yellow")

        for i, circle in enumerate(self.image_processor.circles):
            frame = tk.Frame(self.side_panel, bg="lightgray")
            frame.pack(fill=tk.X)

            label = tk.Label(frame, text=f"Circle {i + 1}", bg="lightgray")
            label.pack(side=tk.LEFT, padx=5)
            label.bind("<Button-1>", lambda event, idx=i: self.highlight_circle(idx))

            delete_button = tk.Button(frame, text="Удалить", command=lambda idx=i: self.delete_circle(idx))
            delete_button.pack(side=tk.RIGHT, padx=5)

            if self.selected_figure == ("circle", i):
                label.config(bg="yellow")

    def highlight_quadrilateral(self, index):
        self.selected_figure = ("quadrilateral", index)
        self.image_processor.draw_all_objects(highlighted_quadrilateral_idx=index)
        self.show_image(self.image_processor.current_image)
        self.update_side_panel()

    def highlight_circle(self, index):
        self.selected_figure = ("circle", index)
        self.image_processor.draw_all_objects(highlighted_circle_idx=index)
        self.show_image(self.image_processor.current_image)
        self.update_side_panel()

    def delete_quadrilateral(self, index):
        if 0 <= index < len(self.image_processor.quadrilaterals):
            self.image_processor.quadrilaterals.pop(index)
            self.image_processor.draw_all_objects()
            self.show_image(self.image_processor.current_image)
            self.update_side_panel()

    def delete_circle(self, index):
        if 0 <= index < len(self.image_processor.circles):
            self.image_processor.circles.pop(index)
            self.image_processor.draw_all_objects()
            self.show_image(self.image_processor.current_image)
            self.update_side_panel()