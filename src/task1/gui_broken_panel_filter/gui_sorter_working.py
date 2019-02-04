'''
This is the GUI sorter for further filtering broken solar panels.
Author: Aman Bhargava (amanb2000)

-------
Use: python3 gui_sorter_working_prototype.py --from json_name.json --to out_json_name.json
	- json_name.json is the file that contains the names of the images in the format
	stated on the trello board
	- out_json_name.json is the name of the json file to which you would like the
	program to output the data to.

	Use right arrow key to "swipe right" on truly damaged solar panels
	Use left arrow key to "swipe left" on not damaged solar panels
	If you make a mistake, use the up arrow key to go back.
-------
Outputs: a JSON file with a list of the right-swiped images

'''

from tkinter import *
import sys
import json
from PIL import ImageTk, Image

'''
Plan of action:
	1. (done)Get a bunch of images in this directory
	2. (done)Make an external json in the format from the trello with the images names
	3. (done)Make a navigation system for going back/forward through photos (arrow keys)
	4. (done)Make an internal data storage system (list of names of good images)
	5. (done)Create a data export system to JSON (in proper format)
	6. (done)Find a way to make sure all the images are constrianed to fit the window
	7. (done)Ensure proper IO for this module
'''

def getScaledDims(xdim, ydim):
	if (xdim/1280 > ydim/720):
		return [1280, int(ydim*(1280/xdim))]
	else:
		return [int(xdim*(720/ydim)), 720]

# System arguments 1 and 2: The input and output file names
json_file_name = sys.argv[2]
json_out_name = sys.argv[4]

# Opening the JSON file and getting its contents, putting the list of images in
# img_names
with open(json_file_name) as f:
	json_in_data = json.load(f)

img_names = json_in_data["positive"]

counter = 0 # Counter for which image we are on

good_images = [] # List to be outputted of the right-swiped images

root = Tk() # Code for making a GUI

# Setting the image for the first time
img = ImageTk.PhotoImage(Image.open(img_names[counter]))
scaleDims = getScaledDims(img.width(), img.height())
img = ImageTk.PhotoImage( (Image.open(img_names[counter]).resize((scaleDims[0], scaleDims[1]))) )
photo_label = Label(root, image = img)
photo_label.pack()

# Function called when we get to the end of the list of images to go through.
def end_program(final_data):
	with open(json_out_name, 'w') as outfile:
		json.dump({"positive": final_data}, outfile)
	exit() 

# Function called when "right swipped" (with the right arrow key)
def good_image(e):
	global counter
	global good_images

	if not(img_names[counter] in good_images):
		good_images += [img_names[counter]]
	counter += 1

	if(counter >= len(img_names)):
		end_program(good_images)

	print("good")
	img2 = ImageTk.PhotoImage(Image.open(img_names[counter]))

	scaleDims = getScaledDims(img2.width(), img2.height())
	img2 = ImageTk.PhotoImage( (Image.open(img_names[counter]).resize((scaleDims[0], scaleDims[1]))) )

	photo_label.configure(image=img2)
	photo_label.image = img2

# Function called when we "left-swipe" (left arrow key)
def bad_image(e):
	global counter
	global good_images

	if (img_names[counter] in good_images):
		bad_index = good_images.index(img_names[counter])
		good_images.pop(bad_index)

	counter += 1
	if(counter == len(img_names)):
		end_program(good_images)
	print("bad")
	img2 = ImageTk.PhotoImage(Image.open(img_names[counter]))

	scaleDims = getScaledDims(img2.width(), img2.height())
	img2 = ImageTk.PhotoImage( (Image.open(img_names[counter]).resize((scaleDims[0], scaleDims[1]))) )

	photo_label.configure(image=img2)
	photo_label.image = img2

# When up arrow key is pressed, we reverse the last action (undo)
def undo(e):
	global counter
	global good_images

	if len(good_images) > 0:
		good_images.pop(len(good_images)-1)
	counter -= 1 #TODO: Prevent out of bounds
	print("undo")
	img2 = ImageTk.PhotoImage(Image.open(img_names[counter]))

	scaleDims = getScaledDims(img2.width(), img2.height())
	img2 = ImageTk.PhotoImage( (Image.open(img_names[counter]).resize((scaleDims[0], scaleDims[1]))) )

	photo_label.configure(image=img2)
	photo_label.image = img2


# Binding keys to commands
root.bind("<Right>", good_image)
root.bind("<Left>", bad_image)
root.bind("<Up>", undo)

# Putting instructions on the screen:

w = Label(root, text=("Right arrow for real damage, left for fake damage, up arrow to go back."))
w.pack()

# Command to run the GUI - do not delete :)
root.mainloop()
