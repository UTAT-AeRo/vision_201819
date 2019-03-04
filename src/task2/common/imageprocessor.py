from tkinter import *
import cv2
from typing import List, Dict, Tuple
import os
import sys
_script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.join(_script_path,
                os.path.join(os.pardir, os.pardir)),
                'common'))
from movableimage import MovableImage


class ImageProcessor:
    """This class represents an the image processing application

    ==== Properties ===
    movable_image: the moveable image updated by this class
    save_to: the path to which the images will be saved.
    curr_path: the path of the image currently loaded.
    """
    # === Private Attributes ===
    _movable_image: MovableImage  # the moveble image updated by this class
    _save_to: str  # the path to which the images will be saved
    _paths: List[str]  # A list of all images to be loaded
    _canvas: Canvas
    _master: Tk

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
        self._movable_image = MovableImage(master)
        self.movable_image.set_from_path(self.curr_path)
        self.movable_image.canvas.bind("<1>",
                                       lambda event: self.movable_image.focus_set)
        self.movable_image.focus_set()
        self._master.after(200, self.reload)

    @property
    def save_to(self):
        return self._save_to

    @property
    def curr_path(self):
        return self._paths[self.__img_counter]

    @property
    def movable_image(self):
        return self._movable_image

    def save_img_to_folder_with_extra(self, extra: str) -> str:
        """Save the cv_img on the movable_image to the save_to folder
        with <extra> added to its name

        :returns the path to which the file was saved
        """
        if not os.path.exists(self._save_to):
            os.makedirs(self._save_to)

        name = os.path.basename(self.curr_path)

        split = name.split('.')

        if len(split) > 1:
            sections = split[:-1]
            extension = split[-1]
            path = os.path.join(self._save_to, '.'.join(sections) + extra + '.'
                                + extension)
            cv2.imwrite(path, self.movable_image.cv_img)
        else:
            path = os.path.join(self._save_to, name + extra)
            cv2.imwrite(path, self.movable_image.cv_img)

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

    def reload(self):
        """reload image from current path"""
        self.movable_image.set_from_path(self.curr_path)
        self.movable_image.reset()
        self.movable_image.clear_dots()


class Panel:
    gps: Tuple[float, float]
    pixel: Tuple[int, int]
    dims: Tuple[int, int]
    path: str

    def __init__(self, gps, pixel, dims=None, path=None):
        self.gps = gps
        self.pixel = pixel
        self.dims = dims
        self.path = path

    def __eq__(self, other):
        return self.pixel == other.pixel \
               and self.gps == other.gps


class JsonFormatError(Exception):
    pass
