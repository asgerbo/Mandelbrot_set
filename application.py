import time
from tkinter import *
from PIL import Image, ImageTk
from mandelbrot_generation import Mandelbrot_Fractal
from multiprocessing import freeze_support
import colorsys


class Mandelbrot_Viewer(Frame):
    """
    This is the main class for the Mandelbrot Viewer. I use the __init__ statement to initialize the class. The super function states that this is a child class which comes from the frame class. This allows me to use tkinter methods and options that are common to all tkinter widgets. This one is a bit different, since we have set values for the x_center, y_center, scale, max_iter, img_width, img_height and use_multiprocessing. Using x_center = -0.5, y_center = 0 and scale = 2.1, seems to be good starting points after having played around with the values. A scale too high, and the set will be too small, and a scale too low, and the set will appear too big. 
    """
    def __init__(self, parent, canvas_size, x_center = -0.5, y_center = 0, scale = 2.1, max_iter = None, img_width = None, img_height = None):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Fractal Viewer")
        self.pack(fill = BOTH, expand=1)
        self.canvas = Canvas(self)

        if img_width is None or img_height is None:
            img_width, img_height = canvas_size, canvas_size

        aspect_ratio = 16 / 9
        self.canvas_width, self.canvas_height = (canvas_size, round(canvas_size / aspect_ratio)) if img_width > img_height else (round(canvas_size * aspect_ratio), canvas_size)

        self.fractal = Mandelbrot_Fractal(self.canvas_width, self.canvas_height, x_center=x_center, y_center=y_center, scale=scale, max_iter=max_iter, img_width=img_width, img_height=img_height)
        self.palette = [(0, 0, 0), (255, 255, 255)]
        self.pixel_colors = []
        self.image = None
        self.render()

    def render(self):
        """
        This is the function that renders the image on the canvas. I have used the time package to measure the time it takes to render the image, since I have been testing different computational methods to improve computational speed. Next i call the generate_pixels function from the Mandelbrot_Fractal class. I then assign the colors to the pixels, and finally paint the pixels on the canvas. To initialize the pixels on the canvas, i set the values 0,0 because i want it to fill the canvas starting from the very first pixel in the top left corer (North West). 
        """
        print('-' * 20)
        start_time = time.time()
        self.fractal.generate_pixels()
        self.assign_colors()
        self.paint_pixels()
        self.canvas.create_image(0, 0, image=self.background, anchor = 'nw')
        self.canvas.pack(fill = 'both', expand = 1)
        print(f"Generating canvas took {time.time() - start_time:.2f} seconds")

    def assign_colors(self):
        """
        Create an empty list for the pixel colors. I then loop through the pixel data and assign the colors to the pixels. I use the palette to assign the colors. The palette is a list of tuples, where each tuple contains the values for the color. The first tuple is the color for the pixels that are in the mandelbrot set, and the second tuple is the color for the pixels that are not in the mandelbrot set.

        This is important, since we are essentially getting 256 * 256 * 256 = 16777216 possible colors to plot on the plane. For this case it is not nessecary since the amount of computations will never reach this amount. But I have done this to show the increasing complexitity of the set. Also here there comes the issue of precision, because as far as i know, we can only be so precise for a set that is infinite. 
        """
        self.pixel_colors = []
        for x, y, iteration_count in self.fractal.pixel_data:
            if iteration_count == 0:
                color = self.palette[0]
            else:
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(iteration_count / self.fractal.max_iter, 1.0, 1.0 if iteration_count < self.fractal.max_iter else 0)]
                color = (r, g, b)
            self.pixel_colors.append(color)

    def paint_pixels(self):
        """
        I use the Image package to create a new image. I then use the load function to load the image into memory. I then loop through the pixel data and assign the colors to the pixels. I then use the ImageTk package to convert the image to a tkinter image. I then resize the image to fit the canvas.
        """
        img = Image.new('RGB', (self.fractal.img_width, self.fractal.img_height))
        pixel_map = img.load()
        for idx, pixel in enumerate(self.fractal.pixel_data):
            pixel_map[int(pixel[0]), int(pixel[1])] = self.pixel_colors[idx]
        photo_img = ImageTk.PhotoImage(img.resize((self.canvas_width, self.canvas_height)))
        self.background = photo_img

def run_program():
    """
    This is the main function. I use the freeze_support function from the multiprocessing package to prevent the program from crashing when running the program on Windows, if I dont include it will also crash on my mac. I then initialize the root window and set the size of the window. I then initialize the Mandelbrot_Viewer class and set the size of the window. I then call the mainloop function to run the program.
    """
    root = Tk()
    screen_height = round(root.winfo_screenheight() * 0.9)
    app = Mandelbrot_Viewer(root, screen_height)
    root.geometry(f"{app.canvas_width}x{app.canvas_height}")
    root.mainloop()

if __name__ == '__main__':
    freeze_support()
    run_program()
