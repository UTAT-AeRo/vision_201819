from tkinter import *
from PIL import Image, ImageTk
import cv2
from typing import Tuple, List
import nPTransform
import numpy as np

from enum import Enum

# https://stackoverflow.com/questions/5501192/how-to-display-picture-and-get-mouse-click-coordinate-on-it

# TODO Allow multiple images
# TODO Overlay an X for the selected regions
# TODO Resize the window automatically
# TODO Use CV instead of PIL since it's more efficient.


class Need4PointsError(Exception):
    pass

class State(Enum):
    DEFAULT = 0
    POLLY = 1
    CIRCLE = 2
    FLATTEN = 3

class Image_Processor:
    """This class represents an the image processing application

    ==== Atributes ===
    master: the root of the gui
    canvas: the canvas containing the image being edited
    state: the current state of the Image_Processor
    clicks: the clicks that have been made on the canvas
    cv_image: the image being displayed in format compatible with open_cv
    tk_image: the image currently being displayed on the screen.
    """
    master: Tk
    canvas: Canvas
    state: State
    clicks: List[Tuple[int,int]]
    cv_image: np.ndarray
    tk_image: PhotoImage

    def __init__(self, master, path):
        """Create a new image processor"""

        self.master = master

        self.state = State.FLATTEN
        self.clicks = []

        # Toolbar
        toolbar = Frame(root)
        circle_button = Button(toolbar, text="Circle",
                               command=self.enter_circle_state)
        polly_button = Button(toolbar, text="Poly",
                              command=self.enter_poly_state)
        next_button = Button(toolbar, text="Next",
                             command=self.next_file)
        circle_button.pack(side=LEFT, padx=2, pady=2)
        polly_button.pack(side=LEFT, padx=2, pady=2)
        next_button.pack(side=LEFT, padx=2, pady=2)
        toolbar.pack(side=TOP, fill=X)

        # Create image frame and canvas
        photo_frame = Frame(self.master, bd=2, relief=SUNKEN)
        photo_frame.grid_rowconfigure(0, weight=1)
        photo_frame.grid_columnconfigure(0, weight=1)
        canvas = Canvas(photo_frame, bd=0)
        self.canvas = canvas

        # Place image
        canvas.grid(row=0, column=0, sticky=N+S+E+W)
        photo_frame.pack(fill=BOTH, expand=1)

        self.cv_image = cv2.imread(path)
        self.tk_image = self.cv2tk_image(self.cv_image)

        self.im_on_canvas = canvas.create_image(0, 0, image=self.tk_image,
                                                anchor="nw",
                                                tags='canvas_image')

        canvas.config(scrollregion=canvas.bbox(ALL))

        canvas.bind('<Button-1>', self.left_mouse_click)

        # Set the size of the window
        #w, h = photo.size()
        #dim = str(w) + "x" + str(h)
        #self.master.geometry(dim)

    def cv2tk_image(self, cv_img) -> PhotoImage:
        b, g, r = cv2.split(cv_img)
        cv_img = cv2.merge((r, g, b))
        im = Image.fromarray(cv_img)
        return ImageTk.PhotoImage(image=im)


    def refresh_from_cv(self, cv_img):
        """Takes a image in array fromat and sets the image on the canvas
        to it"""
        new_tkimage = self.cv2tk_image(cv_img)
        self.canvas.itemconfig(self.im_on_canvas, image=new_tkimage)
        self.tk_image = new_tkimage

    def enter_poly_state(self):
        pass

    def enter_circle_state(self):
        pass

    def enter_default_state(self):
        pass

    def next_file(self):
        pass

    def process_image_at(self, path: str):
        pass

    def left_mouse_click(self, event):
        """Called whenever the left mouse is clicked on the image canves"""
        if self.state == State.FLATTEN:
            # https://stackoverflow.com/questions/28615900/how-do-i-add-a-mouse-click-position-to-a-list-in-tkinter
            self.canvas.create_oval(event.x - 10, event.y - 10,
                                    event.x + 10, event.y + 10,
                                    fill='red', width=1, tags='corners')
            # add tuple (x, y) to existing list
            self.clicks.append((event.x, event.y,))
            if len(self.clicks) >= 4:
                rect = np.asarray([np.asarray(np.float32(p)) for p in
                                   self.clicks])
                flat = nPTransform.four_point_transform(self.cv_image, rect)
                self.canvas.delete('corners')
                self.refresh_from_cv(flat)
                self.enter_default_state()
        elif self.state == State.POLLY:
            pass
        elif self.state == State.CIRCLE:
            pass


if __name__ == '__main__':
    root = Tk()
    pro = Image_Processor(root, 'Sample_Images/solar.jpg')
    #cv2.imwrite("result.png", pro.process_image_at('Sample_Images/solar.jpg'))
    root.mainloop()


