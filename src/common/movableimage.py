from tkinter import *
from PIL import Image, ImageTk
import cv2
from typing import Tuple, List, Dict
import numpy as np
import os

MOVE_SPEED = 1
ZOOM_SPEED = 1.1
CV_CROP_BUFFER = 5
IMG_OVERFILL = 2
DOT_TAG = 'dot_tag'

class MovableImage:
    """This holds a canvas with an image that can be zoomed and moved.

    ==== Properties ===
    canvas: the canvas that the images is on should work like any other canvas
    do not call remove all.
    cv_img: the internal cv image.
    fit_to_frame: boolean fit to the frame (default false). This should only be
    set to two after the main loop runs.
    """
    fit_to_frame: bool
    # === Private Attributes ===
    _master: Tk  # the root of the gui
    _canvas: Canvas  # the canvas containing the image being edited
    _cv_img: np.ndarray  # the internal cv image.

    __photo_frame: Frame # the frame the canvas sits on.
    __im_on_canvas: int  # the id of the image on the canvas
    __tk_image: PhotoImage  # the image currently being displayed on the screen.
    __img_counter: int  # __img_counter: Index of current image in paths being
    # used.
    __x_slider: Scrollbar
    __y_slider: Scrollbar
    _scroll_speed: float  # how fast to move the scroll bars when the arrow keys are pressed
    _zoom_speed: float  # how much bigger to make the image for every click of the scroll wheel
    __win_dims: Tuple[float, float]

    def __init__(self, master: Tk, zoom_speed: float=ZOOM_SPEED, move_speed: float=MOVE_SPEED):
        """
        :param master: The root for this Tk window

        Precondition: Paths is not paths is not empty.
        """
        self.fit_to_frame = False
        self._master = master
        self._scroll_speed = min(move_speed, 0)
        self._zoom_speed = min(zoom_speed, 1)

        # Create image frame and canvas
        self.__photo_frame = Frame(self._master, bd=2, relief=SUNKEN)
        self.__photo_frame.grid_rowconfigure(0, weight=1)
        self.__photo_frame.grid_columnconfigure(0, weight=1)

        self.__x_slider = Scrollbar(self.__photo_frame, orient=HORIZONTAL)
        self.__y_slider = Scrollbar(self.__photo_frame)

        self._canvas = Canvas(self.__photo_frame, bd=0,
                              xscrollcommand=self.__x_slider.set,
                              yscrollcommand=self.__y_slider.set)

        self.__x_slider.config(command=self._canvas.xview)
        self.__y_slider.config(command=self._canvas.yview)
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

        # Place image
        self.__x_slider.grid(row=1, column=0, sticky=E + W)
        self.__y_slider.grid(row=0, column=1, sticky=N + S)
        self._canvas.grid(row=0, column=0, sticky=N + S + E + W)
        self.__photo_frame.pack(fill=BOTH, expand=1)

        # set up arrow key scrolling
        self._canvas.bind("<Left>", lambda event: self.scroll((-MOVE_SPEED, 0)))
        self._canvas.bind("<Right>", lambda event: self.scroll((MOVE_SPEED, 0)))
        self._canvas.bind("<Up>", lambda event: self.scroll((0, -MOVE_SPEED)))
        self._canvas.bind("<Down>", lambda event: self.scroll((0, MOVE_SPEED)))

        # set up scroll bindings
        self._canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self._canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self._canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up

        # set up refresh on resize
        self._canvas.bind('<Configure>', lambda event: self.refresh)

        self._cv_img = np.zeros((100, 100, 3), np.uint8)
        self._set_up_image()
        self.cv_img = self._cv_img

    def focus_set(self):
        """Set the focuse on the canvas when called must be called before you
        can interact with canvas"""
        self._canvas.focus_set()

    def _set_up_image(self):
        """Loads image from curr path and sets up tracking corners"""
        self._canvas.delete('corners')
        if self.fit_to_frame:
            dims = (self.__photo_frame.winfo_height(),
                    self.__photo_frame.winfo_width())
        else:
            h, w, _ = self.cv_img.shape
            dims = (h, w)

        cBR = self.win_to_canvas(dims)
        self.__im_bot_right = self._canvas.create_oval((cBR[0],
                                                        cBR[0],
                                                        cBR[1],
                                                        cBR[1]),
                                                       tags='corners',
                                                       fill='purple',
                                                       state=HIDDEN)
        cTL = self.win_to_canvas((0, 0))
        self.__im_top_left = self._canvas.create_oval((cTL[0],
                                                       cTL[0],
                                                       cTL[1],
                                                       cTL[1]),
                                                      tags='corners',
                                                      fill='green',
                                                      state=HIDDEN)

    @property
    def canvas(self):
        return self._canvas

    @property
    def cv_img(self):
        return self._cv_img

    @cv_img.setter
    def cv_img(self, cv_img: np.ndarray):
        """Sets the current image from an np.ndarray"""
        self._cv_img = cv_img

        self.__tk_image = ImageTk.PhotoImage(Image.fromarray(cv_img))

        self.__im_on_canvas = self._canvas.create_image(0, 0,
                                                        image=self.__tk_image,
                                                        anchor="nw",
                                                        tags='canvas_image')
        self.refresh()

    def scroll(self, delta: Tuple[int, int]):
        """Scroll canvas by delta"""
        self._canvas.xview_scroll(delta[0],
                                  "units")
        self._canvas.yview_scroll(delta[1],
                                  "units")
        self.refresh()

    def wheel(self, event):
        # https://stackoverflow.com/questions/25787523/move-and-zoom-a-tkinter-canvas-with-mouse/48069295#48069295
        scale = 1.0
        if event.num == 5 or event.delta == -120:
            scale *= ZOOM_SPEED
        elif event.num == 4 or event.delta == 120:
            scale /= ZOOM_SPEED

        x = self._canvas.canvasx(event.x)
        y = self._canvas.canvasy(event.y)
        self._canvas.scale('all', x, y, scale, scale)
        self.refresh()

    def clear_dots(self):
        """removes all dots made with make dot"""
        self.canvas.delete(DOT_TAG)

    def reset(self):
        """reset the image scale and position"""
        self.reset_scroll()
        self._set_up_image()
        self.refresh()

    def set_from_path(self, path: str):
        """Sets the current image from a path if image is not found or fails to
        load will raise a FileNotFoundError"""
        temp = cv2.imread(path)
        if temp is None or temp.size == 0:
            raise FileNotFoundError("open cv2 failed to load this file")
        self.cv_img = temp

    def refresh(self):
        """ Updates the image on the canvas from the final cv_image. Should be
        called whenever the canvas is scaled or moved.
        """
        win_dims = (self.__photo_frame.winfo_width(),
                    self.__photo_frame.winfo_height())
        tl_fcv = self.win_to_cv((0, 0))
        br_fcv = self.win_to_cv(win_dims)

        h, w, _ = self._cv_img.shape

        tl_fcv = (min(max(CV_CROP_BUFFER, tl_fcv[0]), w - CV_CROP_BUFFER),
                  min(max(CV_CROP_BUFFER, tl_fcv[1]), h - CV_CROP_BUFFER))

        br_fcv = (max(min(w - CV_CROP_BUFFER, br_fcv[0]),
                      tl_fcv[0] + CV_CROP_BUFFER),
                  max(min(h - CV_CROP_BUFFER, br_fcv[1]),
                      tl_fcv[1] + CV_CROP_BUFFER))

        cropped_cv_img = self._cv_img[tl_fcv[1]: br_fcv[1], tl_fcv[0]: br_fcv[0]]

        b, g, r = cv2.split(cropped_cv_img)
        swiched_cv_img = cv2.merge((r, g, b))
        im = Image.fromarray(swiched_cv_img)

        tl_win = self.final_cv_to_win(tl_fcv)
        br_win = self.final_cv_to_win(br_fcv)

        new_width = min(max(br_win[0] - tl_win[0], 1),
                        int(win_dims[0]))
        new_hight = min(max(br_win[1] - tl_win[1], 1),
                        int(win_dims[1]))

        resized_im = im.resize((new_width, new_hight))

        new_tkimage = ImageTk.PhotoImage(resized_im)

        self._canvas.itemconfig(self.__im_on_canvas, image=new_tkimage)
        tl_canvas = self.cv_to_canvas(tl_fcv)
        self._canvas.coords(self.__im_on_canvas, list(tl_canvas))
        self.__tk_image = new_tkimage

    def win_to_canvas(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point in the window and converts it to canvas space."""
        return int(self._canvas.canvasx(point[0])),\
            int(self._canvas.canvasy(point[1]))

    def canvas_to_win(self, point: Tuple[float, float]):
        """Takes point on the canvas and returns screen position"""
        x0 = self._canvas.canvasx(0)
        y0 = self._canvas.canvasy(0)

        return int(point[0] - x0), int(point[1] - y0)

    def canvas_to_cv(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point on the canvas and converts it to the cv_img
        cords"""
        bounds = self._get_im_bounds()
        scale = self._get_scale()
        return (int((point[0] - bounds[0]) / scale[0]),
                int((point[1] - bounds[1]) / scale[1]))

    def cv_to_canvas(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point on the canvas and converts it to the cv_img
        cords"""
        bounds = self._get_im_bounds()
        scale = self._get_scale()
        canvas_point = (int((point[0] * scale[0]) + bounds[0]),
                        int((point[1] * scale[1]) + bounds[1]))
        return canvas_point

    def win_to_cv(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point in the window and converts it to cv_img space.
        """
        canvas_point = self.win_to_canvas(point)
        return self.canvas_to_cv(canvas_point)

    def final_cv_to_win(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point on the cv_img and converts a point on the window.
        """
        canvas_point = self.cv_to_canvas(point)
        return self.canvas_to_win(canvas_point)

    def _get_scale(self) -> Tuple[int, int]:
        bounds = self._get_im_bounds()
        h, w, _ = self._cv_img.shape
        x_scale = (bounds[2] - bounds[0])/w
        y_scale = (bounds[3] - bounds[1])/h
        return x_scale, y_scale

    def _get_im_bounds(self):
        """The bounding box of the image in canvas cords"""
        top_left = self._canvas.coords(self.__im_top_left)
        center = self._canvas.coords(self.__im_bot_right)
        return tuple(top_left[:2] + center[:2])

    def reset_scroll(self):
        """Reset scroll position"""
        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)

    def make_dot(self, colour: str, pos: Tuple[int, int], dot_size: int):
        """
        :param colour: the colour of the fill must a valid tkinter color
        :param pos: the x, y cords to place the dot on the canvas
        :param dot_size: the size of the dot in px's
        """
        self.canvas.create_oval(pos[0] - dot_size, pos[1] - dot_size,
                                pos[0] + dot_size, pos[1] + dot_size,
                                fill=colour, width=1, tags=DOT_TAG)


if __name__ == '__main__':
    tk = Tk()
    mimg = MovableImage(tk)
    mimg.set_from_path("../Sample_Images/solar.jpg")
    tk.mainloop()
