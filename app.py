# Author: Logan Edwards

'''
Steps:
    1. Open an image (or stream)
    2. Run image detection to find edges of frame, like a tv
    3. (advanced) Warp image to be rectangle
    4. Run kernel over the edges of the frame to average colors
    5. Save output to image (prototyping) or send to serial stream
    which will be read via an Arduino (or similar) and represented
    in a LED array
'''
import cv2
import numpy

def openFile():
    '''
    For prototyping, let's just read a static image in
    and apply our logic before looping over a video stream.
    '''
    return cv2.imread('test.jpg')

def openStream():
    '''
    Open a video stream using cv2's convenience method.
    '''
    pass

def findEdges(image):
    '''
    Assuming that our scene is simple, e.g., no distractions in the
    background from the subject (a tv or picture), let's detect the
    edges of the interesting area (what we want to base our output on)
    and return that section of the image.
    '''
    pass

def transformImage(image):
    '''
    (advanced) Time permitting, allow the camera to be placed anywhere
    so that a transform can be applied and we can grab the areas of
    interest.
    '''
    pass

def applyKernel (image):
    horizontal_regions = 16
    vertical_regions = 8
    (height, width) = image.shape
    '''
    Apply a convolution over the image to average colors of the scene.
    '''


def saveOutput (output):
    '''
    For prototyping, save the output as an image as a novel representation
    of the scene and for demoing the capabilities of the system.
    '''
    cv2.imwrite('output.jpg')

def sendArray(output):
    '''
    send the output as a stream to the serial monitor, so a listener
    like an Arduino can read the stream and process the input to turn
    on some LEDs.
    '''
    pass
