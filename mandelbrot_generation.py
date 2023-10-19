import time
import numpy as np
from tkinter import Tk, Canvas, BOTH
from PIL import Image, ImageTk
from multiprocessing import Pool, freeze_support
import colorsys

background = None

reshape = lambda value, minimum_x, maximum_x, minimum_y, maximum_y: minimum_y + (value - minimum_x) / (maximum_x - minimum_x) * (maximum_y - minimum_y)

def calculate_limits(x_origin, y_origin, scale, aspect_ratio):
    """
    Calculating the limits for the cartesian plane (2-D). 
    """
    y_upper = y_origin + scale / aspect_ratio
    x_upper = x_origin + scale
    y_lower = y_origin - scale / aspect_ratio
    x_lower = x_origin - scale
    return x_lower, x_upper, y_lower, y_upper

def calculate_escape_time(x, y, x_lower, x_upper, y_upper, y_lower, maximum_iterations, frame_dimensions_x, frame_dimensions_y):
    """
    Usage of the escape time algorithm, which stops the iteration if the the sum of the real and imaginary parts exceed 4, it will no longer be a part of the set. So we will return the values for that specific point if that happens for the specific iteration the loop is doing. 
    """
    real_part = reshape(x, 0, frame_dimensions_x, x_lower, x_upper)
    imaginary_part = reshape(y, 0, frame_dimensions_y, y_upper, y_lower)
    complex_number = complex(real_part, imaginary_part) 
    z_value = 0

    for i in range(0, maximum_iterations):
        if abs(z_value + complex_number) > 4:
            return x, y, i
        z_value = z_value * z_value + complex_number
    return x, y, 0

def generate_pixel_map(frame_dimensions_x, frame_dimensions_y, x_lower, x_upper, y_lower, y_upper, maximum_iterations):
    """
    Here i use Numpy's library to generate the map for which the pixels should be colored. I use a combination of linspace and meshgrid, since these are extremely convenient ways of representing a plot and then mapping the colors to the coordinates. Meshgrid takes 1-D arrays and turns them into n-D arrays. 
    """
    x_range = np.linspace(0, frame_dimensions_x - 1, frame_dimensions_x)
    y_range = np.linspace(0, frame_dimensions_y - 1, frame_dimensions_y)
    x_matrix, y_matrix = np.meshgrid(x_range, y_range)
    points = np.column_stack((x_matrix.flatten(), y_matrix.flatten()))

    with Pool() as pool:
        return pool.starmap(calculate_escape_time, [(x, y, x_lower, x_upper, y_upper, y_lower, maximum_iterations, frame_dimensions_x, frame_dimensions_y) for x, y in points])

def render(canvas, canvas_width, canvas_height, pixel_data):
    """
    Here i use some of the features both from Tkinter and Pillow to generate the image. Also i map the colors to each of the iteration, which returned (x, y, i) or (x, y, 0). Furthermore i print the time to took to render the plot, since I have been testing different computations to improve speed and having a point of reference is always a good idea.
    """
    global background
    start_time = time.time()
    img = Image.new('RGB', (canvas_width, canvas_height))
    pixels = img.load()

    for x, y, iteration in pixel_data:
        color = (0, 0, 0) if iteration == 0 else tuple(int(c * 255) for c in colorsys.hsv_to_rgb(iteration / 1000, 1, 1))
        pixels[x, y] = color

    background = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image = background, anchor='nw')
    canvas.pack(fill = 'both', expand = 1)
    print(f"Rendering took {time.time() - start_time:.2f} seconds")

if __name__ == '__main__':
    """
    Now the conclusion enter the picture. I generate the canvas using Tkinter and define the sequence in which the plotting should be done. I also use freeze_support() since my program was crashing if this was not included. This was very weird to me since the documentation said that this was for windows only, but it crashed as well on my mac. 
    """
    freeze_support()
    generate = Tk()
    aspect_ratio = 16 / 9
    canvas_dimensions = round(generate.winfo_screenheight() * 1.5)
    canvas_width = canvas_dimensions
    canvas_height = round(canvas_dimensions / aspect_ratio)
    canvas = Canvas(generate)
    canvas.pack(fill=BOTH, expand=1)

    pixel_data = generate_pixel_map(canvas_width, canvas_height, * calculate_limits(-0.5, 0, 2.1, aspect_ratio), 1000)
    render(canvas, canvas_width, canvas_height, pixel_data)

    generate.title("Fractal Viewer")
    generate.geometry(f"{canvas_width}x{canvas_height}")
    generate.mainloop()
