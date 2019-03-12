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
        super(DegreeDamageViewer, self).__init__(window, file_list, img_x, img_y)
        self.lbl.bind('<Button-1>', self.on_click)
        self.dots = {file_name: [] for file_name in self.files}
        self.output_file = output_file
        next_button = Button(self.button_fr, text="done", command=self.handle_done)
        next_button.grid(row=0, column=12, sticky="e", padx=4, pady=4)


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
        return im

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
            if x not in range(coords[0]-10,coords[0]+11) or y not in range(coords[1]-10,coords[1]+11):
                new_arr.append(coords)
        if len(new_arr) == len(self.dots[filename]):
            new_arr.append([x, y])
        self.dots[filename] = new_arr
        self.next_frame(self.index)

    def handle_done(self):
        '''
        Use each specified dot to calculate the area and return the degree of damage
        in a json file
        :return: None
        '''
        output_json = []
        with open(self.output_file, 'w') as fp:
            for filename in self.dots:
                polygon = Polygon(self.dots[filename])
                area_perc = polygon.area/(self.img_x*self.img_y)
                output_json.append({filename: {'damaged_area':area_perc}})
            json.dump({'positive':output_json}, fp)
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
    app = DegreeDamageViewer(root, json_data['positive'], output_file, 1000, 500)
    root.mainloop()