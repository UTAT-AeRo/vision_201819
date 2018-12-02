from tkinter import Label, Frame, Button, Entry, Tk, StringVar
import os
from PIL import Image, ImageDraw
import sys
sys.path.append("..")
from common import gui

class MarkerViewer(gui.Viewer):
    def __init__(self, *args, **kwargs):
        super(MarkerViewer, self).__init__(*args, **kwargs)
        self.lbl.bind('<Button-1>', self.on_click)
        self.dots = {file_name: [] for file_name in self.files}

    def get_image(self, filename):
        im = Image.open(filename)
        im = im.resize((self.img_x, self.img_y))
        draw = ImageDraw.Draw(im)
        if hasattr(self, 'dots'):
            for coord in self.dots[filename]:
                print(coord)
                draw.rectangle([c_i - 10 for c_i in coord]+[c_i + 10 for c_i in coord],fill='red')
        return im

    def on_click(self, button_press_event):
        x = button_press_event.x
        y = button_press_event.y
        filename = self.files[self.index]
        new_arr = []
        for coords in self.dots[filename]:
            if x not in range(coords[0]-10,coords[0]+11) or y not in range(coords[1]-10,coords[1]+11):
                print('got em')
                new_arr.append(coords)
        if len(new_arr) == len(self.dots[filename]):
            new_arr.append([x, y])
        self.dots[filename] = new_arr
        print(x, y)
        self.next_frame(self.index)

if __name__ == "__main__":
    dir_path = '../common/test/'
    filelist = [dir_path + x for x in os.listdir(dir_path)]
    root = Tk()
    app = MarkerViewer(root, filelist, 1000, 500)
    root.mainloop()