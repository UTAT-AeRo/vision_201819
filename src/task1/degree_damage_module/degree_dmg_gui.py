from tkinter import Label, Frame, Button, Entry, Tk, StringVar
import os
from PIL import Image, ImageDraw
import sys
sys.path.append("..")
from common import gui, imagemetadata
from shapely.geometry import Polygon
import json
import argparse

class DegreeDamageViewer(gui.Viewer):
    def __init__(self, window, file_list, output_file, img_x=500, img_y=500):
        '''
        Initialize the GUI

        :param window: Window size
        :param file_list: File list of images
        :param output_file: Output json file
        :param img_x: Width of image viewer
        :param img_y: Height of image viewer
        '''
        file_names = [x["file"] for x in file_list]
        super(DegreeDamageViewer, self).__init__(window, file_names, img_x, img_y)
        self.gps_coords = {x["file"]:x["dims"] for x in file_list}
        self.lbl.bind('<Button-1>', self.on_click)
        self.dots = {file_name: [] for file_name in self.files}
        self.shapes = {file_name: [] for file_name in self.files}
        self.messages = {file_name: '' for file_name in self.files}
        self.output_file = output_file
        next_button = Button(self.button_fr, text="done", command=self.handle_done)
        next_button.grid(row=0, column=12, sticky="e", padx=4, pady=4)
        polygon_button = Button(self.button_fr, text='add', command=self.handle_add_shape)
        polygon_button.grid(row=0, column=14, padx=4, pady=4)
        delete_button = Button(self.button_fr, text="delete",
                               command=self.handle_delete)
        delete_button.grid(row=0, column=16, padx=4, pady=4)

        self.message = StringVar()
        entry = Entry(self.button_fr, textvariable=self.message)
        entry.grid(row=3, column=0, pady=4)
        entry.bind('<Return>', self.record)

    def record(self, x):
        filename = self.files[self.index]
        self.messages[filename] = self.message.get()

    def get_image(self, filename):
        '''
        Open an image in the viewer
        :param filename: the filename of the image to open
        :return: None
        '''
        im = Image.open(filename)
        im = im.resize((self.img_x, self.img_y))
        draw = ImageDraw.Draw(im)
        if hasattr(self, 'dots'):
            for coord in self.dots[filename]:
                draw.rectangle([c_i - 10 for c_i in coord]+[c_i + 10 for c_i in coord],fill='white')
        if hasattr(self, 'shapes'):
            for coord_list in self.shapes[filename]:
                draw.polygon(tuple([tuple(x) for x in coord_list]), fill='white')
        return im

    def handle_delete(self):
        filename = self.files[self.index]
        if len(self.dots[filename]) > 0:
            self.dots[filename].pop(-1)
        elif len(self.shapes[filename]) > 0:
            self.shapes[filename].pop(-1)
        new_im = self.get_image(filename)
        self.tkimage.paste(new_im)

    def determine_level(self, xy_list):
        total_area = 0
        for xy in xy_list:
            total_area += Polygon(xy).area
        area_perc = total_area/(self.img_x*self.img_y)
        return area_perc

    def handle_add_shape(self):
        filename = self.files[self.index]
        self.shapes[filename].append(self.dots[filename].copy())
        self.dots[filename].clear()

        new_im = self.get_image(filename)
        self.tkimage.paste(new_im)

    def on_click(self, button_press_event):
        '''
        Add new white blob to viewer, or remove white blob
        :param button_press_event:
        :return: None
        '''
        x = button_press_event.x
        y = button_press_event.y
        filename = self.files[self.index]
        new_arr = []
        for coords in self.dots[filename]:
            if x not in range(coords[0]-10,coords[0]+11) \
                    or y not in range(coords[1]-10,coords[1]+11):
                new_arr.append(coords)
        if len(new_arr) == len(self.dots[filename]):
            new_arr.append([x, y])
        self.dots[filename] = new_arr

        new_im = self.get_image(filename)
        self.tkimage.paste(new_im)

    def next_frame(self, new_index):
        super(DegreeDamageViewer, self).next_frame(new_index)
        filename = self.files[self.index]
        self.message.set(self.messages[filename])
        new_im = self.get_image(filename)
        self.tkimage.paste(new_im)

    def handle_done(self):
        '''
        Use each specified dot to calculate the area and return the degree of damage
        in a json file
        :return: None
        '''
        output_json = []
        with open(self.output_file, 'w') as fp:
            for filename in self.shapes:
                output_json.append({
                    'lat': self.gps_coords[filename][0],
                    'long': self.gps_coords[filename][1],
                    'message': '{}: {}'.format(
                        self.determine_level(self.shapes[filename]),
                        self.messages[filename]),
                    'filename': filename
                })
            json.dump({'damaged':output_json}, fp)
        self.top.destroy()

# Self explanatory
def define_args():
    parser = argparse.ArgumentParser(description='Draw irregular polygon over image to specify an area '
                                                 'of damage and calculate the total percentage')
    parser.add_argument('-i', '--input_file', help='specify input json file path', required=True)
    parser.add_argument('-f', '--output_file', help='specify output json file path', required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = define_args()
    input_file = args.input_file
    output_file = args.output_file

    # Leave in for testing
    # input_file = './input_json'
    # output_file = './output_json'

    json_data = json.loads(open(input_file).read())
    root = Tk()
    app = DegreeDamageViewer(root, json_data, output_file,
                             1000, 500)
    root.mainloop()
