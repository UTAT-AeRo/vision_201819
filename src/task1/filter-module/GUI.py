import tkinter;
import tkinter.messagebox;
import cv2;
import PIL
from PIL import ImageTk, Image
import os

top = tkinter.Tk()
top.title("IR Light Filter")
top.geometry("1000x1000")



img = ImageTk.PhotoImage(Image.open("C:\\Users\\aa123\\Desktop\\AeRo\\download (2).jpg"))
panel = tkinter.Label(top, image= img)
panel.pack(fill = "both", expand = "yes")



def hello():
    tkinter.messagebox.showinfo("Say Hello","Hello World")


button = tkinter.Button(top, text ="Yes", command = hello, width=30, height=1000)
button.pack(side="left",fill="both", expand="no")
button = tkinter.Button(top, text ="No", width=30, height=1000)
button.pack(side="right",fill="both", expand="no")


yes_ir = list()
no_ir = list()




top.mainloop()

