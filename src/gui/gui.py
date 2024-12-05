from tkinter import *
from gui.color import *
import ctypes

class AppWindow(Tk):
    def __init__(self):
        super().__init__()

        # Corrects DPI scaling on Windows
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        self.title("Vehicle Recognition App")
        self.geometry("1280x720")

        self.build()

    def build(self):
        self.top_bar = TopBar(self)
        self.top_bar.pack(side="top", fill="x")

        self.main_frame = Frame(self, bg=COLOR_PRIMARY_DARK)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}

    def start(self):
        self.mainloop()


class TopBar(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=COLOR_SECONDARY)
        self.pack(side="top", fill="x")

        self.build()

    def build(self):
        icon = PhotoImage(file="gui/assets/icon.png")
        label = Label(self, image=icon, bg=COLOR_SECONDARY)
        label.image = icon
        label.pack(side="left", padx=20)

        label = Label(self, text="Vehicle Recognition App", font=("Poppins", 18, "bold"), fg=COLOR_PRIMARY, bg=COLOR_SECONDARY)
        label.pack(side="left")

        label = Label(self, text="IF4073 Pemrosesan Citra Digital", font=("Poppins", 12), fg=COLOR_PRIMARY, bg=COLOR_SECONDARY)
        label.pack(side="right", padx=16)