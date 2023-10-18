from multiprocessing import Pool
import numpy as np

class FractalRenderer:
    def __init__(self, canvas_width, canvas_height, x_center=None, y_center=None, scale=None, max_iter=None, img_width=None, img_height=None, zoom=0.1, use_multiprocessing=True):
        self.img_width, self.img_height = (round(canvas_width * 16 / 9), round(canvas_height * 16 / 9)) if img_width is None or img_height is None else (img_width, img_height)
        self.max_iterations = max_iter if max_iter else 500
        self.x_center, self.y_center = x_center, y_center
        self.aspect_ratio = canvas_width / canvas_height
        self.scale = scale
        self.zoom_level = zoom
        self.use_multiprocessing = use_multiprocessing
        self.update_bounds()

    def update_bounds(self):
        self.x_max = self.x_center + self.scale
        self.x_min = self.x_center - self.scale
        self.y_max = self.y_center + self.scale / self.aspect_ratio
        self.y_min = self.y_center - self.scale / self.aspect_ratio

    def zoom(self, event, direction):
        self.x_center = self.map_value(event.x, 0, self.img_width, self.x_min, self.x_max)
        self.y_center = self.map_value(event.y, self.img_height, 0, self.y_min, self.y_max)
        self.scale *= (self.zoom_level if direction == 'in' else 1 / self.zoom_level)
        self.update_bounds()

    def pan(self, event):
        self.x_center = convert(event.x, 0, self.img_width, self.x_min, self.x_max)
        self.y_center = convert(event.y, self.img_height, 0, self.y_min, self.y_max)
        self.update_bounds()

    def generate_pixels(self):
        x_vals = np.linspace(0, self.img_width - 1, self.img_width)
        y_vals = np.linspace(0, self.img_height - 1, self.img_height)
        x_grid, y_grid = np.meshgrid(x_vals, y_vals)
        coords = np.column_stack((x_grid.ravel(), y_grid.ravel()))

        if self.use_multiprocessing:
            with Pool() as pool:
                self.pixel_data = pool.starmap(self.calculate_escape_time, coords, chunksize=1000)
        else:
            self.pixel_data = [self.calculate_escape_time(x, y) for x, y in coords]

    def calculate_escape_time(self, x, y):
        real = convert(x, 0, self.img_width, self.x_min, self.x_max)
        imag = convert(y, 0, self.img_height, self.y_max, self.y_min)
        c = complex(real, imag)
        z = c
        for i in range(1, self.max_iterations):
            if abs(z) > 2:
                return (x, y, i)
            z = z * z + c
        return (x, y, 0)

def convert(value, min1, max1, min2, max2):
    span1 = max1 - min1
    span2 = max2 - min2
    scaled_value = (value - min1) / span1
    return min2 + (scaled_value * span2)
