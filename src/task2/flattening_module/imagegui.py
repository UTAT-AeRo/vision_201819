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

class ImageGUI:
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
    _im_scale: float  # the scale of the image on the screen

    __photo_frame: Frame # the frame the canvas sits on.
    __im_on_canvas: int  # the id of the image on the canvas
    __tk_image: PhotoImage  # the image currently being displayed on the screen.
    __img_counter: int  # __img_counter: Index of current image in paths being
    # used.
    __x_slider: Scrollbar
    __y_slider: Scrollbar
    # === Representation Invariants ===
    # __tk_image must be _im_scale larger than _final_cv_image

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
        self._im_scale = 1.0

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

        self._final_cv_img = cv2.imread(self.curr_path)
        self.__tk_image = ImageTk.PhotoImage(Image.open(paths[0]))

        self.__im_on_canvas = self._canvas.create_image(0, 0,
                                                        image=self.__tk_image,
                                                        anchor="nw",
                                                        tags='canvas_image')

        # set focus to canvas when left you left click
        self._canvas.focus_set()
        self._canvas.bind("<1>", lambda event: self._canvas.focus_set())

        # set up arrow key scrolling
        self._canvas.bind("<Left>", lambda event: self.scroll((-MOVE_SPEED, 0)))
        self._canvas.bind("<Right>", lambda event: self.scroll((MOVE_SPEED, 0)))
        self._canvas.bind("<Up>", lambda event: self.scroll((0, -MOVE_SPEED)))
        self._canvas.bind("<Down>", lambda event: self.scroll((0, MOVE_SPEED)))

        # set up scroll bindings
        self._canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self._canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self._canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up

        self._set_up_image()
        self._master.after(200, self.reload)

    def _set_up_image(self):
        """Loads image from curr path and sets up tracking corners"""
        h = int(self.__photo_frame.winfo_height())
        w = int(self.__photo_frame.winfo_width())
        self._canvas.delete('corners')
        cBR = self.win_to_canvas((w, h))
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

    def scroll(self, delta: Tuple[int, int]):
        """Scroll canvas by delta"""
        self._canvas.xview_scroll(delta[0],
                                  "units")
        self._canvas.yview_scroll(delta[1],
                                  "units")
        self.refresh()

    @property
    def save_to(self):
        return self._save_to

    @property
    def curr_path(self):
        return self._paths[self.__img_counter]

    def wheel(self, event):
        # https://stackoverflow.com/questions/25787523/move-and-zoom-a-tkinter-canvas-with-mouse/48069295#48069295
        scale = 1.0
        if event.num == 5 or event.delta == -120:
            scale *= ZOOM_SPEED
            self._im_scale *= ZOOM_SPEED
        elif event.num == 4 or event.delta == 120:
            scale /= ZOOM_SPEED
            self._im_scale /= ZOOM_SPEED

        x = self._canvas.canvasx(event.x)
        y = self._canvas.canvasy(event.y)
        self._canvas.scale('all', x, y, scale, scale)
        self.refresh()

    def reload(self):
        """reload the current image from the path and reset the image scale"""
        self._final_cv_img = cv2.imread(self.curr_path)
        self.reset_scroll()
        self._set_up_image()
        self.refresh()

    def refresh(self):
        """ Updates the image on the canvas from the final cv_image. Should be
        called whenever the canvas is scaled or moved.
        """
        win_dims = (self.__photo_frame.winfo_width(),
                    self.__photo_frame.winfo_height())
        tl_fcv = self.win_to_final_cv((0, 0))
        br_fcv = self.win_to_final_cv(win_dims)

        h, w, _ = self._final_cv_img.shape

        tl_fcv = (min(max(CV_CROP_BUFFER, tl_fcv[0]), w - CV_CROP_BUFFER),
                  min(max(CV_CROP_BUFFER, tl_fcv[1]), h - CV_CROP_BUFFER))

        br_fcv = (max(min(w - CV_CROP_BUFFER, br_fcv[0]),
                      tl_fcv[0] + CV_CROP_BUFFER),
                  max(min(h - CV_CROP_BUFFER, br_fcv[1]),
                      tl_fcv[1] + CV_CROP_BUFFER))

        cropped_cv_img = self._final_cv_img[tl_fcv[1]: br_fcv[1], tl_fcv[0]: br_fcv[0]]

        b, g, r = cv2.split(cropped_cv_img)
        swiched_cv_img = cv2.merge((r, g, b))
        im = Image.fromarray(swiched_cv_img)

        tl_win = self.final_cv_to_win(tl_fcv)
        br_win = self.final_cv_to_win(br_fcv)

        new_width = min(max(br_win[0] - tl_win[0], 1),
                        int(win_dims[0] * IMG_OVERFILL))
        new_hight = min(max(br_win[1] - tl_win[1], 1),
                        int(win_dims[1] * IMG_OVERFILL))

        resized_im = im.resize((new_width, new_hight))

        new_tkimage = ImageTk.PhotoImage(resized_im)

        self._canvas.itemconfig(self.__im_on_canvas, image=new_tkimage)
        tl_canvas = self.final_cv_to_canvas(tl_fcv)
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

    def canvas_to_final_cv(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point on the canvas and converts it to the final_cv_image
        cords"""
        bounds = self._get_im_bounds()
        scale = self._get_scale()
        return (int((point[0] - bounds[0]) / scale[0]),
                int((point[1] - bounds[1]) / scale[1]))

    def final_cv_to_canvas(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point on the canvas and converts it to the final_cv_image
        cords"""
        bounds = self._get_im_bounds()
        scale = self._get_scale()
        canvas_point = (int((point[0] * scale[0]) + bounds[0]),
                        int((point[1] * scale[1]) + bounds[1]))
        return canvas_point

    def win_to_final_cv(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point in the window and converts it to final_cv_image space.
        """
        canvas_point = self.win_to_canvas(point)
        return self.canvas_to_final_cv(canvas_point)

    def final_cv_to_win(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Takes a point on the final_cv_image and converts a point on the window.
        """
        canvas_point = self.final_cv_to_canvas(point)
        return self.canvas_to_win(canvas_point)

    def _get_scale(self) -> Tuple[int, int]:
        bounds = self._get_im_bounds()
        h, w, _ = self._final_cv_img.shape
        x_scale = (bounds[2] - bounds[0])/w
        y_scale = (bounds[3] - bounds[1])/h
        return x_scale, y_scale

    def _get_im_bounds(self):
        """The bounding box of the image in canvas cords"""
        top_left = self._canvas.coords(self.__im_top_left)
        center = self._canvas.coords(self.__im_bot_right)
        return tuple(top_left[:2] + center[:2])

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
        """Reset scroll position"""
        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)
