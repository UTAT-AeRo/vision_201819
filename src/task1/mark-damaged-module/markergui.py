from tkinter import Label, Frame, Button, Entry, Tk, StringVar
import os
from PIL import Image, ImageDraw
import sys
sys.path.append("..")
from common import gui
import json
import argparse

class MarkerViewer(gui.Viewer):
    def __init__(self, window, file_list, output_file, img_x=500, img_y=500):
        super(MarkerViewer, self).__init__(window, file_list, img_x, img_y)
        self.lbl.bind('<Button-1>', self.on_click)
        self.dots = {file_name: [] for file_name in self.files}
        self.output_file = output_file
        next_button = Button(self.button_fr, text="done", command=self.handle_done)
        next_button.grid(row=0, column=12, sticky="e", padx=4, pady=4)

    def get_image(self, filename):
        im = Image.open(filename)
        im = im.resize((self.img_x, self.img_y))
        draw = ImageDraw.Draw(im)
        if hasattr(self, 'dots'):
            for coord in self.dots[filename]:
                draw.rectangle([c_i - 10 for c_i in coord]+[c_i + 10 for c_i in coord],fill='red')
        return im

    def on_click(self, button_press_event):
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
        with open(self.output_file, 'w') as fp:
            json.dump(self.dots, fp)
        self.top.destroy()

def define_args():
    parser = argparse.ArgumentParser(description='Detect broken solar panels')
    parser.add_argument('-i', '--input_file', help='specify input json file path', required=True)
    parser.add_argument('-f', '--output_file', help='specify output json file path', required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = define_args()
    input_file = args.input_file
    output_file = args.output_file

    json_data = json.loads(open(input_file).read())
    root = Tk()
    app = MarkerViewer(root, json_data['positive'], output_file, 1000, 500)
    root.mainloop()