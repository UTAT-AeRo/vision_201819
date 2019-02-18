from tkinter import *
import cv2
from typing import Tuple, List, Optional, Dict
import numpy as np
from enum import Enum
from shapely.geometry import Polygon
from imageprocessor import Panel, ImageProcessor

# https://stackoverflow.com/questions/5501192/how-to-display-picture-and-get-mouse-click-coordinate-on-it

LINE_COLOR = (0, 0, 255)
LINE_WIDTH = 2
TEXT_SIZE = 0.5
TEXT_COLOR = (0, 125, 200)
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_THICKNESS = 2
MARK_TAG = "mark"
CANVAS_LINE_COLOR = 'red'
CANVAS_LINE_THICKNESS = 1
CANVAS_DASH_PATTERN = (5,)


class State(Enum):
    DEFAULT = 0
    POLLY = 1
    CIRCLE = 2


class DamageSelector(ImageProcessor):
    """"""

    def __init__(self, master: Tk, panels_in: List[Panel], save_to):
        """"""


        self.__state = State.DEFAULT
        self.__panels_in = panels_in
        self.__clicks = []

        # Toolbar
        toolbar = Frame(root)
        circle_button = Button(toolbar, text="Circle",
                               command=self.enter_circle_state)
        polly_button = Button(toolbar, text="Poly",
                              command=self.enter_polly_state)
        next_button = Button(toolbar, text="Next",
                             command=self.next_and_save)
        self.state_lable = Label(root, text=f'State: {self.__state}')
        circle_button.pack(side=LEFT, padx=2, pady=2)
        polly_button.pack(side=LEFT, padx=2, pady=2)
        next_button.pack(side=LEFT, padx=2, pady=2)
        self.state_lable.pack()
        toolbar.pack(side=TOP, fill=X)

        ImageProcessor.__init__(self, master,
                                [panel.path for panel in panels_in], save_to)

        self.movable_image.canvas.bind('<Button-1>', self.left_mouse_down)
        self.movable_image.canvas.bind('<B1-Motion>', self.left_mouse_move)
        self.movable_image.canvas.bind('<ButtonRelease-1>', self.left_mouse_up)

    @property
    def curr_panel(self):
        for panel in self.__panels_in:
            if panel.path == self.curr_path:
                return panel

    def enter_polly_state(self):
        self.__state = State.POLLY
        self._reset()

    def enter_circle_state(self):
        self.__state = State.CIRCLE
        self._reset()

    def enter_default_state(self):
        self.__state = State.DEFAULT
        self._reset()

    def _reset(self):
        self.state_lable.config(text=f'State: {self.__state}')
        self.__clicks = []

    def next_and_save(self):
        """Load next image and save image to save_to"""
        self.save_img_to_folder_with_extra("annotated")
        self.load_next_img_or_end()

    def left_mouse_down(self, event):
        """Called whenever the left mouse is clicked on the image canvas"""
        x, y = self.movable_image.win_to_cv((event.x, event.y))
        pass

    def left_mouse_move(self, event):
        """Called whenever left mouse is moved while being held down
           on canvas.
        """
        x, y = self.movable_image.win_to_canvas((event.x, event.y))
        self._clear_canvas()
        if self.__state == State.CIRCLE:
            self._draw_circle_on_canvas_from_last_click((x, y))
        elif self.__state == State.POLLY:
            self._draw_line_on_canvas_from_last_click((x, y))

    def _clear_canvas(self):
        self.movable_image.canvas.delete(MARK_TAG)

    def _draw_circle_on_canvas_from_last_click(self, point: Tuple[int, int]):
        if len(self.__clicks) >= 1:
            p1 = self.movable_image.cv_to_canvas(self.__clicks[-1])
            p2 = point
            r = self._dist(p1, p2)
            self.movable_image.canvas.create_oval(p2[0] - r, p2[1] - r,
                                                  p2[0] + r, p2[1] + r,
                                                  width=CANVAS_LINE_THICKNESS,
                                                  tags=MARK_TAG,
                                                  dash=CANVAS_DASH_PATTERN,
                                                  outline=CANVAS_LINE_COLOR)

    def _draw_line_on_canvas_from_last_click(self, point: Tuple[int, int]):
        if len(self.__clicks) >= 1:
            p1 = self.movable_image.cv_to_canvas(self.__clicks[-1])
            p2 = point
            self.movable_image.canvas.create_line(p1[0], p1[1],
                                                  p2[0], p2[1],
                                                  width=CANVAS_LINE_THICKNESS,
                                                  tags=MARK_TAG,
                                                  dash=CANVAS_DASH_PATTERN,
                                                  fill=CANVAS_LINE_COLOR)

    def left_mouse_up(self, event):
        """Called when ever left mouse button is released"""
        x, y = self.movable_image.win_to_cv((event.x, event.y))

        if self.__state == State.POLLY:
            self._draw_line_on_cv_from_last_click((x, y))
            self.__clicks.append((x, y))

            if len(self.__clicks) >= 4:
                self._draw_line_on_cv_from_last_click(self.__clicks[0])

                print('Side 1:', self._dist(self.__clicks[0], self.__clicks[1]) * self.px_size(), 'cm')
                print('Side 2:', self._dist(self.__clicks[1], self.__clicks[2]) * self.px_size(), 'cm')
                print('Side 3:', self._dist(self.__clicks[2], self.__clicks[3]) * self.px_size(), 'cm')
                print('Side 4:', self._dist(self.__clicks[3], self.__clicks[0]) * self.px_size(), 'cm')

                quadrangle = Polygon(self.__clicks)

                print('Area:', quadrangle.area * self.px_size()**2, 'cm^2')

                self.enter_default_state()
        elif self.__state == State.CIRCLE:

            self._draw_circle_on_cv_from_last_click((x, y))
            self._draw_line_on_cv_from_last_click((x, y))
            self.__clicks.append((x, y))

            if len(self.__clicks) >= 2:

                radius = self._dist(self.__clicks[0], self.__clicks[1])

                print('Radius:', radius)

                print('Area:', np.pi * (radius ** 2))

                self.enter_default_state()

    def _draw_line_on_cv_from_last_click(self, point):
        if len(self.__clicks) >= 1:

            cv2.line(self.movable_image.cv_img, self.__clicks[-1], point,
                     LINE_COLOR, LINE_WIDTH)

            text_org = ((point[0] + self.__clicks[-1][0]) // 2,
                        (point[1] + self.__clicks[-1][1]) // 2 + int(TEXT_SIZE))

            length = np.round(self._dist(self.__clicks[-1], point) * self.px_size(), 0)

            cv2.putText(self.movable_image.cv_img,
                        f'{length}cm'
                        , text_org, TEXT_FONT, TEXT_SIZE, TEXT_COLOR,
                        thickness=TEXT_THICKNESS, bottomLeftOrigin=False)

            self.movable_image.refresh()

    def _draw_circle_on_cv_from_last_click(self, center):
        if len(self.__clicks) >= 1:
            cv2.circle(self.movable_image.cv_img, center,
                       int(self._dist(center, self.__clicks[0])),
                       LINE_COLOR, LINE_WIDTH)
            self.movable_image.refresh()

    def px_size(self) -> float:
        """
        Precondition: Solar panel has already been flattened
        :return: returns the size of a pixel in cm
        """
        x, y, _ = self.movable_image.cv_img.shape

        px_size = self.curr_panel.dims[0]

        return px_size

    def _dist(self, point1: tuple, point2: tuple) -> int:
        """Returns the distance in px between two points on the canvas"""
        delta_x = abs(point1[0] - point2[0])
        delta_y = abs(point1[1] - point2[1])
        return np.sqrt(delta_x**2 + delta_y**2)


if __name__ == '__main__':
    root = Tk()

    p1 = Panel((123, 143), (2000, 2000))
    p2 = Panel((123.1, 90.2), (3023, 1231))

    p1.path = "/home/lev/Pictures/OdroidJan2619/2019-01-26_21-48-13-682.jpg"
    p2.path = "/home/lev/Pictures/OdroidJan2619/2019-01-26_21-48-13-682.jpg"

    p1.dims = (12, 32)
    p2.dims = (12, 23)

    pro = DamageSelector(root, [p1, p2], "test")
    root.mainloop()
