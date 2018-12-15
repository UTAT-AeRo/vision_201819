import tkinter
import tkinter.messagebox
from tkinter import font
from json import loads
from json import dump
from PIL import ImageTk, Image
import cv2
import PIL
import os
import glob
import shutil
import _json

top = tkinter.Tk()
top.title("IR Light Filter")
top.geometry("20000x20000")

input_file = open('C:/Users/aa123/Desktop/input.json')
input_file_contents = input_file.read()
input_dict = loads(input_file_contents)
img_list = input_dict['positive']

counter = 0

positive = []

def handle_btn_click_yes():
    global counter
    positive.append(img_list[counter])
    counter = counter+1
    img_2 = ImageTk.PhotoImage(Image.open(img_list[counter]).resize((600, 600), Image.ANTIALIAS))
    panel.configure(image=img_2)
    panel.image = img_2

def handle_btn_click_no():
    global counter
    counter = counter+1
    img_3 = ImageTk.PhotoImage(Image.open(img_list[counter]).resize((600, 600), Image.ANTIALIAS))
    panel.configure(image=img_3)
    panel.image = img_3

def hello():
    tkinter.messagebox.showinfo("Say Hello","This is COOL!")

img = ImageTk.PhotoImage(Image.open(img_list[counter]).resize((600, 600), Image.ANTIALIAS))
panel = tkinter.Label(top, image= img)
panel.pack(fill = "none", expand = "no")

button = tkinter.Button(top, text =("Yes"), command = handle_btn_click_yes, padx = 275, pady = 100)
button.pack(side="left", fill="both")
button.config(bg='green',fg='white')
button.config(font=('helvetica',50))
button = tkinter.Button(top, text ="No", command = handle_btn_click_no, padx = 275, pady = 100)
button.pack(side="right", fill="both")
button.config(bg='red',fg='white')
button.config(font=('helvetica',50))

top.mainloop()

data = {
    "positive": [positive]
}
with open('positive_file.json', 'w') as write_file:
    dump(data, write_file)