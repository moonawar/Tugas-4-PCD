from tkinter import *
from gui.color import *
from gui.utils import *
import ctypes

class AppWindow(Tk):
    def __init__(self):
        super().__init__()

        # Corrects DPI scaling on Windows (Removes blurry visuals)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        self.title("Vehicle Recognition App")
        self.geometry("1280x720")
        self.resizable(False, False)

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
        create_space(self, bg=COLOR_PRIMARY)

        label = Label(self, text="Input Image", font=("Poppins", 14, "bold"), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY)
        label.pack(side="top", anchor="w", padx=24, pady=4)

        btn_image = PhotoImage(file="gui/assets/btn-choose-file.png")
        btn = Button(self, image=btn_image, fg=COLOR_PRIMARY, bg=COLOR_PRIMARY, bd=0)
        btn.image = btn_image
        btn.pack(side="top", anchor="w", padx=24, pady=4)

        self.selected_label = Label(self, text="No file selected", font=("Poppins", 12), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY)
        self.selected_label.pack(side="top", anchor="w", padx=24, pady=4)

        canvas = Canvas(self, width=300, height=300, bg=COLOR_SECONDARY, highlightthickness=0)
        canvas.pack(side="top", padx=24, pady=4, anchor="center")

        create_space(self, bg=COLOR_PRIMARY)

        btn_image = PhotoImage(file="gui/assets/btn-run.png")
        btn = Button(self, image=btn_image, bg=COLOR_PRIMARY, fg=COLOR_SECONDARY, bd=0)
        btn.image = btn_image
        btn.pack(side="top", anchor="center", padx=24, pady=4)

        pass

class Main(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=COLOR_PRIMARY_DARK)

        self.build()

    def build(self):
        pass