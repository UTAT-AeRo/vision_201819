from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
import cv2

# https://stackoverflow.com/questions/5501192/how-to-display-picture-and-get-mouse-click-coordinate-on-it

# TODO Allow multiple images
# TODO Overlay an X for the selected regions
# TODO Resize the window automatically
# TODO Use CV instead of PIL since it's more efficient.


# function to be called when mouse is clicked
def printcoords(event):
    # outputting x and y coords to console
    print (event.x, event.y)

def gui():

    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    canvas = Canvas(frame, bd=0)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)

    frame.pack(fill=BOTH,expand=1)

    #adding the image
    File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
    # img = cv2.imread('Sample_Images/book.png')
    im = Image.open(File)
    img = ImageTk.PhotoImage(im)
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))
    w, h = im.size
    dim = str(w) + "x" + str(h)
    root.geometry(dim)

    #mouseclick event
    # create list of clicks
    clicks = []
    # create function to track clicks into 'clicks'
    tracking_function = track_to_list(clicks, root)
    # use clicks tracker generated as click handler
    canvas.bind('<Button-1>', lambda event: tracking_function(event))
    root.mainloop()

# https://stackoverflow.com/questions/28615900/how-do-i-add-a-mouse-click-position-to-a-list-in-tkinter
def track_to_list(lst, root):
    def left_mouse_click(event):
        # Should create and return a list
        canvas = event.widget
        canvas.create_oval(event.x - 10, event.y - 10,
                           event.x + 10, event.y + 10,
                           fill='red', width=1)
        # add tuple (x, y) to existing list
        lst.append((event.x, event.y,))
        print event.x, event.y
        print lst
        if (len(lst) >=4):
            root.destroy()
    return left_mouse_click


# TODO create rectangle for the selected image points
