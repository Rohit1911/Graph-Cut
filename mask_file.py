#Rohit Sriram Muniganti
#DF05298
#CMSC641 Project 1 Graphcut Images
#This is the python code used for creating the masked image file
import numpy as np                          #importing numpy & Other useful modules
import matplotlib.pyplot as plt             
import copy
import matplotlib.widgets as widgets
import os
import argparse
import cv2

FileNameOfPic1 = 'pic1.jpg'
FileNameOfPic2 = 'pic2.jpg'
FileNameOfMaskedPic = 'MaskedPic.jpg'
widthOfLine = 9
ColorPic1Line= (255, 255, 0)
ColorPic2Line = (0, 128, 255)

#Defining a function for accessing the images
def gettingPictures(pictureName, pictureLocation):
    

    picture = None

    if pictureName == "pic1":                                                           #Reading picture 1
        picture = cv2.imread(os.path.join(pictureLocation, FileNameOfPic1))
        picture = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)

    elif pictureName == "pic2":                                                         #Reading picture 2
        picture = cv2.imread(os.path.join(pictureLocation, FileNameOfPic2))
        picture = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)

    return picture

#Creating function for drawing the mask 
class MaskOutlineCreation():
    def __init__(self):
        ArgParse = argparse.ArgumentParser()
        ArgParse.add_argument('-i', dest='pictureDirectory', required=True, help='Saved location of pictures 1 & 2')
        args = ArgParse.parse_args()
  
        self.pictureDirectory = args.pictureDirectory
        self.CurrentPicture = "pic1"
        self.initialCoordinates = None
        self.pic1_input = gettingPictures("pic1", self.pictureDirectory)
        self.pic1_input_copy = copy.copy(self.pic1_input)
        self.pic2_input = gettingPictures("pic2", self.pictureDirectory)
        self.pic2_input_copy = copy.copy(self.pic2_input)
        self.Outline = np.zeros(self.pic2_input.shape)
        self.fig = plt.figure(figsize=(15, 15))
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.set_title("Select the image part you would like to add")   #Text that displays on top

    #Creating function for accessing the coordinates
    def TapOrClick(self, event):
        x = int(event.xdata)
        y = int(event.ydata)
        nextCoordinates = (x, y)

        if event.inaxes in [self.ax1]:
            if self.initialCoordinates == None:
                self.initialCoordinates = nextCoordinates
                print("Changing Coordinates {}".format(self.initialCoordinates))
            else:
                if self.CurrentPicture == "pic1":
                    cv2.line(self.Outline, self.initialCoordinates, nextCoordinates, ColorPic1Line, widthOfLine)
                    cv2.line(self.pic1_input_copy, self.initialCoordinates, nextCoordinates, ColorPic1Line, widthOfLine)
                    cv2.line(self.pic2_input_copy, self.initialCoordinates, nextCoordinates, ColorPic1Line, widthOfLine)
                    self.ax1.imshow(self.pic1_input_copy)
                elif self.CurrentPicture == "pic2":
                    cv2.line(self.Outline, self.initialCoordinates, nextCoordinates, ColorPic2Line, widthOfLine)
                    cv2.line(self.pic1_input_copy, self.initialCoordinates, nextCoordinates, ColorPic2Line, widthOfLine)
                    cv2.line(self.pic2_input_copy, self.initialCoordinates, nextCoordinates, ColorPic2Line, widthOfLine)
                    self.ax1.imshow(self.pic2_input_copy)
                self.initialCoordinates = nextCoordinates
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    #Function for clicking are going to next image and closing the window
    def ClickTheButton(self, event):
        if self.CurrentPicture == "pic1":
            self.CurrentPicture = "pic2"
            self.ax1.imshow(self.pic2_input_copy)
            self.initialCoordinates = None
        elif self.CurrentPicture == "pic2":
            self.CurrentPicture = "done"
            self.Outline = np.uint8(self.Outline)
            self.ax1.imshow(self.Outline)
            self.Outline = cv2.cvtColor(self.Outline, cv2.COLOR_RGB2BGR)
            cv2.imwrite(os.path.join(self.pictureDirectory, FileNameOfMaskedPic), self.Outline) #This writes the mask image file
        elif self.CurrentPicture == "done":
            plt.close()
    #Function for creating the final mask
    def CreatingTheMask(self):
        self.ax1.imshow(self.pic1_input)
        self.ax1.axis('off')
        axcut = plt.axes([0.9, 0.0, 0.1, 0.075])
        bcut = widgets.Button(axcut, 'Next/End', color='orange') #The button for going to the second image or to finish

        self.fig.canvas.mpl_connect('button_press_event', self.TapOrClick)
        bcut.on_clicked(self.ClickTheButton)

        plt.show()

#Calling the Mask function for creating the mask 
if __name__ == "__main__":
    FinalMask = MaskOutlineCreation()
    FinalMask.CreatingTheMask()