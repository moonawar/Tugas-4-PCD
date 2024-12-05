from tkinter import Label

def create_space(parent, sizex=0, sizey=0, bg="white", side="top"):
    space = Label(parent, height=sizey, width=sizex, bg=bg, padx=0, pady=0)
    space.pack(side=side)
    return space