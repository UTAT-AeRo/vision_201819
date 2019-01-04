from tkinter import *
from PIL import Image, ImageTk
import cv2
from typing import Tuple, List, Optional
import nPTransform
import numpy as np
from enum import Enum
from shapely.geometry import Polygon

# https://stackoverflow.com/questions/5501192/how-to-display-picture-and-get-mouse-click-coordinate-on-it


LINE_COLOR = (0, 0, 255)
LINE_WIDTH = 3
TEXT_SIZE = 1
TEXT_COLOR = (255, 0, 0)
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_THICKNESS = 3

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
        *** This class assumes the solar panels are rectangles ***

    ==== Atributes ===
    master: the root of the gui
    canvas: the canvas containing the image being edited
    state: the current state of the Image_Processor
    clicks: the clicks that have been made on the canvas
    final_cv_img: The final image to be saved in the form of a np.array
    tk_image: the image currently being displayed on the screen.
    state_label: Displays the current state
    im_on_canvas: id of the image on the canvas.
    dim: This is a tuple containing first the length of the smaller
        edge of the solar panel (width in mm) and then the larger edge
        (height in mm).
    """
    master: Tk
    canvas: Canvas
    state: State
    clicks: List[Tuple[int, int]]
    final_cv_img: np.ndarray
    tk_image: PhotoImage
    dim: Optional[Tuple[float, float]]

    def __init__(self, master: Tk, path: str, dim: Optional[Tuple[float, float]]):
        """
        :param master: The root for this Tk window
        :param path: The path for the file to be opened TODO Temp
        :param dim: The is a tuple containing first the length of the smaller
        edge of the solar panel (width) and then the larger edge (height).
        """

        # TODO should be moved to a per-panel basis

        self.dim = dim

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

        self.final_cv_img = cv2.imread(path)
        self.tk_image = self.cv2tk_image(self.final_cv_img)

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

    def show_cv_image(self, cv_img):
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
        """Called whenever the left mouse is clicked on the image canvas"""
        x, y = self.to_canvas((event.x, event.y))
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
                flat = nPTransform.four_points_correct_aspect(self.final_cv_img,
                                                              rect,
                                                              self.dim[0],
                                                              self.dim[1])
                self.canvas.delete('corners')
                self.show_cv_image(flat)
                self.enter_default_state()
                self.final_cv_img = flat

        elif self.state == State.POLLY:
            pass
        elif self.state == State.CIRCLE:
            pass

    def left_mouse_move(self, event):
        """Called whenever left mouse is moved while being held down
           on canvas.
        """
        x, y = self.to_canvas((event.x, event.y))

        if self.state == State.POLLY:
            temp = self.final_cv_img.copy()
            self._draw_line_from_last_click((x, y), temp)

        elif self.state == State.CIRCLE:
            temp = self.final_cv_img.copy()
            self._draw_circle_from_last_click((x, y), temp)
            self._draw_line_from_last_click((x, y), temp)

    def left_mouse_up(self, event):
        """Called when ever left mouse button is released"""
        x, y = self.to_canvas((event.x, event.y))

        if self.state == State.POLLY:
            self._draw_line_from_last_click((x, y), self.final_cv_img)
            self.clicks.append((x, y))

            if len(self.clicks) >= 4:
                self._draw_line_from_last_click(self.clicks[0],
                                                self.final_cv_img)
                self.show_cv_image(self.final_cv_img)

                print('Side 1:', self._dist(self.clicks[0], self.clicks[1])*self.px_size(), 'mm')
                print('Side 2:', self._dist(self.clicks[1], self.clicks[2])*self.px_size(), 'mm')
                print('Side 3:', self._dist(self.clicks[2], self.clicks[3])*self.px_size(), 'mm')
                print('Side 4:', self._dist(self.clicks[3], self.clicks[0])*self.px_size(), 'mm')

                quadrangle = Polygon(self.clicks)

                print('Area:', quadrangle.area * self.px_size()**2, 'mm^2')

                self.enter_default_state()
        elif self.state == State.CIRCLE:

            self._draw_line_from_last_click((x, y), self.final_cv_img)
            self._draw_circle_from_last_click((x, y), self.final_cv_img)
            self.clicks.append((x, y))

            if len(self.clicks) >= 2:

                radius = self._dist(self.clicks[0], self.clicks[1])

                print('Radius:', radius)

                print('Area:', np.pi * (radius ** 2))

                self.state = State.DEFAULT

    def to_canvas(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point in the window and converts it to canvas space."""
        return int(self.canvas.canvasx(point[0])),\
            int(self.canvas.canvasy(point[1]))

    def _draw_line_from_last_click(self, point, cv_image):
        if len(self.clicks) >= 1:

            cv2.line(cv_image, self.clicks[-1], point,
                     LINE_COLOR, LINE_WIDTH)

            text_org = ((point[0] + self.clicks[-1][0])//2,
                        (point[1] + self.clicks[-1][1])//2 + int(TEXT_SIZE))

            length = np.round(self._dist(self.clicks[-1], point)*self.px_size(), 2)

            cv2.putText(cv_image,
                        f'{length}mm'
                        , text_org, TEXT_FONT, TEXT_SIZE, TEXT_COLOR,
                        thickness=TEXT_THICKNESS)

            self.show_cv_image(cv_image)

    def _draw_circle_from_last_click(self, center, cv_image):
        if len(self.clicks) >= 1:
            cv2.circle(cv_image, center, int(self._dist(center, self.clicks[0]))
                       , LINE_COLOR, LINE_WIDTH)
            self.show_cv_image(cv_image)

    def px_size(self) -> float:
        """
        Precondition: Solar panel has already been flattened
        :return: returns the size of a pixel in mm
        """
        x, y, _ = self.final_cv_img.shape

        px_size = self.dim[0]/min(x, y)

        return px_size

    def _dist(self, point1:tuple, point2:tuple) -> int:
        """Returns the distance in px between two points on the canvas"""
        delta_x = abs(point1[0] - point2[0])
        delta_y = abs(point1[1] - point2[1])
        return np.sqrt(delta_x**2 + delta_y**2)


if __name__ == '__main__':
    root = Tk()
    pro = Image_Processor(root, 'Sample_Images/hd_solar.jpg', (215.9, 279.4))
    #cv2.imwrite("result.png", pro.process_image_at('Sample_Images/solar.jpg'))
    root.mainloop()


