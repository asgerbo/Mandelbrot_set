import os
import time
from tkinter import *
from PIL import Image, ImageTk
from mandelbrot import FractalRenderer  # Assuming the refactored Mandelbrot class is saved in a file named fractal_renderer.py
from multiprocessing import freeze_support


class FractalViewer(Frame):
    def __init__(self, parent, canvas_size, x_center=-0.75, y_center=0, scale=1.5, max_iter=None, img_width=None, img_height=None, save_image=False, use_multiprocessing=True):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Fractal Viewer")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)

        if img_width is None or img_height is None:
            img_width, img_height = canvas_size, canvas_size

        aspect_ratio = img_width / img_height
        self.canvas_width, self.canvas_height = (canvas_size, round(canvas_size / aspect_ratio)) if img_width > img_height else (round(canvas_size * aspect_ratio), canvas_size)

        self.fractal = FractalRenderer(self.canvas_width, self.canvas_height, x_center=x_center, y_center=y_center, scale=scale, max_iter=max_iter, img_width=img_width, img_height=img_height, use_multiprocessing=use_multiprocessing)
        self.palette = [(0, 0, 0), (255, 255, 255)]
        self.pixel_colors = []
        self.image = None
        self.save_image = save_image
        self.render()

        parent.bind("<Button-1>", self.zoom_in)
        parent.bind("<Button-3>", self.zoom_out)
        parent.bind("<Control-1>", self.pan_view)

    def zoom_in(self, event):
        self.fractal.zoom(event, 'in')
        self.render()

    def zoom_out(self, event):
        self.fractal.zoom(event, 'out')
        self.render()

    def pan_view(self, event):
        self.fractal.pan(event)
        self.render()

    def render(self):
        print('-' * 20)
        start_time = time.time()
        self.fractal.generate_pixels()
        self.assign_colors()
        self.paint_pixels()
        self.canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.canvas.pack(fill=BOTH, expand=1)
        print(f"Rendering took {round(time.time() - start_time, 2)} seconds")

    def assign_colors(self):
        self.pixel_colors = [self.palette[0] if pixel[2] == 0 else self.palette[1] for pixel in self.fractal.pixel_data]

    def paint_pixels(self):
        img = Image.new('RGB', (self.fractal.img_width, self.fractal.img_height), "black")
        pixel_map = img.load()
        for idx, pixel in enumerate(self.fractal.pixel_data):
            pixel_map[int(pixel[0]), int(pixel[1])] = self.pixel_colors[idx]
        self.image = img
        if self.save_image:
            self.save_image_to_disk()
        photo_img = ImageTk.PhotoImage(img.resize((self.canvas_width, self.canvas_height)))
        self.background = photo_img

    def save_image_to_disk(self):
        self.image.save(f"output/{time.strftime('%Y-%m-%d-%H:%M:%S')}.png", "PNG", optimize=True)


def main():
    root = Tk()
    screen_height = round(root.winfo_screenheight() * 0.9)
    app = FractalViewer(root, screen_height)
    root.geometry(f"{app.canvas_width}x{app.canvas_height}")
    root.mainloop()


if __name__ == '__main__':
    freeze_support()
    main()
