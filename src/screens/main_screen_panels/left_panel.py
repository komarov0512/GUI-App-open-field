import tkinter as tk


class LeftPanel(tk.Frame):
    def __init__(self, master, app, img_proc, central_panel, right_panel):
        super().__init__(master)
        self.app = app
        self.central_panel = central_panel
        self.right_panel = right_panel
        self._create_widgets()
        self.img_proc = img_proc

    def _create_widgets(self):
        """Создает элементы левой панели"""
        self.config(bg="#e0e0e0")
        self.label = tk.Label(self, text="Инструменты", bg="#e0e0e0")
        self.label.pack(fill="x")

        self.quadrilateral_button = tk.Button(self, text="Нарисовать четырехугольник",
                                         command=self.start_drawing_quadrilateral,
                                         bg="#e0e0e0",
                                         state=tk.DISABLED)
        self.quadrilateral_button.pack(fill="x")

        self.circle_button = tk.Button(self, text="Нарисовать круг",
                                  command=self.start_drawing_circle,
                                  bg="#e0e0e0",
                                  state=tk.DISABLED)
        self.circle_button.pack(fill="x")

    def enable_buttons(self):
        self.quadrilateral_button.config(state=tk.NORMAL)
        self.circle_button.config(state=tk.NORMAL)

    def start_drawing_quadrilateral(self):
        self.img_proc.start_drawing_quadrilateral(self.central_panel.img_cont, self.right_panel.update_side_panel)

    def start_drawing_circle(self):
        self.img_proc.start_drawing_circle(self.central_panel.img_cont, self.right_panel.update_side_panel)