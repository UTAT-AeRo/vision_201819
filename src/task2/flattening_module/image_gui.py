from tkinter import *
from PIL import Image, ImageTk
import cv2
from typing import Tuple, List, Dict
import numpy as np
import os


MOVE_SPEED = 10

class Image_GUI:
    """This class represents an the image processing application

    ==== Atributes ===
    master: the root of the gui
    canvas: the canvas containing the image being edited
    final_cv_img: The final image to be saved in the form of a np.array
    tk_image: the image currently being displayed on the screen.
    im_on_canvas: id of the image on the canvas.
    paths: A list of all images to be loaded
    _img_counter: Index of current image in paths being used.
    save_to: the path to which the images will be saved
    im_on_canvas: the id of the image on the canvas
    """
    master: Tk
    canvas: Canvas
    final_cv_img: np.ndarray
    tk_image: PhotoImage
    paths: List[str]
    _img_counter: int
    save_to: str
    _x_slider: Scrollbar
    _y_slider: Scrollbar

    def __init__(self, master: Tk, paths: List[str], save_to: str):
        """
        :param master: The root for this Tk window
        :param paths: Path of the first image to be loaded
        :param save_to: the path to which the images will be saved

        Precondition: Paths is not paths is not empty.
        """
        self.master = master
        self.paths = paths
        self._img_counter = 0
        self.save_to = save_to

        # Create image frame and canvas
        photo_frame = Frame(self.master, bd=2, relief=SUNKEN)
        photo_frame.grid_rowconfigure(0, weight=1)
        photo_frame.grid_columnconfigure(0, weight=1)

        self._x_slider = Scrollbar(photo_frame, orient=HORIZONTAL)
        self._y_slider = Scrollbar(photo_frame)

        self.canvas = Canvas(photo_frame, bd=0,
                             xscrollcommand=self._x_slider.set,
                             yscrollcommand=self._y_slider.set)

        self._x_slider.config(command=self.canvas.xview)
        self._y_slider.config(command=self.canvas.yview)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Place image

        self._x_slider.grid(row=1, column=0, sticky=E + W)
        self._y_slider.grid(row=0, column=1, sticky=N + S)
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
        photo_frame.pack(fill=BOTH, expand=1)

        self.final_cv_img = cv2.imread(paths[0])
        self.tk_image = self.cv2tk_image(self.final_cv_img)

        self.im_on_canvas = self.canvas.create_image(0, 0, image=self.tk_image,
                                                     anchor="nw",
                                                     tags='canvas_image')

    def _up(self):
        """called on up arrow press"""
        self._x_slider.set(0.5, 0.5)
    def _down(self):
        """called on down arrow press"""

    def _left(self):
        """called on left arrow press"""

    def _right(self):
        """called on left arrow press"""

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

    def to_canvas(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point in the window and converts it to canvas space."""
        return int(self.canvas.canvasx(point[0])),\
            int(self.canvas.canvasy(point[1]))

    def save_img_to_folder_with_extra(self, extra: str):
        """Save the final_cv_img to the save_to folder
        with <extra> added to its name"""
        if not os.path.exists(self.save_to):
            os.makedirs(self.save_to)

        name = os.path.basename(self.paths[self._img_counter])

        slit = name.split('.')

        if len(slit) > 1:
            sections = slit[:-1]
            extension = slit[-1]
            path = os.path.join(self.save_to, '.'.join(sections) + extra + '.' + extension)
            cv2.imwrite(path, self.final_cv_img)
        else:
            path = os.path.join(self.save_to, name + extra)
            cv2.imwrite(path, self.final_cv_img)

    def load_next_img_or_end(self):
        """Loads next image from paths if there are no more images to load
        it ends the main loop.
        """
        if self._img_counter < len(self.paths) - 1:
            self._img_counter += 1
            self.reload()
        else:
            self.master.destroy()

    def reload(self):
        """reload the current image from the path"""
        self.final_cv_img = cv2.imread(self.paths[self._img_counter])
        self.show_cv_image(self.final_cv_img)


if __name__ == '__main__':
    root = Tk()
    pro = Image_GUI(root, ['Sample_Images/Test_Images/2018-05-25_16-22-29-018.bmp'], 'test')
    #cv2.imwrite("result.png", pro.process_image_at('Sample_Images/solar.jpg'))
    root.mainloop()
