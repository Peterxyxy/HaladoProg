#Import the tkinter library
from tkinter import *
import numpy as np
import cv2
from PIL import Image, ImageTk

#Create an instance of tkinter frame
win = Tk()
win.geometry("700x550")
Path = 'C:/Users/mpeti/Pictures/teszt3.png'

def imageviewer(path):
    img = cv2.imread(path)
    cv2.imshow("test", img)
    blue, green, red = cv2.split(img)
    img = cv2.merge((red, green, blue))
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im)
    Label(win, image=imgtk).pack()
    win.mainloop()

#Create a Label to display the image
imageviewer(Path)