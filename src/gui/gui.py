from tkinter import Tk
import ctypes

class AppWindow(Tk):
    def __init__(self):
        super().__init__()

        # Corrects DPI scaling on Windows
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        self.title("Vehicle Recognition App")
        self.geometry("1280x720")

    def start(self):
        self.mainloop()