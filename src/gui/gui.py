from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import ctypes
import time
import threading

from gui.color import *
from gui.utils import *
from model.PretrainedModel import classify_image as classify_image_pretrained
from model.ConventionalModel import classify_image as classify_image_improc

PLACEHOLDER_IMAGE_PIL = Image.open("gui/assets/placeholder.png")
input_image_path = ""
is_running = False

# String Vars
status_text = None
message_text = None

# PATH CONSTANT
MODEL_PATH = "../model/conventional_model.joblib"

def choose_file():
    filepath = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")],
    )

    return filepath

def calc_image_size(image, max_size):
    width, height = image.size

    if width > height:
        new_width = max_size
        new_height = int(max_size * height / width)
    else:
        new_width = int(max_size * width / height)
        new_height = max_size

    return new_width, new_height

def fit_image(image, max_size):
    width, height = calc_image_size(image, max_size)
    image = image.resize((width, height), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (max_size, max_size), COLOR_SECONDARY)

    x_offset = (max_size - width) // 2
    y_offset = (max_size - height) // 2
    canvas.paste(image, (x_offset, y_offset))

    image = ImageTk.PhotoImage(canvas)
    return image

def extract_filename(filepath):
    return filepath.split("/")[-1]

def run_algorithm_sync():
    global input_image_path

    if not input_image_path:
        messagebox.showerror("Error", "Please select an image first!")
        return

    pretrained_class = classify_image_pretrained(input_image_path)
    improc_class = classify_image_improc(input_image_path, MODEL_PATH)
    
    return pretrained_class, improc_class

def run_algorithm_async(callback):
    def task():
        output_pretrained, output_improc = run_algorithm_sync()
        callback(output_pretrained, output_improc)

    thread = threading.Thread(target=task)
    thread.start()

def add_text_with_bg(canvas, text, font, text_color, bg_color):
    text_id = canvas.create_text(5, 355, text=text, fill=text_color, font=font, anchor="sw")
    bbox = canvas.bbox(text_id)

    if bbox:
        x1, y1, x2, y2 = bbox
        padding = 5
        canvas.create_rectangle(x1-padding, y1-padding, x2+padding, y2+padding, fill=bg_color, width=0)
        canvas.tag_raise(text_id)
        

class AppWindow(Tk):
    def __init__(self):
        super().__init__()

        # Corrects DPI scaling on Windows (Removes blurry visuals)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        self.title("Vehicle Recognition App")
        self.geometry("1280x720")
        self.resizable(False, False)

        self.init_vars()
        self.build()

    def init_vars(self):
        global status_text, message_text
        status_text = StringVar(value="Status: Idle")
        message_text = StringVar(value="Waiting for the application to be run!")

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

    def clear_output(self):
        placeholder_image = PLACEHOLDER_IMAGE_PIL.resize((360, 360), Image.Resampling.LANCZOS)
        placeholder_image = ImageTk.PhotoImage(placeholder_image)

        output_pretrained_image = Result.output_images["pretrained"]
        output_pretrained_image.delete("all")
        output_pretrained_image.create_image(180, 180, image=placeholder_image)
        output_pretrained_image.image = placeholder_image

        output_improc_image = Result.output_images["improc"]
        output_improc_image.delete("all")
        output_improc_image.create_image(180, 180, image=placeholder_image)
        output_improc_image.image = placeholder_image

        Result.class_labels["pretrained"].config(text="Class: None")
        Result.class_labels["improc"].config(text="Class: None")

    def reset_status(self):
        global status_text, message_text
        status_text.set("Status: Idle")
        message_text.set("Waiting for the application to be run!")


    def choose_input_file(self):
        global input_image_path
        input_image_path = choose_file()

        if input_image_path:
            image = Image.open(input_image_path)
            image = fit_image(image, 300)

            self.input_image.config(image=image)
            self.input_image.image = image

            self.selected_file_text.set(extract_filename(input_image_path))
            self.clear_output()
            self.reset_status()

            self.output_pretrained = None
            self.output_improc = None

    def run_algorithm(self):
        global status_text, message_text
        status_text.set("Status: Running")
        message_text.set("Running the algorithm...")  

        self.choose_file_button.config(state="disabled")
        self.run_button.config(state="disabled")

        def callback(pretrained_class, improc_class):
            status_text.set("Status: Done")
            message_text.set("The application has finished running!")

            base_image = Image.open(input_image_path)
            base_image = fit_image(base_image, 360)

            output_pretrained_image = Result.output_images["pretrained"]
            output_pretrained_image.delete("all")
            output_pretrained_image.create_image(180, 180, image=base_image)
            output_pretrained_image.image = base_image
            add_text_with_bg(
                output_pretrained_image, f"Class: {pretrained_class}", ("Poppins", 12, "bold"), 
                COLOR_PRIMARY_DARK, COLOR_ACCENT
            )

            Result.class_labels["pretrained"].config(text=f"Class (Pretrained): {pretrained_class}")

            output_improc_image = Result.output_images["improc"]
            output_improc_image.delete("all")
            output_improc_image.create_image(180, 180, image=base_image)
            output_improc_image.image = base_image
            add_text_with_bg(
                output_improc_image, f"Class (Image Processing): {improc_class}", ("Poppins", 12, "bold"), 
                COLOR_PRIMARY_DARK, COLOR_ACCENT
            )

            Result.class_labels["improc"].config(text=f"Class: {improc_class}")

            self.choose_file_button.config(state="normal")
            self.run_button.config(state="normal")

        run_algorithm_async(callback)

    def build(self):
        create_space(self, bg=COLOR_PRIMARY)

        label = Label(self, text="Input Image", font=("Poppins", 14, "bold"), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY)
        label.pack(side="top", anchor="w", padx=24, pady=4)

        button_image = PhotoImage(file="gui/assets/btn-choose-file.png")
        self.choose_file_button = Button(self, image=button_image, fg=COLOR_PRIMARY, bg=COLOR_PRIMARY, bd=0, command=self.choose_input_file)
        self.choose_file_button.image = button_image
        self.choose_file_button.pack(side="top", anchor="w", padx=24, pady=4)

        self.selected_file_text = StringVar(value="No file selected")
        selected_label = Label(self, textvariable=self.selected_file_text, font=("Poppins", 12), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY)
        selected_label.pack(side="top", anchor="w", padx=24, pady=4)

        placeholder_image = PLACEHOLDER_IMAGE_PIL.resize((300, 300), Image.Resampling.LANCZOS)
        placeholder_image = ImageTk.PhotoImage(placeholder_image)
        self.input_image = Label(self, image=placeholder_image, bg=COLOR_PRIMARY)
        self.input_image.image = placeholder_image
        self.input_image.pack(side="top", anchor="center", padx=24, pady=4)

        create_space(self, bg=COLOR_PRIMARY)

        button_image = PhotoImage(file="gui/assets/btn-run.png")
        self.run_button = Button(self, image=button_image, bg=COLOR_PRIMARY, fg=COLOR_SECONDARY, bd=0, command=self.run_algorithm)
        self.run_button.image = button_image
        self.run_button.pack(side="top", anchor="center", padx=24, pady=4)

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

        result_pretrained_frame = Result(self, "pretrained")
        result_pretrained_frame.set_label("Result (Pretrained Model)")
        result_pretrained_frame.set_output_path("../output/")
        result_pretrained_frame.grid(row=0, column=0, sticky="nswe")

        result_improc_frame = Result(self, "improc")
        result_improc_frame.set_label("Result (Image Processing)")
        result_improc_frame.set_output_path("../output/")
        result_improc_frame.grid(row=0, column=1, sticky="nswe")

        bottom_frame = Frame(self)
        bottom_frame.configure(bg=COLOR_PRIMARY_DARK)
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nswe")

        create_space(bottom_frame, bg=COLOR_PRIMARY_DARK, sizey=2)

        global status_text, message_text

        status = Label(bottom_frame, textvariable=status_text, font=("Poppins", 12, "bold"), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY_DARK)
        status.pack(side="top", padx=(56, 0), anchor="w")

        message = Label(bottom_frame, textvariable=message_text, font=("Poppins", 12), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY_DARK)
        message.pack(side="top", padx=(56, 0), anchor="w")
        pass

class Result(Frame):
    output_images = {}
    class_labels = {}

    def __init__(self, master, method):
        super().__init__(master)
        self.configure(bg=COLOR_PRIMARY_DARK)

        self.method = method
        self.build()

    def build(self):
        create_space(self, bg=COLOR_PRIMARY_DARK)

        self.outputPath = ""
        self.label_text = StringVar(value="Result")
        self.label = Label(self, textvariable=self.label_text, font=("Poppins", 14, "bold"), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY_DARK)
        self.label.pack(side="top", anchor="w", padx=(56, 0), pady=4)

        placeholder_image = PLACEHOLDER_IMAGE_PIL.resize((360, 360), Image.Resampling.LANCZOS)
        placeholder_image = ImageTk.PhotoImage(placeholder_image)

        output_image = Canvas(self, width=360, height=360, bg=COLOR_PRIMARY_DARK, highlightthickness=0)
        output_image.create_image(180, 180, image=placeholder_image)
        output_image.image = placeholder_image
        output_image.pack(side="top", anchor="center", padx=24, pady=4)

        Result.output_images[self.method] = output_image

        label = Label(self, text="Class: None", font=("Poppins", 12, "bold"), fg=COLOR_SECONDARY, bg=COLOR_PRIMARY_DARK)
        # label.pack(side="top", anchor="w", padx=(56, 0), pady=4)

        Result.class_labels[self.method] = label

    def set_label(self, text):
        self.label_text.set(text)

    def set_output_path(self, path):
        self.outputPath = path
