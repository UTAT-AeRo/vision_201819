from tkinter import *
from PIL import Image, ImageTk
import cv2
from typing import Tuple, List, Dict
import numpy as np
import os


MOVE_SPEED = 10


class Image_GUI:
    """This class represents an the image processing application

    ==== Properties ===
    save_to: the path to which the images will be saved.
    curr_path: the path of the image currently loaded.
    """
    # === Private Attributes ===
    _save_to: str  # the path to which the images will be saved
    _master: Tk  # the root of the gui
    _canvas: Canvas  # the canvas containing the image being edited
    _final_cv_img: np.ndarray  # The final image to be saved in the form of
    # a np.array
    _paths: List[str]  # A list of all images to be loaded
    __im_on_canvas: int  # the id of the image on the canvas

    __tk_image: PhotoImage  # the image currently being displayed on the screen.
    __img_counter: int  # __img_counter: Index of current image in paths being
    # used.
    __x_slider: Scrollbar
    __y_slider: Scrollbar

    def __init__(self, master: Tk, paths: List[str], save_to: str):
        """
        :param master: The root for this Tk window
        :param paths: Path of the first image to be loaded
        :param save_to: the path to which the images will be saved

        Precondition: Paths is not paths is not empty.
        """
        self._master = master
        self._paths = paths
        self.__img_counter = 0
        self._save_to = save_to

        # Create image frame and canvas
        photo_frame = Frame(self._master, bd=2, relief=SUNKEN)
        photo_frame.grid_rowconfigure(0, weight=1)
        photo_frame.grid_columnconfigure(0, weight=1)

        self.__x_slider = Scrollbar(photo_frame, orient=HORIZONTAL)
        self.__y_slider = Scrollbar(photo_frame)

        self._canvas = Canvas(photo_frame, bd=0,
                              xscrollcommand=self.__x_slider.set,
                              yscrollcommand=self.__y_slider.set)

        self.__x_slider.config(command=self._canvas.xview)
        self.__y_slider.config(command=self._canvas.yview)
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

        # Place image

        self.__x_slider.grid(row=1, column=0, sticky=E + W)
        self.__y_slider.grid(row=0, column=1, sticky=N + S)
        self._canvas.grid(row=0, column=0, sticky=N + S + E + W)
        photo_frame.pack(fill=BOTH, expand=1)

        self._final_cv_img = cv2.imread(paths[0])
        self.__tk_image = self.cv2tk_image(self._final_cv_img)

        self.__im_on_canvas = self._canvas.create_image(0, 0, image=self.__tk_image,
                                                        anchor="nw",
                                                        tags='canvas_image')
        self.reload()



    @property
    def save_to(self):
        return self._save_to

    @property
    def curr_path(self):
        return self._paths[self.__img_counter]

    def reload(self):
        """reload the current image from the path"""
        self._final_cv_img = cv2.imread(self.curr_path)
        self.show_cv_image(self._final_cv_img)

    def _up(self):
        """called on up arrow press"""
        self.__x_slider.set(0.5, 0.5)
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
        self._canvas.itemconfig(self.__im_on_canvas, image=new_tkimage)
        self.__tk_image = new_tkimage

    def to_canvas(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point in the window and converts it to canvas space."""
        return int(self._canvas.canvasx(point[0])),\
            int(self._canvas.canvasy(point[1]))

    def save_img_to_folder_with_extra(self, extra: str) -> str:
        """Save the final_cv_img to the save_to folder
        with <extra> added to its name

        :returns the path to which the file was saved
        """
        if not os.path.exists(self._save_to):
            os.makedirs(self._save_to)

        name = os.path.basename(self.curr_path)

        slit = name.split('.')

        if len(slit) > 1:
            sections = slit[:-1]
            extension = slit[-1]
            path = os.path.join(self._save_to, '.'.join(sections) + extra + '.'
                                + extension)
            cv2.imwrite(path, self._final_cv_img)
        else:
            path = os.path.join(self._save_to, name + extra)
            cv2.imwrite(path, self._final_cv_img)

        return path

    def load_next_img_or_end(self):
        """Loads next image from paths if there are no more images to load
        it ends the main loop.
        """
        if self.__img_counter < len(self._paths) - 1:
            self.__img_counter += 1
            self.reload()
        else:
            self._master.destroy()

    def reset_scroll(self):
        self._canvas.config(xscrollcommand=self.__x_slider.set)
        self._canvas.config(yscrollcommand=self.__y_slider.set)
