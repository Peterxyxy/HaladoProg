import PIL
import cv2
import numpy as np
from tkinter import *
from tkinterdnd2 import *
from PIL import Image, ImageTk

#_________________________manipulator________________________________

class Manipulator:
    global var, image

    def __init__(self, master):
        self.master = master
        master.title("Peter's photo manipulator")

        self.label = Label(master, text="Peter's photo manipulator")
        self.label.pack(padx=5, pady=5)

        self.backButton = Button(master, text="Back", command=self.back)
        self.backButton.pack(padx=5, pady=5)

        self.scale = Scale(master, variable=var, orient=HORIZONTAL, from_=1, to=200)
        self.scale.pack()

        self.viewButton = Button(master, text="upscale", command=self.scaling)
        self.viewButton.pack(padx=5, pady=5)

        self.viewButton = Button(master, text="sharpen", command=self.sharpening)
        self.viewButton.pack(padx=5, pady=5)

        self.viewButton = Button(master, text="grayscale", command=self.grayScale)
        self.viewButton.pack(padx=5, pady=5)

        self.viewButton = Button(master, text="erode", command=self.erode)
        self.viewButton.pack(padx=5, pady=5)

        self.closeButton = Button(master, text="Close", command=self.close)
        self.closeButton.pack(padx=5, pady=5)

        #photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))

        #self.canvas = Canvas(master, bg="black", height=500, width=500)
        #self.canvas.pack()
        #self.canvas.create_image(0, 0, image=photo)



    def close(self):
        self.master.destroy()

    def back(self):
        global root, mainPage
        for widget in root.winfo_children():
            widget.destroy()
        root.geometry('300x150')
        mainPage = MainPage(root)


    def scaling(self):
        global image, singleImage, var
        print(var.get())
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

#_________________________main_page________________________________

class MainPage:
    def __init__(self, master):
        self.master = master

        global image, var2, var

        def drop(event):
            var2.set(event.data)

        Label(root, text='A kép elérési útja:').pack(anchor=NW, padx=10, pady=10)
        e_box = Entry(root, textvar=var2, width=80)
        e_box.pack(fill=X, padx=10)
        e_box.drop_target_register(DND_FILES)
        e_box.dnd_bind('<<Drop>>', drop)

        self.button = Button(master, text="Image manipulation", command=self.Classic)
        self.button.pack(pady=10)

    def Classic(self):
        global validatedImageFlag, image
        if ImageValidation():
            global image, var, var2 ,myInput, singleImage
            for widget in root.winfo_children():
                widget.destroy()
            root.geometry('300x300')
            manipulator = Manipulator(root)


def ImageValidation():
    global validatedImageFlag, image
    image = cv2.imread(str(var2.get()), flags=cv2.IMREAD_COLOR)
    if image is not None:
        return True
    else:
        errorRoot = Tk()
        errorLabel = Label(errorRoot, text='"Nem megfelelő elérési utat adott meg! \nKérem próbálja újra."')
        errorLabel.pack(padx=10, pady=10)
        errorRoot.eval('tk::PlaceWindow . center')


#_________________________constants_and_init________________________________

image = cv2.imread('C:/Users/mpeti/Pictures/teszt3.png', flags=cv2.IMREAD_COLOR)
singleImage = 0
validatedImageFlag = 0
root = TkinterDnD.Tk()
root.geometry('300x150')
root.eval('tk::PlaceWindow . center')
var = DoubleVar()

var2 = StringVar()
hide = 1

mainPage = MainPage(root)
root.mainloop()

#my_gui = TkinterGUI(root)

#ablakok bezarasa
#cv2.waitKey()
#cv2.destroyAllWindows()

