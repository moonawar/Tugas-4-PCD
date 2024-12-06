from tkinter import *
from gui.color import *
from gui.utils import *
import ctypes

from PIL import Image, ImageTk

PLACEHOLDER_IMAGE_PIL = Image.open("gui/assets/placeholder.png")

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

        button_image = PhotoImage(file="gui/assets/btn-choose-file.png")
        button = Button(self, image=button_image, fg=COLOR_PRIMARY, bg=COLOR_PRIMARY, bd=0)
        button.image = button_image
        button.pack(side="top", anchor="w", padx=24, pady=4)

        self.selected_label = Label(self, text="No file selected", font=("Poppins", 12), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY)
        self.selected_label.pack(side="top", anchor="w", padx=24, pady=4)

        placeholder_image = PLACEHOLDER_IMAGE_PIL.resize((300, 300), Image.ANTIALIAS)
        placeholder_image = ImageTk.PhotoImage(placeholder_image)
        input_image = Label(self, image=placeholder_image, bg=COLOR_PRIMARY)
        input_image.image = placeholder_image
        input_image.pack(side="top", anchor="center", padx=24, pady=4)

        create_space(self, bg=COLOR_PRIMARY)

        button_image = PhotoImage(file="gui/assets/btn-run.png")
        button = Button(self, image=button_image, bg=COLOR_PRIMARY, fg=COLOR_SECONDARY, bd=0)
        button.image = button_image
        button.pack(side="top", anchor="center", padx=24, pady=4)

        pass

class Main(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=COLOR_PRIMARY_DARK)

        self.build()

    def build(self):
        self.grid_rowconfigure(0, weight=3, uniform="y")
        self.grid_rowconfigure(1, weight=1, uniform="y")
        self.grid_columnconfigure(0, weight=1, uniform="y")
        self.grid_columnconfigure(1, weight=1, uniform="y")

        result_pretrained_frame = Result(self)
        result_pretrained_frame.set_label("Result (Pretrained Model)")
        result_pretrained_frame.set_output_path("../output/")
        result_pretrained_frame.grid(row=0, column=0, sticky="nswe")

        result_improc_frame = Result(self)
        result_improc_frame.set_label("Result (Image Processing)")
        result_improc_frame.set_output_path("../output/")
        result_improc_frame.grid(row=0, column=1, sticky="nswe")

        bottom_frame = Frame(self)
        bottom_frame.configure(bg=COLOR_PRIMARY_DARK)
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nswe")

        create_space(bottom_frame, bg=COLOR_PRIMARY_DARK, sizey=2)

        self.statusText = StringVar(value="Status: Idle")
        status = Label(bottom_frame, textvariable=self.statusText, font=("Poppins", 12, "bold"), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY_DARK)
        status.pack(side="top", padx=(56, 0), anchor="w")

        self.messageText = StringVar(value="Waiting for the application to be run!")
        message = Label(bottom_frame, textvariable=self.messageText, font=("Poppins", 12), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY_DARK)
        message.pack(side="top", padx=(56, 0), anchor="w")
        pass

class Result(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=COLOR_PRIMARY_DARK)

        self.build()

    def build(self):
        create_space(self, bg=COLOR_PRIMARY_DARK)

        self.outputPath = ""
        self.labelText = StringVar(value="Result")
        self.label = Label(self, textvariable=self.labelText, font=("Poppins", 14, "bold"), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY_DARK)
        self.label.pack(side="top", anchor="w", padx=(56, 0), pady=4)

        placeholder_image = PLACEHOLDER_IMAGE_PIL.resize((360, 360), Image.ANTIALIAS)
        placeholder_image = ImageTk.PhotoImage(placeholder_image)
        output_image = Label(self, image=placeholder_image, bg=COLOR_PRIMARY_DARK)
        output_image.image = placeholder_image
        output_image.pack(side="top", anchor="center", padx=24, pady=4)

        create_space(self, bg=COLOR_PRIMARY_DARK)

        button_image = PhotoImage(file="gui/assets/btn-save.png")
        button = Button(self, image=button_image, bg=COLOR_PRIMARY_DARK, fg=COLOR_PRIMARY_DARK, bd=0)
        button.image = button_image
        button.pack(side="top", anchor="w", padx=(56, 0))

    def set_label(self, text):
        self.labelText.set(text)

    def set_output_path(self, path):
        self.outputPath = path