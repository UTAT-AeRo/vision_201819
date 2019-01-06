from tkinter import *
from typing import Tuple
import nPTransform
import numpy as np
from image_gui import Image_GUI

# https://stackoverflow.com/questions/5501192/how-to-display-picture-and-get-mouse-click-coordinate-on-it

# TODO fix pTransform aspect ratio issue
# TODO Allow multiple images
# TODO Resize the window automatically
# TODO Implement Reset

class Image_Falattener(Image_GUI):
    """This class represents an the image processing application
        *** This class assumes the solar panels are rectangles ***

    ==== Atributes ===
    clicks: the clicks that have been made on the canvas
    save_to: the folder to which the images will be saved.
    dim: This is a tuple containing first the length of the smaller
        edge of the solar panel (width in mm) and then the larger edge
        (height in mm).
    """

    def __init__(self, master: Tk, paths: str, save_to: str, dim: Tuple[int, int]):
        """
        :param master: The root for this Tk window
        :param paths: The paths to each file
        :param save_to: The path to the folder to save images to
        :param dim: The is a tuple containing first the length of the smaller
        edge of the solar panel (width) and then the larger edge (height).
        """
        self.dim = dim
        self.clicks = []

        Image_GUI.__init__(self, master, paths, save_to)
        self.canvas.bind('<Button-1>', self.left_mouse_down)

    def left_mouse_down(self, event):
        """Called whenever the left mouse is clicked on the image canvas"""
        x, y = self.to_canvas((event.x, event.y))
        # https://stackoverflow.com/questions/28615900/how-do-i-add-a-mouse-click-position-to-a-list-in-tkinter
        self.canvas.create_oval(x - 10, y - 10,
                                x + 10, y + 10,
                                fill='red', width=1, tags='corners')

        # add tuple (x, y) to existing list
        self.clicks.append((x, y))

        if len(self.clicks) >= 4:
            rect = np.asarray([np.asarray(np.float32(p)) for p in
                               self.clicks])
            flat = nPTransform.four_points_correct_aspect(self.cv_img,
                                                          rect,
                                                          self.dim[0],
                                                          self.dim[1])

            self.canvas.delete('corners')
            self.save_img_to_folder_with_extra('_flat', flat)
            self.load_next_img_or_end()

            self.clicks = []


if __name__ == '__main__':
    root = Tk()
    pro = Image_Falattener(root, ['../Sample_Images/solar.jpg', '../Sample_Images/book.png'], 'test/', (215.9, 279.4))
    #cv2.imwrite("result.png", pro.process_image_at('Sample_Images/solar.jpg'))
    root.mainloop()


