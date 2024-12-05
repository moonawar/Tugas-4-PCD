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
        main_frame = Frame(self, bg=COLOR_PRIMARY_DARK)
        main_frame.pack(side="top", fill="both", expand=True)

        main_frame.grid_rowconfigure(0, weight=1, uniform="y")
        main_frame.grid_rowconfigure(1, weight=10, uniform="y")
        main_frame.grid_columnconfigure(0, weight=1, uniform="y")
        main_frame.grid_columnconfigure(1, weight=3, uniform="y")

        top_bar = Header(main_frame)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="nswe")

        side_bar = SideBar(main_frame)
        side_bar.grid(row=1, column=0, sticky="nswe")

        main = Main(main_frame)
        main.grid(row=1, column=1, sticky="nswe")

    def start(self):
        self.mainloop()

class Header(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=COLOR_SECONDARY)

        self.build()

    def build(self):
        # pass
        icon = PhotoImage(file="gui/assets/icon.png")
        label = Label(self, image=icon, bg=COLOR_SECONDARY)
        label.image = icon
        label.pack(side="left", padx=20)

        label = Label(self, text="Vehicle Recognition App", font=("Poppins", 18, "bold"), fg=COLOR_PRIMARY, bg=COLOR_SECONDARY)
        label.pack(side="left")

        label = Label(self, text="IF4073 Pemrosesan Citra Digital", font=("Poppins", 12), fg=COLOR_PRIMARY, bg=COLOR_SECONDARY)
        label.pack(side="right", padx=16)

class SideBar(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=COLOR_PRIMARY)

        self.build()

    def build(self):
        pass

class Main(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=COLOR_PRIMARY_DARK)

        self.build()

    def build(self):
        pass