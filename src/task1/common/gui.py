from tkinter import Label, Frame, Button, Entry, StringVar
import os
from PIL import Image, ImageTk


class Viewer:
    """
    Base GUI to scroll through files
    """
    def __init__(self, window, file_list, img_x=500, img_y=500):
        self.top = window       # top window
        self.files = file_list   # list of files
        self.index = 0          # index of file list
        self.img_x = img_x      # width of image/image viewer
        self.img_y = img_y      # height of image/image viewer
        self.x_scale = None  # set when ge
        self.y_scale = None  # set when get image is called
        self.files_reverse = {os.path.basename(file_name): i for (i, file_name) in enumerate(file_list)}

        assert len(file_list) > 0
        filename = file_list[0]
        if not os.path.exists(filename):
            self.top.quit()

        # Set top searchbar
        self.title_fr = Frame(self.top)
        self.title_fr.place(x=15,y=15)
        self.evar = StringVar()
        self.evar.set(os.path.basename(self.files[self.index]))
        entry = Entry(self.title_fr, textvariable=self.evar)
        entry.grid(row=0, column=1, sticky="e", pady=4)
        entry.bind('<Return>', self.next_frame_by_name)

        # Set image + image label
        self.tkimage = ImageTk.PhotoImage(self.load_image(filename))
        self.lbl = Label(self.top, image=self.tkimage, height=self.img_y, width=self.img_x)
        self.lbl.place(x=15,y=40)

        # the button frame
        self.button_fr = Frame(self.top)
        self.button_fr.place(x=15,y=self.img_y+55)
        self.button_fr.place(x=1)
        back_button = Button(self.button_fr, text="back", command=lambda: self.next_frame(self.index-1))
        back_button.grid(row=0, column=0, sticky="w", padx=4, pady=4)
        next_button = Button(self.button_fr, text="next", command=lambda: self.next_frame(self.index+1))
        next_button.grid(row=0, column=6, sticky="e", padx=4, pady=4)

    # Open an image and resets ratios
    def load_image(self, filename):
        im = Image.open(filename)
        width, height = im.size
        self.x_scale = width / self.img_x
        self.y_scale = height / self.img_y
        im = im.resize((self.img_x, self.img_y))
        return im

    # Go to image at index new_index
    def next_frame(self, new_index):
        self.index = new_index % len(self.files)
        filename = self.files[self.index]
        basename = os.path.basename(filename)
        im = self.load_image(filename)
        self.evar.set(basename)
        self.tkimage.paste(im)

    # Go to frame with name written in search bar
    def next_frame_by_name(self, event=None):
        name = self.evar.get()
        if name in self.files_reverse:
            self.next_frame(self.files_reverse[name])

    @property
    def file(self):
        return self.files[self.index]
