from multiprocessing import Pool
import numpy as np

convert = lambda value, min1, max1, min2, max2: min2 + ((value - min1) / (max1 - min1)) * (max2 - min2)

class Mandelbrot_Fractal:
    """
    I initialize the class with the __init__ statement. I set the default values for all the parameters I use in the class. Furthermore i set the aspect ratio to 16:9 by multipying both the width and height of the canvas created in the framework.py file. 
    """
    def __init__(self, canvas_width, canvas_height, x_center = None, y_center = None, scale = None, max_iter = 1000, img_width = None, img_height = None):
        self.img_width = np.round(canvas_width).astype(int)
        self.img_height = np.round(canvas_height).astype(int)
        self.max_iterations = max_iter if max_iter else 500
        self.x_center = x_center
        self.y_center = y_center
        self.aspect_ratio = 16 / 9
        self.scale = scale
        self.update_bounds()

    def update_bounds(self):
        """
        These are the max and min values for the canvas. I use the scale and aspect ratio to calculate the max and min values for the x and y axis. 
        """
        self.x_max = self.x_center + self.scale
        self.x_min = self.x_center - self.scale
        self.y_max = self.y_center + self.scale / self.aspect_ratio
        self.y_min = self.y_center - self.scale / self.aspect_ratio

    def generate_pixels(self):
        """
        This function generates the pixels for the mandelbrot set. I use a combination of packages here. The meshgrid function is rather convenient for this use case since it creates a grid of coordinates. I then use the column_stack function to stack the x and y coordinates together.

        I then use the starmap function from the multiprocessing package to calculate the escape time for each pixel. The starmap function is a bit like the map function, but it takes multiple arguments.
        """
        x_vals = np.linspace(0, self.img_width - 1, self.img_width)
        y_vals = np.linspace(0, self.img_height - 1, self.img_height)
        x_grid, y_grid = np.meshgrid(x_vals, y_vals)
        coords = np.column_stack((x_grid.ravel(), y_grid.ravel()))

        with Pool() as pool:
            self.pixel_data = pool.starmap(self.calculate_escape_time, coords)

    def calculate_escape_time(self, x, y):
        real = convert(x, 0, self.img_width, self.x_min, self.x_max)
        imag = convert(y, 0, self.img_height, self.y_max, self.y_min)
        c = complex(real, imag)
        z = complex(real, imag)
        for i in range(1, self.max_iterations):
            if abs(z) > 2:
                return (x, y, i)
            z = z * z + c
        return (x, y, 0)
    
