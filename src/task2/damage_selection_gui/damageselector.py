import argparse
import json
from tkinter import *
import cv2
from typing import Tuple, List, Optional, Dict
import numpy as np
from enum import Enum
from shapely.geometry import Polygon

# adds image the imageprocessor to the sys.path so that we can import it
import os
import sys
_script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.join(_script_path, os.pardir), 'common'))
from imageprocessor import Panel, ImageProcessor, JsonFormatError

# Defaults for args
LINE_WIDTH = 2
DECIMAL_PLACES = 0
TEXT_SIZE = 0.5

# Constants
LINE_COLOR = (0, 0, 255)
TEXT_THICKNESS = 2
TEXT_COLOR = (0, 125, 200)
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
MARK_TAG = "mark"
CANVAS_DASH_PATTERN = (5,)
CANVAS_LINE_COLOR = 'red'
CANVAS_LINE_WIDTH = LINE_WIDTH


class State(Enum):
    DEFAULT = 0
    POLLY = 1
    CIRCLE = 2


class DamageSelector(ImageProcessor):
    """Class for selecting and identifying damaged area
    """
    __state: State
    __panel_in: List[Panel]  # A list of panels input to the class these include
    # location, dimensions and path to an image of this.
    __clicks: List[Tuple[int, int]]  # list of all clicks since last reset.
    __state_label: Label  # The label at the top of the window displaying the
    # state of the DamageSelector

    def __init__(self, master: Tk, panels_in: List[Panel], save_to):
        """Create a new Damage selector"""

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
        self.__state_lable = Label(root, text=f'State: {self.__state}')
        circle_button.pack(side=LEFT, padx=2, pady=2)
        polly_button.pack(side=LEFT, padx=2, pady=2)
        next_button.pack(side=LEFT, padx=2, pady=2)
        self.__state_lable.pack()
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
        self.__state_lable.config(text=f'State: {self.__state}')
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

    # The following to methods do not directly edit the final image.
    # They add lines and circles to the canvas to preview the next part of the
    # selection.

    def _draw_line_on_canvas_from_last_click(self, point: Tuple[int, int]):
        """Draws a line from the last point in the clicks list to a point on
        the point given on the canvas. <point> is in canvas cords.
        """
        if len(self.__clicks) >= 1:
            p1 = self.movable_image.cv_to_canvas(self.__clicks[-1])
            p2 = point
            self.movable_image.canvas.create_line(p1[0], p1[1],
                                                  p2[0], p2[1],
                                                  width=CANVAS_LINE_WIDTH,
                                                  tags=MARK_TAG,
                                                  dash=CANVAS_DASH_PATTERN,
                                                  fill=CANVAS_LINE_COLOR)

    def _draw_circle_on_canvas_from_last_click(self, point: Tuple[int, int]):
        """Draws a circle with its edge being the last point in the clicks list
        and its center being the point provided on the canvas.
        <point> is in canvas cords.
        """
        if len(self.__clicks) >= 1:
            p1 = self.movable_image.cv_to_canvas(self.__clicks[-1])
            p2 = point
            r = self._dist(p1, p2)
            self.movable_image.canvas.create_oval(p2[0] - r, p2[1] - r,
                                                  p2[0] + r, p2[1] + r,
                                                  width=CANVAS_LINE_WIDTH,
                                                  tags=MARK_TAG,
                                                  dash=CANVAS_DASH_PATTERN,
                                                  outline=CANVAS_LINE_COLOR)

    def left_mouse_up(self, event):
        """Called when ever left mouse button is released"""
        x, y = self.movable_image.win_to_cv((event.x, event.y))

        if self.__state == State.POLLY:
            self._draw_line_on_cv_from_last_click((x, y))
            self.__clicks.append((x, y))

            if len(self.__clicks) < 4:
                return

            self._draw_line_on_cv_from_last_click(self.__clicks[0])

            print('Side 1:', self._dist(self.__clicks[0],
                                        self.__clicks[1]) * self.px_size(),
                  'cm')
            print('Side 2:', self._dist(self.__clicks[1],
                                        self.__clicks[2]) * self.px_size(),
                  'cm')
            print('Side 3:', self._dist(self.__clicks[2],
                                        self.__clicks[3]) * self.px_size(),
                  'cm')
            print('Side 4:', self._dist(self.__clicks[3],
                                        self.__clicks[0]) * self.px_size(),
                  'cm')

            quadrangle = Polygon(self.__clicks)

            print('Area:', quadrangle.area * self.px_size() ** 2, 'cm^2')

            self.enter_default_state()
        elif self.__state == State.CIRCLE:

            self._draw_circle_on_cv_from_last_click((x, y))
            self._draw_line_on_cv_from_last_click((x, y))
            self.__clicks.append((x, y))

            if len(self.__clicks) < 2:
                return

            radius = self._dist(self.__clicks[0], self.__clicks[1])

            print('Radius:', radius)

            print('Area:', np.pi * (radius ** 2))

            self.enter_default_state()

    def _draw_line_on_cv_from_last_click(self, point):
        """Draws a line from the last point in the clicks list to a point on
        the point given on the cv image that will be saved.
        <point> is in canvas cords.
        """
        if len(self.__clicks) >= 1:

            cv2.line(self.movable_image.cv_img, self.__clicks[-1], point,
                     LINE_COLOR, LINE_WIDTH)

            text_org = ((point[0] + self.__clicks[-1][0]) // 2,
                        (point[1] + self.__clicks[-1][1]) // 2 + int(TEXT_SIZE))

            length = np.round(
                self._dist(self.__clicks[-1], point) * self.px_size(),
                DECIMAL_PLACES)

            cv2.putText(self.movable_image.cv_img,
                        f'{length}cm'
                        , text_org, TEXT_FONT, TEXT_SIZE, TEXT_COLOR,
                        thickness=TEXT_THICKNESS, bottomLeftOrigin=False)

            self.movable_image.refresh()

    def _draw_circle_on_cv_from_last_click(self, center):
        """Draws a circle with its edge being the last point in the clicks list
        and its center being the point provided on the cv image that will be
        saved. <point> is in cv image cords.
        """
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

        px_size = self.curr_panel.dims[0] / x

        return px_size

    @staticmethod
    def _dist(point1: tuple, point2: tuple) -> int:
        """Returns the distance in px between two points on the canvas"""
        delta_x = abs(point1[0] - point2[0])
        delta_y = abs(point1[1] - point2[1])
        return np.sqrt(delta_x ** 2 + delta_y ** 2)


def parse_input(panel_listings: any) -> List[Panel]:
    """Attempts to parse input from either list or dictionary if input is
    bad will throw useful errors"""

    panels_in = []
    if not isinstance(panel_listings, list):
        raise JsonFormatError('Json should be formatted like a list')

    for image_listing in panel_listings:
        if ('file' not in image_listing or
                'gps' not in image_listing or
                'pixel' not in image_listing):
            raise JsonFormatError('All items must contain a \"file\", \
                                  \"gps\" and \"pixle\" keys.')

        file = image_listing['file']
        gps = image_listing['gps']
        pixel = image_listing['pixel']
        dims = image_listing['dims']

        if not isinstance(file, str):
            raise JsonFormatError('File must be string')
        if not isinstance(dims, list) or len(dims) != 2:
            raise JsonFormatError('\"dims\" should be a list of length 2')

        if gps is None or pixel is None:
            panels_in.append(Panel(None, None, tuple(dims), file))
        else:
            if not isinstance(gps, list) or not isinstance(pixel, list) \
               or len(gps) != 2 or len(pixel) != 2:
                raise JsonFormatError('\"gps\" and \"pixel 2\" should be a list\
                                        of length 2 or null')

            panels_in.append(Panel(tuple(gps), tuple(pixel), tuple(dims), file))

    return panels_in


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Flatten a list of panels')
    parser.add_argument('--input', type=str,
                        help='The path to the jason contain')
    parser.add_argument('--output', type=str,
                        help='The folder to save output new images')
    parser.add_argument('--line_width', type=int,
                        help='The size of the dots used to mark and select \
                        panel corners.',
                        default=LINE_WIDTH)
    parser.add_argument('--text_size', type=float, help='The size of the text on \
                        the final cv image', default=TEXT_SIZE)
    parser.add_argument('--decimal_places', type=int, help='The number of \
                        decimal points for lengths and areas',
                        default=DECIMAL_PLACES)

    args = parser.parse_args()

    LINE_WIDTH = args.line_width
    CANVAS_LINE_WIDTH = args.line_width
    TEXT_SIZE = args.text_size
    DECIMAL_PLACES = args.decimal_places

    with open(args.input) as input_json:
        panel_listings = json.load(input_json)

    panels_in = parse_input(panel_listings)

    root = Tk()
    pro = DamageSelector(root, panels_in, args.output)
    root.mainloop()
