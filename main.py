import cv2
import numpy as np
from tkinter import *
from tkinterdnd2 import *
from PIL import Image, ImageTk

class TkinterGUI:
    global var, image

    def __init__(self, master):
        self.master = master
        master.title("Peter's photo manipulator")

        self.label = Label(master, text="Peter's photo manipulator")
        self.label.pack(side=TOP)

        self.viewButton = Button(master, text="upscale", command=self.scaling)
        self.viewButton.pack()

        self.viewButton = Button(master, text="sharpen", command=self.sharpening)
        self.viewButton.pack()

        self.viewButton = Button(master, text="grayscale", command=self.grayScale)
        self.viewButton.pack()

        self.viewButton = Button(master, text="erode", command=self.erode)
        self.viewButton.pack()

        self.closeButton = Button(master, text="Close", command=self.close)
        self.closeButton.pack()

        #self.canvas = Canvas(master, bg="black", height=500, width=500)
        #self.canvas.pack()

        self.scale = Scale(master, variable=var, orient=HORIZONTAL, from_=1, to=200)
        self.scale.pack()

    def close(self):
        self.master.destroy()

    def scaling(self):
        global image, singleImage, var
        scale_percent = int(var.get())
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        # upscaler kivalasztasa
        # myinput = input('irja be a nagyitasi eljaras nevet \n')
        my_dict = {'nearest': cv2.INTER_NEAREST,
                   'linear': cv2.INTER_LINEAR,
                   'cubic': cv2.INTER_CUBIC,
                   'lanczos': cv2.INTER_LANCZOS4}
        myinput = "lanczos"
        image = cv2.resize(image, dim, my_dict[myinput])
        if singleImage != 0:
            cv2.destroyAllWindows()
        cv2.imshow("upscaled", image)
        singleImage = 1

    def sharpening(self):
        global kernel, image, singleImage
        kernel = np.array([[0, -1, 0],
                           [-1, 10, -1],
                           [0, -1, 0]])
        kernel = kernel / 5
        image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
        if singleImage != 0:
            cv2.destroyAllWindows()
        cv2.imshow("sharpened", image)
        singleImage = 1

    def grayScale(self):
        global image, singleImage
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if singleImage != 0:
            cv2.destroyAllWindows()
        cv2.imshow('grayscale', gray_image)

    def erode(self):
        global kernel, image, singleImage
        kernel = np.ones((6, 6), np.uint8)
        image = cv2.erode(image, kernel, cv2.BORDER_REFLECT)
        if singleImage != 0:
            cv2.destroyAllWindows()
        cv2.imshow("erode", image)
        singleImage =1

class MainPage:
    def __init__(self, master):
        self.master = master

        global image, var2, var

        self.button = Button(master, text="Image manipulation", command=self.Classic)
        self.button.pack()

        def drop(event):
            var2.set(event.data)


        Label(root, text='Path of the File').pack(anchor=NW, padx=10)
        e_box = Entry(root, textvar=var2, width=80)
        e_box.pack(fill=X, padx=10)
        e_box.drop_target_register(DND_FILES)
        e_box.dnd_bind('<<Drop>>', drop)


    def Classic(self):
        global image, var, myInput
        print(str(var2.get()))
        image = cv2.imread(str(var2.get()), flags=cv2.IMREAD_COLOR)
        root2 = Tk()
        root2.geometry('300x200')
        my_gui = TkinterGUI(root2)
        root.destroy()


image = cv2.imread('C:/Users/mpeti/Pictures/teszt3.png', flags=cv2.IMREAD_COLOR)
singleImage = 0
root = TkinterDnD.Tk()
root.geometry('300x200')
var = DoubleVar()
var = 100
var2 = StringVar()

#my_gui = TkinterGUI(root)
mainPage = MainPage(root)
root.mainloop()

#ablakok bezarasa
#cv2.waitKey()
#cv2.destroyAllWindows()

