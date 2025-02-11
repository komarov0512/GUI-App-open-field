# import tkinter as tk
#
#
# class RightPanel(tk.Frame):
#     def __init__(self, master, app, img_proc):
#         super().__init__(master)
#         self.app = app
#         self._create_widgets()
#         self.img_proc = img_proc
#
#     def _create_widgets(self):
#         """Создает элементы правой панели"""
#         self.config(
#             bg="#e0e0e0",
#             width=int(self.app.winfo_screenwidth() * 0.2)
#         )
#
#         label = tk.Label(self, text="Правая панель", bg="#e0e0e0")
#         label.pack(pady=20)
#
#     def update_side_panel(self):
#         for widget in self.winfo_children():
#             widget.destroy()
#
#         tk.Label(self, text="Нарисованные объекты", font=("Arial", 14), bg="lightgray").pack(pady=10)
#
#         for i, quadrilateral in enumerate(self.img_proc.quadrilaterals):
#             frame = tk.Frame(self, bg="lightgray")
#             frame.pack(fill=tk.X)
#
#             label = tk.Label(frame, text=f"Quadrilateral {i + 1}", bg="lightgray")
#             label.pack(side=tk.LEFT, padx=5)
#             label.bind("<Button-1>", lambda event, idx=i: self.highlight_quadrilateral(idx))
#
#             delete_button = tk.Button(frame, text="Удалить", command=lambda idx=i: self.delete_quadrilateral(idx))
#             delete_button.pack(side=tk.RIGHT, padx=5)
#
#             if self.selected_figure == ("quadrilateral", i):
#                 label.config(bg="yellow")
#
#         for i, circle in enumerate(self.img_proc.circles):
#             frame = tk.Frame(self, bg="lightgray")
#             frame.pack(fill=tk.X)
#
#             label = tk.Label(frame, text=f"Circle {i + 1}", bg="lightgray")
#             label.pack(side=tk.LEFT, padx=5)
#             label.bind("<Button-1>", lambda event, idx=i: self.highlight_circle(idx))
#
#             delete_button = tk.Button(frame, text="Удалить", command=lambda idx=i: self.delete_circle(idx))
#             delete_button.pack(side=tk.RIGHT, padx=5)
#
#             if self.selected_figure == ("circle", i):
#                 label.config(bg="yellow")
#
#     def highlight_quadrilateral(self, index):
#         self.selected_figure = ("quadrilateral", index)
#         self.img_proc.draw_all_objects(highlighted_quadrilateral_idx=index)
#         self.show_image(self.img_proc.current_image)
#         self.update_side_panel()
#
#     def highlight_circle(self, index):
#         self.selected_figure = ("circle", index)
#         self.img_proc.draw_all_objects(highlighted_circle_idx=index)
#         self.show_image(self.img_proc.current_image)
#         self.update_side_panel()
#
#     def delete_quadrilateral(self, index):
#         if 0 <= index < len(self.img_proc.quadrilaterals):
#             self.img_proc.quadrilaterals.pop(index)
#             self.img_proc.draw_all_objects()
#             self.show_image(self.img_proc.current_image)
#             self.update_side_panel()
#
#     def delete_circle(self, index):
#         if 0 <= index < len(self.img_proc.circles):
#             self.img_proc.circles.pop(index)
#             self.img_proc.draw_all_objects()
#             self.show_image(self.img_proc.current_image)
#             self.update_side_panel()

import tkinter as tk


class RightPanel(tk.Frame):
    def __init__(self, master, app, img_proc, central_panel):
        super().__init__(master)
        self.app = app
        self.img_proc = img_proc
        self.central_panel = central_panel
        self._create_widgets()
        self.selected_figure = None

    def _create_widgets(self):
        """Создает элементы правой панели"""
        self.config(bg="#e0e0e0")
        label = tk.Label(self, text="Список объектов:", bg="#e0e0e0")
        label.pack(pady=10, padx=5)

    def create_figure_widget(self, parent, text, index, figure_type):
        """
        Создает фрейм с меткой и кнопкой удаления для фигуры.

        :param parent: Родительский виджет (например, self).
        :param text: Текст для метки (например, "Quadrilateral 1").
        :param index: Индекс фигуры в списке.
        :param figure_type: Тип фигуры ("quadrilateral" или "circle").
        :return: Фрейм с виджетами.
        """
        frame = tk.Frame(parent, bg="lightgray")
        frame.pack(fill=tk.X)

        # Метка с названием фигуры
        label = tk.Label(frame, text=text, bg="lightgray")
        label.pack(side=tk.LEFT, padx=5)

        # Привязка события для выделения фигуры
        label.bind("<Button-1>", lambda event, idx=index, ft=figure_type: self.highlight_figure(idx, ft))

        # Кнопка удаления
        delete_button = tk.Button(
            frame,
            text="Удалить",
            command=lambda idx=index, ft=figure_type: self.delete_figure(idx, ft)
        )
        delete_button.pack(side=tk.RIGHT, padx=5)

        # Выделение, если фигура выбрана
        if self.selected_figure == (figure_type, index):
            label.config(bg="yellow")

        return frame

    def create_figures_widgets(self, figures, figure_type):
        """
        Создает виджеты для списка фигур.

        :param figures: Список фигур (например, self.img_proc.quadrilaterals).
        :param figure_type: Тип фигуры ("quadrilateral" или "circle").
        """
        for i, figure in enumerate(figures):
            self.create_figure_widget(
                parent=self,
                text=f"{figure_type.capitalize()} {i + 1}",
                index=i,
                figure_type=figure_type
            )

    def update_side_panel(self):
        """Обновляет правую панель с нарисованными объектами."""
        # Очищаем панель
        for widget in self.winfo_children():
            widget.destroy()

        # Заголовок
        tk.Label(self, text="Нарисованные объекты", font=("Arial", 14), bg="lightgray").pack(pady=10)

        # Четырехугольники
        self.create_figures_widgets(self.img_proc.quadrilaterals, "quadrilateral")

        # Круги
        self.create_figures_widgets(self.img_proc.circles, "circle")

    def highlight_figure(self, index, figure_type):
        """
        Выделяет фигуру по индексу и типу.

        :param index: Индекс фигуры.
        :param figure_type: Тип фигуры ("quadrilateral" или "circle").
        """
        self.selected_figure = (figure_type, index)

        if figure_type == "quadrilateral":
            self.img_proc.draw_all_objects(highlighted_quadrilateral_idx=index)
        elif figure_type == "circle":
            self.img_proc.draw_all_objects(highlighted_circle_idx=index)

        self.img_proc.show_image(self.central_panel.img_cont)
        self.update_side_panel()

    def delete_figure(self, index, figure_type):
        """
        Удаляет фигуру по индексу и типу.

        :param index: Индекс фигуры.
        :param figure_type: Тип фигуры ("quadrilateral" или "circle").
        """
        if figure_type == "quadrilateral":
            if 0 <= index < len(self.img_proc.quadrilaterals):
                self.img_proc.quadrilaterals.pop(index)
        elif figure_type == "circle":
            if 0 <= index < len(self.img_proc.circles):
                self.img_proc.circles.pop(index)

        # Перерисовываем изображение и обновляем панель
        self.img_proc.draw_all_objects()
        self.img_proc.show_image(self.central_panel.img_cont)
        self.update_side_panel()