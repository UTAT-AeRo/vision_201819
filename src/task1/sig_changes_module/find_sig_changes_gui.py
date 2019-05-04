from tkinter import *
import os
from PIL import Image, ImageDraw
import sys

sys.path.append("..")
from common import gui, imagemetadata
from projection_module import projection
import json
import argparse


IMAGE_FORMATS = ('.bmp', '.jpg', '.png')

class MarkerViewer(gui.Viewer):
    def __init__(self, window, file_list, output_file, img_x=500, img_y=500):
        self.message = ''
        super(MarkerViewer, self).__init__(window, file_list, img_x, img_y)
        self.lbl.bind('<Button-1>', self.on_click)
        self.dots = {file_name: [] for file_name in self.files}
        self.output_file = output_file
        next_button = Button(self.button_fr, text="done",
                             command=self.handle_done)
        next_button.grid(row=0, column=12, sticky="e", padx=4, pady=4)

    # Draw the given image in filename
    def load_image(self, filename):
        im = gui.Viewer.load_image(self, filename)
        draw = ImageDraw.Draw(im)
        if hasattr(self, 'dots'):
            for coord, _ in self.dots[filename]:
                draw.rectangle(
                    [c_i - 10 for c_i in coord] + [c_i + 10 for c_i in coord],
                    fill='white')
        return im

    # Add new white blob to viewer, or remove white blob
    def on_click(self, button_press_event):
        x = button_press_event.x
        y = button_press_event.y
        filename = self.files[self.index]
        new_arr = []
        for coords, message in self.dots[filename]:
            if x not in range(coords[0] - 10, coords[0] + 11) or y not in range(
                    coords[1] - 10, coords[1] + 11):
                new_arr.append((coords, message))
        if len(new_arr) == len(self.dots[filename]):
            self.promt_for_message_and_make_point(new_arr, [x, y], filename)

    def promt_for_message_and_make_point(self, new_arr, pimg, filename):
        """Creates pop up requesting message and handles updating self.dots"""
        self.message = ''
        pop = Tk()
        pop.wm_title('What broke?')

        message_label = Label(pop, text='Message')
        message_label.pack()
        message_entry = Entry(pop)
        message_entry.pack()

        def done():
            self.message = message_entry.get()
            pop.destroy()
            new_arr.append((pimg, self.message))
            self.dots[filename] = new_arr
            self.next_frame(self.index)

        done_button = Button(pop, text='Done', command=done)
        done_button.pack(side=LEFT)

        pop.mainloop()

    def handle_done(self):
        ip = projection.ImageProjection()
        output_list = []
        output_dir = os.path.dirname(output_file)
        if output_dir is not None and not os.path.exists(output_dir):
            print(f'creating the output directory {output_dir}')
            os.makedirs(output_dir)

        with open(self.output_file, 'w') as fp:
            for filename in self.dots:
                # Get information from metadata
                entry = {}
                abs_path = os.path.abspath(filename)
                info_abs_path = '.'.join(abs_path.split('.')[:-1] + ['txt'])
                p = imagemetadata.MetadataProcessor()
                info = p.Process(p.Read(info_abs_path))
                i = info['corrected']
                yawangle = float(i['attitude']['yaw_angle'])
                pitchangle = float(i['attitude']['pitch_angle'])
                rollangle = float(i['attitude']['roll_angle'])
                altdrone = float(i['gps']['altitude_agl'])
                latdrone = float(i['gps']['latitude'])
                longdrone = float(i['gps']['longitude'])
                gpss = []
                for pimg, message in self.dots[filename]:
                    pimg = (pimg[0]*self.x_scale, pimg[1]*self.y_scale)
                    # Call projection code
                    try:
                        latlongalt = ip.get_pixel_coords(pimg, yawangle,
                                                         pitchangle,
                                                         rollangle, latdrone,
                                                         longdrone, altdrone)
                    except projection.AltitudeError:
                        print('Altitude Error')
                        continue
                    gpss.append(latlongalt[:2])
                # Add entry to json
                for gps in gpss:
                    entry['long'] = gps[0]
                    entry['lat'] = gps[1]
                    entry['message'] = [m for _, m in self.dots[filename]]
                    entry['filename'] = abs_path
                    output_list.append(entry)
            json.dump({"damaged": output_list}, fp)
        self.top.destroy()


# Self explanatory
def define_args():
    parser = argparse.ArgumentParser(description='Allows you to label significant changes')
    parser.add_argument('-d', '--input_dir',
                        help='specify input folder', required=True)
    parser.add_argument('-f', '--output_file',
                        help='specify output json file path', required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = define_args()
    input_dir = args.input_dir
    output_file = args.output_file
    images = []
    for root, _, files in os.walk(input_dir):
        images.extend([os.path.join(root, file) for file in files
                       if file.lower().endswith(IMAGE_FORMATS)])

    root = Tk()
    app = MarkerViewer(root, images, output_file, 1000, 500)
    root.mainloop()
