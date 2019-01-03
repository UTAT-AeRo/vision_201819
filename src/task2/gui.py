from tkinter import *
from PIL import Image, ImageTk
import cv2
from typing import Tuple, List
import nPTransform
import numpy as np
from enum import Enum
from shapely.geometry import Polygon


# https://stackoverflow.com/questions/5501192/how-to-display-picture-and-get-mouse-click-coordinate-on-it


# TODO fix pTransform aspect ratio issue
# TODO Allow multiple images
# TODO Resize the window automatically
# TODO Implement Circle
# TODO Implement Reset

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
    cv_image: The final image to be saved in the form of a np.array
    tk_image: the image currently being displayed on the screen.
    state_label: Displays the current state
    im_on_canvas: id of the image on the canvas.
    width: the length of the sortest side of the solar panel in milimeters
    """
    master: Tk
    canvas: Canvas
    state: State
    clicks: List[Tuple[int,int]]
    cv_image: np.ndarray
    tk_image: PhotoImage
    width: float

    def __init__(self, master, path:str, width:float=None):
        """Create a new image processor"""

        # TODO should be moved to a perpanel basis
        self.width = width

        self.master = master

        self.state = State.FLATTEN
        self.clicks = []

        # Toolbar
        toolbar = Frame(root)
        circle_button = Button(toolbar, text="Circle",
                               command=self.enter_circle_state)
        polly_button = Button(toolbar, text="Poly",
                              command=self.enter_polly_state)
        next_button = Button(toolbar, text="Next",
                             command=self.next_file)
        self.state_lable = Label(root, text=f'State: {self.state}')
        circle_button.pack(side=LEFT, padx=2, pady=2)
        polly_button.pack(side=LEFT, padx=2, pady=2)
        next_button.pack(side=LEFT, padx=2, pady=2)
        self.state_lable.pack()
        toolbar.pack(side=TOP, fill=X)

        # Create image frame and canvas
        photo_frame = Frame(self.master, bd=2, relief=SUNKEN)
        photo_frame.grid_rowconfigure(0, weight=1)
        photo_frame.grid_columnconfigure(0, weight=1)

        xscrollbar = Scrollbar(photo_frame, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=E + W)

        yscrollbar = Scrollbar(photo_frame)
        yscrollbar.grid(row=0, column=1, sticky=N + S)

        canvas = Canvas(photo_frame, bd=0, xscrollcommand=xscrollbar.set,
                        yscrollcommand=yscrollbar.set)
        self.canvas = canvas

        # Place image
        canvas.grid(row=0, column=0, sticky=N+S+E+W)

        xscrollbar.config(command=canvas.xview)
        yscrollbar.config(command=canvas.yview)

        photo_frame.pack(fill=BOTH, expand=1)

        self.cv_image = cv2.imread(path)
        self.tk_image = self.cv2tk_image(self.cv_image)

        self.im_on_canvas = canvas.create_image(0, 0, image=self.tk_image,
                                                anchor="nw",
                                                tags='canvas_image')

        canvas.bind('<Button-1>', self.left_mouse_down)
        canvas.bind('<B1-Motion>', self.left_mouse_move)
        canvas.bind('<ButtonRelease-1>', self.left_mouse_up)

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
        self.canvas.create_image(0, 0, image=self.tk_image,
                                 anchor="nw",
                                 tags='canvas_image')
        self.canvas.itemconfig(self.im_on_canvas, image=new_tkimage)
        self.tk_image = new_tkimage

    def enter_polly_state(self):
        self.state = State.POLLY
        self._reset()

    def enter_circle_state(self):
        self.state = State.CIRCLE
        self._reset()

    def enter_default_state(self):
        self.state = State.DEFAULT
        self._reset()

    def _reset(self):
        self.state_lable.config(text=f'State: {self.state}')
        self.clicks = []

    def next_file(self):
        pass

    def process_image_at(self, path: str):
        pass

    def left_mouse_down(self, event):
        """Called whenever the left mouse is clicked on the image canves"""
        x, y = int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y))
        if self.state == State.FLATTEN:
            # https://stackoverflow.com/questions/28615900/how-do-i-add-a-mouse-click-position-to-a-list-in-tkinter
            self.canvas.create_oval(x - 10, y - 10,
                                    x + 10, y + 10,
                                    fill='red', width=1, tags='corners')
            # add tuple (x, y) to existing list
            self.clicks.append((x, y))
            if len(self.clicks) >= 4:
                rect = np.asarray([np.asarray(np.float32(p)) for p in
                                   self.clicks])
                flat = nPTransform.four_point_transform(self.cv_image, rect)
                self.canvas.delete('corners')
                self.refresh_from_cv(flat)
                self.enter_default_state()
                self.cv_image = flat
        elif self.state == State.POLLY:
            pass
        elif self.state == State.CIRCLE:
            pass

    def left_mouse_move(self, event):
        x, y = int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y))

        if self.state == State.POLLY:
            temp = self.cv_image.copy()
            self._draw_line_from_last_point(x, y, temp)

    def left_mouse_up(self, event):
        x, y = int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y))

        if self.state == State.POLLY:
            self._draw_line_from_last_point(x, y, self.cv_image)
            self.clicks.append((x, y))

            if len(self.clicks) >= 4:
                self._draw_line_from_last_point(self.clicks[0][0],
                                                self.clicks[0][1],
                                                self.cv_image)
                self.refresh_from_cv(self.cv_image)

                quadrangle = Polygon(self.clicks)
                if self.width is None:
                    print(quadrangle.area, 'px^2')
                else:
                    print(quadrangle.area * self.px_size()**2, 'mm^2')

                self.enter_default_state()

    def _draw_line_from_last_point(self, x, y, cv_image):
        if len(self.clicks) >= 1:
            cv2.line(cv_image, self.clicks[-1], (x, y),
                     (255, 0, 0), 5)
            self.refresh_from_cv(cv_image)

    def px_size(self) -> float:
        """
        Precondition: Solar panel has already been flattened
        :return: returns the size of a pixel in cm if width is None returns 1
        """
        if self.width is not None:
            x, y, _ = self.cv_image.shape

            px_size = self.width/min(x, y)

            return px_size
        else:
            return 1


if __name__ == '__main__':
    root = Tk()
    pro = Image_Processor(root, 'Sample_Images/paper_2_in.jpg', 215.9)
    #cv2.imwrite("result.png", pro.process_image_at('Sample_Images/solar.jpg'))
    root.mainloop()


