import cv2
import numpy as np
from PIL import Image, ImageTk

class Shape:
    def draw(self, image, scale_x, scale_y, highlight_color=None):
        raise NotImplementedError("Subclasses must implement this method")

class Quadrilateral(Shape):
    def __init__(self, points):
        self.points = points

    def draw(self, image, scale_x, scale_y, highlight_color=None):
        color = highlight_color if highlight_color else (0, 255, 0)
        pts = np.array([(int(x / scale_x), int(y / scale_y)) for (x, y) in self.points], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], isClosed=True, color=color, thickness=2)

class Circle(Shape):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def draw(self, image, scale_x, scale_y, highlight_color=None):
        color = highlight_color if highlight_color else (0, 255, 0)
        cv2.circle(image, (int(self.center[0] / scale_x), int(self.center[1] / scale_y)), int(self.radius / scale_x), color, 2)
        cv2.circle(image, (int(self.center[0] / scale_x), int(self.center[1] / scale_y)), 5, (0, 255, 0), -1)

class ImageProcessor:
    def __init__(self):
        self.current_image = None
        self.original_image = None
        self.drawing_quadrilateral = False
        self.quadrilaterals = []
        self.drawing_circle = False
        self.circles = []
        self.scale_x = 1.0
        self.scale_y = 1.0

    def load_image(self, path):
        self.original_image = cv2.imread(path)
        if self.original_image is None:
            raise ValueError("Изображение не загружено. Проверьте путь.")
        self.current_image = self.original_image.copy()

    def restore_original_image(self):
        self.current_image = self.original_image.copy()

    def get_current_image(self):
        return self.current_image

    def show_image(self, image, panel):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        self.tk_image = ImageTk.PhotoImage(image)
        panel.config(image=self.tk_image)
        panel.image = self.tk_image

    def get_image_coordinates(self, event, panel, scale_factor):
        # Получаем координаты с учетом масштабирования
        x = event.x / scale_factor
        y = event.y / scale_factor
        return int(x), int(y)

    def start_drawing_quadrilateral(self, panel, update_side_panel_callback, scale_factor):
        self.drawing_quadrilateral = True
        self.quadrilateral_points = []
        panel.bind("<Button-1>", lambda event: self.add_quadrilateral_point(event, panel, update_side_panel_callback, scale_factor))

    def add_quadrilateral_point(self, event, panel, update_side_panel_callback, scale_factor):
        if len(self.quadrilateral_points) < 4:
            img_x, img_y = self.get_image_coordinates(event, panel, scale_factor)
            self.quadrilateral_points.append((img_x, img_y))

            # Перерисовываем изображение с учетом добавленной точки
            self.restore_original_image()
            self.draw_all_objects()
            cv2.circle(self.current_image, (img_x, img_y), 5, (0, 0, 255), -1)
            self.show_image(self.current_image, panel)

            if len(self.quadrilateral_points) == 4:
                self.finish_quadrilateral(panel, update_side_panel_callback)

    def finish_quadrilateral(self, panel, update_side_panel_callback):
        if len(self.quadrilateral_points) == 4:
            quadrilateral = Quadrilateral(self.quadrilateral_points)
            self.quadrilaterals.append(quadrilateral)
            self.draw_all_objects()
            self.show_image(self.current_image, panel)
            update_side_panel_callback()

        self.drawing_quadrilateral = False
        panel.unbind("<Button-1>")

    def start_drawing_circle(self, panel, update_side_panel_callback, scale_factor):
        self.drawing_circle = True
        self.circle_points = []
        panel.bind("<Button-1>", lambda event: self.add_circle_point(event, panel, update_side_panel_callback, scale_factor))
        panel.bind("<Motion>", lambda event: self.preview_circle_motion(event, panel, scale_factor))

    def add_circle_point(self, event, panel, update_side_panel_callback, scale_factor):
        if len(self.circle_points) < 2:
            img_x, img_y = self.get_image_coordinates(event, panel, scale_factor)
            self.circle_points.append((img_x, img_y))

            if len(self.circle_points) == 2:
                self.finish_circle(panel, update_side_panel_callback)

    def preview_circle_motion(self, event, panel, scale_factor):
        if len(self.circle_points) == 1:
            img_x, img_y = self.get_image_coordinates(event, panel, scale_factor)
            center_x, center_y = self.circle_points[0]
            radius = int(np.sqrt((img_x - center_x) ** 2 + (img_y - center_y) ** 2))

            temp_image = self.current_image.copy()
            cv2.circle(temp_image, (center_x, center_y), radius, (255, 0, 0), 2)
            cv2.circle(temp_image, (center_x, center_y), 5, (0, 255, 0), -1)
            self.show_image(temp_image, panel)

    def finish_circle(self, panel, update_side_panel_callback):
        if len(self.circle_points) == 2:
            center_x, center_y = self.circle_points[0]
            radius = int(np.sqrt((self.circle_points[1][0] - center_x) ** 2 + (self.circle_points[1][1] - center_y) ** 2))

            circle = Circle((center_x, center_y), radius)
            self.circles.append(circle)
            self.draw_all_objects()
            self.show_image(self.current_image, panel)
            update_side_panel_callback()

        self.drawing_circle = False
        panel.unbind("<Button-1>")
        panel.unbind("<Motion>")

    def draw_all_objects(self, highlighted_quadrilateral_idx=None, highlighted_circle_idx=None):
        self.restore_original_image()

        for i, quadrilateral in enumerate(self.quadrilaterals):
            color = (0, 0, 255) if i == highlighted_quadrilateral_idx else None
            quadrilateral.draw(self.current_image, self.scale_x, self.scale_y, color)

        for i, circle in enumerate(self.circles):
            color = (0, 0, 255) if i == highlighted_circle_idx else None
            circle.draw(self.current_image, self.scale_x, self.scale_y, color)