from mandelbrot_set import Mandelbrot
import tkinter as tk

class MandelbrotApp:
    def __init__(self, master):
        self.master = master
        self.mandelbrot = Mandelbrot(self.master)
        self.mandelbrot.canvas.bind("<Button-1>", self.zoom_in)
        self.mandelbrot.canvas.bind("<Button-3>", self.zoom_out)  # Changed to Button-3 for right-click

    def zoom_in(self, event):
        self.mandelbrot.zoom(-0.1)

    def zoom_out(self, event):
        self.mandelbrot.zoom(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MandelbrotApp(root)
    root.mainloop()
