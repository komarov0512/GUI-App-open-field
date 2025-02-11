import cv2
import numpy as np
from PIL import Image, ImageTk

class Quadrilateral:
    def __init__(self, points):
        self.points = points

    def draw(self, image, highlight_color=None):
        color = highlight_color if highlight_color else (0, 255, 0)
        pts = np.array([(int(x), int(y)) for (x, y) in self.points], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], isClosed=True, color=color, thickness=2)

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def draw(self, image, highlight_color=None):
        color = highlight_color if highlight_color else (0, 255, 0)
        cv2.circle(image, (int(self.center[0]), int(self.center[1])), int(self.radius), color, 2)
        cv2.circle(image, (int(self.center[0]), int(self.center[1])), 5, (0, 255, 0), -1)

class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.quadrilaterals = []
        self.circles = []

    def load_image(self, path):
        cap = cv2.VideoCapture(path)
        ret, frame = cap.read()
        self.original_image = frame
        self.current_image = self.original_image.copy()
        cap.release()

    def get_image(self, image=None):
        image = self.current_image if image is None else image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        img_width, img_height = image.size
        new_width = int(img_width * self.scale_factor)
        new_height = int(img_height * self.scale_factor)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def set_scale_factor(self, width, height):
        img_height, img_width = self.original_image.shape[:2]
        self.scale_factor = min(width / img_width, height / img_height)
        scaled_width = int(img_width * self.scale_factor)
        scaled_height = int(img_height * self.scale_factor)
        self.pad_x = (width - scaled_width) // 2
        self.pad_y = (height - scaled_height) // 2

    def show_image(self, container, image=None):
        image = self.get_image(image)
        container.config(image=image)
        container.image = image

    def restore_original_image(self):
        self.current_image = self.original_image.copy()

    def get_image_coordinates(self, event):
        x = (event.x - self.pad_x) / self.scale_factor
        y = (event.y - self.pad_y) / self.scale_factor
        return int(x), int(y)

    def start_drawing_quadrilateral(self, img_cont, update_side_panel_callback):
        self.quadrilateral_points = []
        img_cont.bind("<Button-1>", lambda event: self.add_quadrilateral_point(event, img_cont, update_side_panel_callback))

    def _draw_quadrilateral_points(self):
        for i, (x, y) in enumerate(self.quadrilateral_points):
            cv2.circle(self.current_image, (x, y), 5, (0, 0, 255), -1)
            if i > 0:
                prev_x, prev_y = self.quadrilateral_points[i - 1]
                cv2.line(self.current_image, (prev_x, prev_y), (x, y), (255, 0, 0), 2)

    def add_quadrilateral_point(self, event, img_cont, update_side_panel_callback):
        if len(self.quadrilateral_points) < 4:
            img_x, img_y = self.get_image_coordinates(event)
            self.quadrilateral_points.append((img_x, img_y))
            self.restore_original_image()
            self.draw_all_objects()
            self._draw_quadrilateral_points()
            self.show_image(img_cont)
            if len(self.quadrilateral_points) == 4:
                self.finish_quadrilateral(img_cont, update_side_panel_callback)

    def finish_quadrilateral(self, img_cont, update_side_panel_callback):
        if len(self.quadrilateral_points) == 4:
            quadrilateral = Quadrilateral(self.quadrilateral_points)
            self.quadrilaterals.append(quadrilateral)
            self.draw_all_objects()
            self.show_image(img_cont)
            update_side_panel_callback()
        img_cont.unbind("<Button-1>")

    def start_drawing_circle(self, img_cont, update_side_panel_callback):
        self.circle_points = []
        img_cont.bind("<Button-1>", lambda event: self.add_circle_point(event, img_cont, update_side_panel_callback))
        img_cont.bind("<Motion>", lambda event: self.preview_circle_motion(event, img_cont))

    def add_circle_point(self, event, img_cont, update_side_panel_callback):
        if len(self.circle_points) < 2:
            img_x, img_y = self.get_image_coordinates(event)
            self.circle_points.append((img_x, img_y))
            if len(self.circle_points) == 2:
                self.finish_circle(img_cont, update_side_panel_callback)

    def preview_circle_motion(self, event, img_cont):
        if len(self.circle_points) == 1:
            img_x, img_y = self.get_image_coordinates(event)
            center_x, center_y = self.circle_points[0]
            radius = int(np.sqrt((img_x - center_x) ** 2 + (img_y - center_y) ** 2))
            temp_image = self.current_image.copy()
            cv2.circle(temp_image, (center_x, center_y), radius, (255, 0, 0), 2)
            cv2.circle(temp_image, (center_x, center_y), 5, (0, 255, 0), -1)
            self.show_image(img_cont, temp_image)

    def finish_circle(self, img_cont, update_side_panel_callback):
        if len(self.circle_points) == 2:
            center_x, center_y = self.circle_points[0]
            radius = int(np.sqrt((self.circle_points[1][0] - center_x) ** 2 + (self.circle_points[1][1] - center_y) ** 2))
            circle = Circle((center_x, center_y), radius)
            self.circles.append(circle)
            self.draw_all_objects()
            self.show_image(img_cont)
            update_side_panel_callback()
        img_cont.unbind("<Button-1>")
        img_cont.unbind("<Motion>")

    def draw_all_objects(self, highlighted_quadrilateral_idx=None, highlighted_circle_idx=None):
        self.restore_original_image()
        for i, quadrilateral in enumerate(self.quadrilaterals):
            color = (0, 0, 255) if i == highlighted_quadrilateral_idx else None
            quadrilateral.draw(self.current_image, color)
        for i, circle in enumerate(self.circles):
            color = (0, 0, 255) if i == highlighted_circle_idx else None
            circle.draw(self.current_image, color)