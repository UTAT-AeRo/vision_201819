import json
import tkinter
import argparse
import PIL.Image
import PIL.ImageTk
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#  written by Alex Zhuang zhual@utschools.ca 2019/02/23

global index, basewidth, out, lat, long
global cycle, cyclecanvas, canvas, t, point, second
index = 0
basewidth = 300
out = {'damaged': []}


def output():
    """
    writes out the output json
    """
    global out
    with open('idsignificantchanges.json', 'w') as outfile:
        json.dump(out, outfile)
    top.destroy()


def prev():
    """
    decrements image index within inputsurveyphotos list
    """
    global index
    if (index > 0):
        index -= 1
        refresh()


def next():
    """
    increments image index within inputsurveyphotos list
    """
    global index
    if (index < len(inputsurveyphotos)-1):
        index += 1
        refresh()


def refresh(init=False):
    """
    Refresh the image in the image viewing window based on next or
    previous buttons. Resizes images if too large.

    if init is true, the canvas must be canvas must be created.
    """
    global cycle, cyclecanvas
    cycleimg = PIL.Image.open(inputsurveyphotos[index])
    wpercent = (basewidth/float(cycleimg.size[0]))
    hsize = int((float(cycleimg.size[1])*float(wpercent)))
    cycleimg = cycleimg.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    cyclephoto = PIL.ImageTk.PhotoImage(cycleimg)
    cycle.cyclephoto = cyclephoto
    cycle.geometry('{}x{}'.format(cyclephoto.width(), cyclephoto.height()+80))
    if init:
        cyclecanvas = tkinter.Canvas(cycle, width=cyclephoto.width(),
                                     height=cyclephoto.height())
    cyclecanvas.create_image(0, 0, image=cyclephoto, anchor=tkinter.NW)
    cyclecanvas.pack()


def save():
    """
    Saves the lat, long, and label description for the selected point
    """
    global index, lat, long, second, t, point
    desc = t.get("1.0", 'end-1c')
    out['damaged'].append({'lat': lat,
                           'long': long,
                           'message': desc,
                          'filename': inputsurveyphotos[index]})
    print("the current list of points is as follows:\n")
    for each in out['damaged']:
        print(each)
    second.destroy()


def delete():
    global second, canvas, point
    """
    cancels the creation of a point by removing the red point
    """
    canvas.delete(point)
    second.destroy()


def clicked(event):
    """
    a click on the map triggers this function.

    -checks if coordinates of click fit inside the image dimensions, to
    ensure that we can calculate lat/long validly
    -calculates lat, long based on relative position of click to the x
    and y dimension.
    -puts a red dot on map to mark labelled location
    -pops up window to add description to lat, long value.
    -If save and quit is clicked, saves the point.

    ** We assume that the image is oriented North

    lat calculation:
    (relative y of point in image * distance between latitude coordinates)
    + most southern latitude coordinate

    long calculation:
    (relative x of point in image * distance between longitude coordinates)
    + most western longitude coordinate
    """
    global index, lat, long, second, t, point
    if (event.x >= 0 and event.x <= photo.width() and event.y >= 0
            and event.y <= photo.height()):
        second = tkinter.Toplevel(width=300)

        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)

        lat = ((((photo.height()-event.y)/photo.height()) *
               abs(inputmap['topleft']['lat']-inputmap['bottomright']['lat']))
               + inputmap['bottomright']['lat'])
        long = (((event.x/photo.width()) *
                abs(inputmap['topleft']['long']
                - inputmap['bottomright']['long']))
                + inputmap['topleft']['long'])
        point = canvas.create_oval(x1, y1, x2, y2, fill="# FF0000",
                                   outline="# FF0000", width=10)
        second.grab_set()
        second.title("New Label")

        # message box
        msg = tkinter.Message(second, justify='center', width=300,
                              text="Label at (lat,long) \n{}, {}"
                              .format(lat, long))
        msg.pack()
        t = tkinter.Text(second, height=5, width=40)
        t.pack()

        button = tkinter.Button(second, text="Save and Quit", command=save)
        button.pack()

        second.protocol("WM_DELETE_WINDOW", delete)
        second.mainloop()


# Argparse section
parser = argparse.ArgumentParser(
                    description='You must specify paths to two jsons')
parser.add_argument("--map", help='valid path to the reference map json',
                    type=str)
parser.add_argument("--photos", help='valid path to the survey photos json',
                    type=str)
args = parser.parse_args()
mappath = args.map
photopath = args.photos

# read paths provided by command line arguments e.g.
# python idsignificantchanges.py --map=inputmap.json
# --photos=inputsurveyphotos.json
with open(mappath, 'r') as f:
    inputmap = json.load(f)
with open(photopath, 'r') as f:
    inputsurveyphotos = json.load(f)

# Create tk instance and set it to output the json on window close.
top = tkinter.Tk()
top.protocol("WM_DELETE_WINDOW", output)

# Open the map image and fit the window to the image dims
img = PIL.Image.open(inputmap['filename'])
photo = PIL.ImageTk.PhotoImage(img)
top.geometry('{}x{}'.format(photo.width(), photo.height()))

# Place a canvas over the entire window
canvas = tkinter.Canvas(top, width=photo.width(), height=photo.height())
canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
canvas.pack()

# on left-click on canvas, label a point
canvas.bind("<Button-1>", clicked)

# Second tk window for viewing inputsurveyphotos images and cycling through
cycle = tkinter.Toplevel()
# Window inialization
init = True
refresh(init)

# Cycle between images in the list using next and previous buttons
next = tkinter.Button(cycle, text="Next", command=next)
next.pack()
prev = tkinter.Button(cycle, text="Previous", command=prev)
prev.pack()

top.mainloop()
cycle.mainloop()
