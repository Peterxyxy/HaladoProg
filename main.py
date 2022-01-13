import cv2
from cv2 import cv2
from cv2 import dnn_superres
import numpy as np
from tkinter import *
from tkinterdnd2 import *
from PIL import Image, ImageTk



#_________________________manipulator________________________________

class Manipulator:
    global upscalerPercentage, image, upscalerSelected, dropDownSelection1

    def __init__(self, master):
        self.master = master
        master.title("Peter's photo manipulator")

        self.label = Label(master, text="Peter's photo manipulator")
        self.label.grid(column=0, row=0, columnspan=9)

        self.backButton = Button(master, text="Back", command=self.back)
        self.backButton.grid(column=0, row=1)

        self.dropDown = OptionMenu(master, upscalerSelected, "linear", "lanczos", "nearest", "cubic")
        self.dropDown.grid(column=1, row=1, padx=5)

        self.scale = Scale(master, variable=upscalerPercentage, orient=HORIZONTAL, from_=1, to=200)
        self.scale.grid(column=2, row=1, padx=5)

        self.viewButton = Button(master, text="upscale", command=self.scaling)
        self.viewButton.grid(column=3, row=1, padx=5)

        self.viewButton = Button(master, text="sharpen", command=self.sharpening)
        self.viewButton.grid(column=4, row=1, padx=5)

        self.viewButton = Button(master, text="invert", command=self.invert)
        self.viewButton.grid(column=5, row=1, padx=5)

        self.viewButton = Button(master, text="erode", command=self.erode)
        self.viewButton.grid(column=6, row=1, padx=5)

        self.saveButton = Button(master, text="save", command=self.save)
        self.saveButton.grid(column=7, row=1, padx=5)

        self.closeButton = Button(master, text="Close", command=self.close)
        self.closeButton.grid(column=8, row=1, padx=15)



    def close(self):
        self.master.destroy()

    def save(self):
        global image
        saveImage(image)

    def back(self):
        global root, mainPage
        for widget in root.winfo_children():
            widget.destroy()
        root.geometry('300x200')
        mainPage = MainPage(root)


    def scaling(self):
        global image, singleImage, upscalerPercentage, upscalerSelected, root
        scale_percent = int(upscalerPercentage.get())
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        if width<1 or height<1:
            errorRoot = Tk()
            errorLabel = Label(errorRoot, text='"The image would be to small to see! \nPlease try a bigger number."')
            errorLabel.pack(padx=10, pady=10)
            errorRoot.eval('tk::PlaceWindow . center')
        else:
            dim = (width, height)
            my_dict = {'nearest': cv2.INTER_NEAREST,
                       'linear': cv2.INTER_LINEAR,
                       'cubic': cv2.INTER_CUBIC,
                       'lanczos': cv2.INTER_LANCZOS4}
            image = cv2.resize(image, dim, my_dict[upscalerSelected.get()])
            appScaler(100)
            if singleImage != 0:
                cv2.destroyAllWindows()
            singleImage = 1
            imageviewer(root,TRUE)


    def sharpening(self):
        global kernel, image, singleImage, function
        kernel = np.array([[0, -1, 0],
                           [-1, 10, -1],
                           [0, -1, 0]])
        kernel = kernel / 5
        image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
        function = function + "sharpened_"
        if singleImage != 0:
            cv2.destroyAllWindows()
        singleImage = 1
        imageviewer(root,TRUE)


    def invert(self):
        global image, singleImage, function
        if singleImage != 0:
            cv2.destroyAllWindows()
        image = cv2.bitwise_not(image)
        function = function + "inverted_"
        singleImage = 1
        imageviewer(root,TRUE)

    def erode(self):
        global kernel, image, singleImage, function
        kernel = np.ones((6, 6), np.uint8)
        image = cv2.erode(image, kernel, cv2.BORDER_REFLECT)
        function = function + "eroded_"
        if singleImage != 0:
            cv2.destroyAllWindows()
        singleImage =1
        imageviewer(root,TRUE)


#_________________________AI_ upscalers________________________________

class AIUpcscaler:
    def __init__(self, master):
        self.master = master
        master.title("Peter's photo upscaler")

        self.backButton = Button(master, text="Back", command=self.back)
        self.backButton.pack(padx=5, pady=25)

        self.label=Label(master, text='Please choose an upscaling algorithm,\n when you click on one,\n the image will be upscaled \n and saved to the application folder')
        self.label.pack()

        self.upscaleButton = Button(master, text="ESPCN", command=self.espcnUpscale)
        self.upscaleButton.pack(padx=5, pady=5)

        self.upscaleButton = Button(master, text="FSRCNN", command=self.fsrcnnUpscale)
        self.upscaleButton.pack(padx=5, pady=5)

        self.upscaleButton = Button(master, text="LapSRN", command=self.lapsrnUpscale)
        self.upscaleButton.pack(padx=5, pady=5)

        self.upscaleButton = Button(master, text="EDSR (WARNING: resource intensive)", command=self.edsrUpscale)
        self.upscaleButton.pack(padx=5, pady=5)

        self.closeButton = Button(master, text="Close", command=self.close)
        self.closeButton.pack(padx=5, pady=25)


    def espcnUpscale(self):
        global image, pathToImage, function
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = "ESPCN_x2.pb"
        sr.readModel(path)
        sr.setModel("espcn", 2)
        upscaledImage = sr.upsample(image)
        cv2.imshow("upscaled with ESPCN", upscaledImage)
        function = "espcn_"
        saveImage(upscaledImage)

    def fsrcnnUpscale(self):
        global image, pathToImage, function
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = "FSRCNN_x2.pb"
        sr.readModel(path)
        sr.setModel("fsrcnn", 2)
        upscaledImage = sr.upsample(image)
        cv2.imshow("upscaled with FSRCNN", upscaledImage)
        function = "fsrxnn_"
        saveImage(upscaledImage)

    def lapsrnUpscale(self):
        global image, pathToImage, function
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = "LapSRN_x2.pb"
        sr.readModel(path)
        sr.setModel("lapsrn", 2)
        upscaledImage = sr.upsample(image)
        cv2.imshow("upscaled with LapSRN", upscaledImage)
        function = "lapsrn_"
        saveImage(upscaledImage)

    def edsrUpscale(self):
        global image, pathToImage, function
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = "EDSR_x2.pb"
        sr.readModel(path)
        sr.setModel("edsr", 2)
        upscaledImage = sr.upsample(image)
        cv2.imshow("upscaled with EDSR", upscaledImage)
        function = "edsr_"
        saveImage(upscaledImage)

    def close(self):
        self.master.destroy()

    def back(self):
        global root, mainPage
        for widget in root.winfo_children():
            widget.destroy()
        cv2.destroyAllWindows()
        root.geometry('300x200')
        mainPage = MainPage(root)



#_________________________main_page________________________________

class MainPage:
    def __init__(self, master):
        self.master = master

        global image, pathToImage, upscalerPercentage

        def drop(event):
            pathToImage.set(event.data)

        Label(root, text='Please enter the path of an image:\n(you can also drag and drop the file to the box!)').pack(anchor=NW, padx=10, pady=10)
        e_box = Entry(root, textvar=pathToImage, width=80)
        e_box.pack(fill=X, padx=10)
        e_box.drop_target_register(DND_FILES)
        e_box.dnd_bind('<<Drop>>', drop)

        self.button = Button(master, text="Image manipulation", command=self.classic)
        self.button.pack(pady=5)

        self.button = Button(master, text="AI upscaling", command=self.aiUpscaler)
        self.button.pack(pady=5)

        self.closeButton = Button(master, text="Close", command=self.close)
        self.closeButton.pack(pady=15)

    def close(self):
        self.master.destroy()

    def classic(self):
        global validatedImageFlag, image
        if ImageValidation():
            global image, upscalerPercentage, pathToImage, singleImage
            for widget in root.winfo_children():
                widget.destroy()
            appScaler(100)
            manipulator = Manipulator(root)
            imageviewer(root,TRUE)

    def aiUpscaler(self):
        global validatedImageFlag, image
        if ImageValidation():
            global image, upscalerPercentage, pathToImage, singleImage
            for widget in root.winfo_children():
                widget.destroy()
            appScaler(400)
            aIUpcscaler = AIUpcscaler(root)
            imageviewer(root, FALSE)



#_________________________global_functions________________________________

def ImageValidation():
    global validatedImageFlag, image
    image = cv2.imread(str(pathToImage.get()), flags=cv2.IMREAD_COLOR)
    if image is not None:
        return True
    else:
        errorRoot = Tk()
        errorLabel = Label(errorRoot, text='"The given path is incorrect! \nPlease try again."')
        errorLabel.pack(padx=10, pady=10)
        errorRoot.eval('tk::PlaceWindow . center')

def imageviewer(master, grid):
    global image, root, singleImage
    img = image
    blue, green, red = cv2.split(img)
    img = cv2.merge((red, green, blue))
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im)
    if singleImage != 0:
        for widget in root.winfo_children():
            temp = widget
        widget.destroy()
    if grid==TRUE:
        ImageLabel = Label(master, image=imgtk).grid(column=0, row=44, columnspan=300, sticky=S)
        master.mainloop()
    else:
        ImageLabel = Label(master, image=imgtk).pack()
        master.mainloop()


def appScaler(menuHeight):
    global image, root
    width = int(image.shape[1])
    height = int(image.shape[0])
    if width<600: width=600
    root.geometry(str(width) + "x" + str(menuHeight+height))


def saveImage(image):
    global pathToImage, function
    fileName = str(function + "image.jpg")
    cv2.imwrite(str(fileName), image)




#_________________________constants_and_init________________________________

singleImage = 0
validatedImageFlag = 0
root = TkinterDnD.Tk()
root.geometry('300x200')
root.eval('tk::PlaceWindow . center')
upscalerPercentage = DoubleVar()
pathToImage = StringVar()
upscalerSelected = StringVar()
function = ""
upscalerSelected.set("nearest")
dropDownSelection1 = ['nearest',
                   'linear',
                   'cubic',
                   'lanczos']
hide = 1


mainPage = MainPage(root)
root.mainloop()



