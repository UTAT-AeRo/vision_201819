from tkinter import *
from typing import Tuple, List, Dict, Optional
import nPTransform
import numpy as np
from imageprocessor import ImageProcessor, JsonFormatError
import argparse
import os
import json
from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon


DOT_SIZE = 10
PANEL_MARKER_COLOUR = 'blue'
CORNER_COLOUR = 'red'
DOT_TAG = 'dots'


class Panel:
    gps: Tuple[float, float]
    pixel: Tuple[int, int]
    dims: Tuple[int, int]
    path: str
    def __init__(self, gps, pixel):
        self.gps = gps
        self.pixel = pixel
        self.dims = None
        self.path = None


class ImageFlattener(ImageProcessor):
    """This class represents an the image processing application
        *** This class assumes the solar panels are rectangles ***

    ==== Properties ===
    dim: This is a tuple containing first the length of the smaller
        edge of the solar panel (width in cm) and then the larger edge
        (height in cm).
    saved: a list of the path to all of the _saved images
    """
    # === Private Attributes ===
    __panels_in: Dict[str, List[Panel]]  # a dictionary whose
    # keys are absolute paths to the images and whose values are a list panels
    # in those images.
    __selected_panel: Optional[Panel]
    __saved: List[Panel]
    __last_dims: Optional[Tuple[int, int]]
    __clicks: List[Tuple[int, int]]  # position of clicks on the canvas since
    # that have been made on the canvas since last reload
    __imgs_flattened: bool  # is the current image a of a flattened panel
    __num_saved: int  # the number of panels saved during while processing one
    # image

    def __init__(self, master: Tk, panels_in: Dict[str, List[Panel]],
                 save_to: str):
        """
        :param master: The root for this Tk window
        :param panels_in: a dictionary whose keys are absolute paths to the
        images and whose values are a list of pixel cords of panels in
        said images.
        :param save_to: The path to the folder to save images to.
        """
        self.__panels_in = panels_in
        self.__num_saved = 0
        self.__selected_panel = None
        self.__last_dims = None
        self.__clicks = []
        self.__saved = []

        # Toolbar
        toolbar = Frame(master)
        reload_button = Button(toolbar, text="Reload",
                               command=self.reload)
        save_button = Button(toolbar, text="Save",
                             command=self.save)
        next_button = Button(toolbar, text="Next",
                             command=self.next_file)
        reload_button.pack(side=LEFT, padx=2, pady=2)
        save_button.pack(side=LEFT, padx=2, pady=2)
        next_button.pack(side=LEFT, padx=2, pady=2)
        toolbar.pack(side=TOP, fill=X)

        ImageProcessor.__init__(self, master, list(panels_in.keys()), save_to)

        self.movable_image.canvas.bind('<Button-1>', self.left_mouse_down)
        self._master.after(200, self.reload)

    @property
    def saved(self) -> List[Panel]:
        return self.__saved

    def left_mouse_down(self, event):
        """Called whenever the left mouse is clicked on the image canvas"""

        if self.__selected_panel is not None:
            return

        x, y = self.movable_image.win_to_canvas((event.x, event.y))
        self.movable_image.make_dot(CORNER_COLOUR, (x, y), DOT_SIZE)

        # add tuple (x, y) to existing list
        self.__clicks.append((x, y))

        if len(self.__clicks) == 4:
            self.__selected_panel = self._get_panel_within_clicks()
            self._request_dims()

    def _flatten_img(self):
        """flatten the current img

        Precondition:
        self.__selected_panel is not None
        len(self._clicks) == 4
        """
        assert len(self.__clicks) == 4
        # convert clicks to an np array
        rect = np.asarray([np.asarray(
                           np.float32(
                           self.movable_image.canvas_to_cv(p)))
                           for p in self.__clicks])

        flat = nPTransform.four_points_correct_aspect(self.movable_image.cv_img,
                                                      rect,
                                                      self.__selected_panel.dims[0],
                                                      self.__selected_panel.dims[1])

        self.movable_image.cv_img = flat
        self.movable_image.reset()
        self.movable_image.clear_dots()

        self.__clicks = []

    def _get_panel_within_clicks(self) -> Panel:
        """returns the most central panel within the bounds of the clicked area of a panel
        with all attributes set to None if no such panel exists.

        Precondition:
        len(self.__clicks) == 4
        """
        bounds = Polygon(self.__clicks)

        panels_in_bounds = []

        for panels in self.__panels_in.values():
            for panel in panels:
                p = Point(panel.pixel)
                if p.within(bounds):
                    panels_in_bounds.append(panel)

        if panels_in_bounds == []:
            return Panel(None, None)
        else:
            min_dist_to_center = None
            closest_to_center = None
            for panel in panels_in_bounds:
                dist_to_center = Point(panel.pixel).distance(bounds.centroid)
                if min_dist_to_center is None or dist_to_center < min_dist_to_center:
                    min_dist_to_center = dist_to_center
                    closest_to_center = panel

            return closest_to_center




    def _make_panel_dots(self):
        """place dots that mark panels onto screen"""
        for panel in self.__panels_in[self.curr_path]:
            self.movable_image.make_dot(PANEL_MARKER_COLOUR,
                                        self.movable_image.cv_to_canvas(panel.pixel),
                                        DOT_SIZE)

    def reload(self):
        """Overrides because we need to reset img_flattened, add panel markers
        and remove dots"""
        ImageProcessor.reload(self)
        self.__selected_panel = None
        self.__clicks = []
        self._make_panel_dots()

    def next_file(self):
        """Runs when next button pressed saves image to save_to with prefix
        'flat' and loads the next image"""
        self.__selected_panel = None
        self.__num_saved = 0
        self.load_next_img_or_end()

    def save(self):
        """Save the current image"""
        if self.__selected_panel is not None:
            if len(self.saved) > 0:
                path = self.save_img_to_folder_with_extra(
                    f'_flat_{self.__num_saved}')
            else:
                path = self.save_img_to_folder_with_extra(f'_flat')
            self.__selected_panel.path = path
            self.__saved.append(self.__selected_panel)
            print(self.__saved)
            self.__num_saved += 1
            self.__selected_panel = None
            self.reload()

    def _request_dims(self):
        """Creates pop up requesting dimensions"""
        pop = Tk()
        pop.wm_title('Need dimensions')

        long_label = Label(pop, text='Longer side (cm)')
        long_label.pack()
        long_entry = Entry(pop)
        long_entry.pack()
        short_labe = Label(pop, text='Sorter side (cm)')
        short_labe.pack()
        short_entry = Entry(pop)
        short_entry.pack()

        def use_last():
            self.__selected_panel.dims = self.__last_dims
            pop.destroy()
            self._flatten_img()

        def done():
            short_str = short_entry.get()
            long_str = long_entry.get()

            try:
                short = float(short_str)
            except ValueError:
                print('That\'s not a number.')
                return
            try:
                long = float(long_str)
            except ValueError:
                print('That\'s not a number.')
                return

            if self.__selected_panel is None:
                print("No panel is selected")
                pop.destroy()
            self.__selected_panel.dims = (short, long)
            self.__last_dims = (short, long)
            pop.destroy()
            self._flatten_img()

        done_button = Button(pop, text='Done', command=done)
        done_button.pack(side=LEFT)

        if self.__last_dims is not None:
            skip_button = Button(pop, text='Use Last',
                                 command=use_last)
            skip_button.pack(side=LEFT)

        pop.mainloop()


def _parse_input(images_input: any) -> Dict[str, List[Panel]]:
    """Attempts to parse input from either list or dictionary if input is
    bad will throw useful errors"""

    panels_in = dict()
    if not isinstance(images_input, list):
        raise JsonFormatError('Json should be formatted like a list')

    for image_listing in images_input:
        if ('file' not in image_listing or
            'gps' not in image_listing or
                'pixels' not in image_listing):
            raise JsonFormatError('All items must contain a \"file\", \
                                  \"gps\" and \"pixle\" keys.')

        file = image_listing['file']
        gpss = image_listing['gps']
        pixels = image_listing['pixels']

        if not isinstance(file, str):
            raise JsonFormatError('File must be string')
        if not isinstance(gpss, list) or not isinstance(pixels, list) or \
           len(gpss) != len(pixels):
            raise JsonFormatError('\"gps\" and \"pixel\" should be a list \
                                   of the same length')

        for gps, pixel in zip(gpss, pixels):
            if len(gps) != 2:
                raise JsonFormatError('All items in \"gps\" must be len 2')
            if len(pixel) != 2:
                raise JsonFormatError('All items in \"pixel\" must be len 2')

            if file in panels_in:
                panels_in[file].append(Panel(gps, pixel))
            else:
                panels_in[file] = [Panel(gps, pixel)]

    return panels_in


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Flatten a list of panels')
    parser.add_argument('--input', type=str,
                        help='The path to the jason contain')
    parser.add_argument('--output', type=str,
                        help='The folder to save output json and new images')
    parser.add_argument('--dot_size', type=int,
                        help='The size of the dots used to mark and select panel corners.',
                        default=10
                        )

    arg = parser.parse_args()

    DOT_SIZE = arg.dot_size

    master = Tk()

    with open(arg.input) as input_json:
        images_input = json.load(input_json)

    panels_in = _parse_input(images_input)

    flattener = ImageFlattener(master, panels_in, arg.output)

    master.mainloop()

    if not os.path.exists(arg.output):
        os.makedirs(arg.output)

    output_list = []

    for panel in flattener.saved:
        panel_dict = dict()
        panel_dict['pixel'] = panel.pixel
        panel_dict['file'] = panel.path
        panel_dict['gps'] = panel.gps
        output_list.append(panel_dict)

    with open(os.path.join(arg.output, 'result.json'), 'w') as outfile:
        json.dump(output_list, outfile)
