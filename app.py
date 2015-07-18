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

# useful value for different lighting conditions
BIAS = 0.0
corners = []

def open_file():
    '''
    For prototyping, let's just read a static image in
    and apply our logic before looping over a video stream.
    '''
    return cv2.imread('test2.jpg')

def open_stream():
    '''
    Open a video stream using cv2's convenience method.
    '''
    return cv2.VideoCapture(0)

def find_edges(img):
    '''
    Assuming that our scene is simple, e.g., no distractions in the
    background from the subject (a tv or picture), let's detect the
    edges of the interesting area (what we want to base our output on)
    and return that section of the image.
    '''
    return cv2.Canny(img, 150, 255)

def transform_image(img):
    '''
    (advanced) Time permitting, allow the camera to be placed anywhere
    so that a transform can be applied and we can grab the areas of
    interest.
    '''
    global corners
    bounds = numpy.float32([[0,0], [640, 0], [0, 480], [640, 480]])
    corners = numpy.float32(corners)
    M = cv2.getPerspectiveTransform(corners, bounds)
    dst = cv2.warpPerspective(img, M, (640,480))
    return dst

def fill_screen(frame_in):
    # edges = find_edges(frame_in)
    edges = cv2.Canny(frame_in, 150, 255)
    MIN_LINE_LEN = 100
    MAX_LINE_GAP = 10
    lines = cv2.HoughLinesP(edges, 1, numpy.pi/180, 100, MIN_LINE_LEN, MAX_LINE_GAP)
    try:
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(frame_in,(x1,y1),(x2,y2),(0,255,0),2)
    except:
        return frame_in
    return frame_in

def average_pixels (image, horiz=16, vert=8):
    '''
    Apply a convolution (maybe) over the image to average colors of the scene.
    u x x u     x = horizontal_regions
    y     y     y = vertical_regions
    y     y     u = nodes computed in both directions, for simplicity
    u x x u

    We want to create regions that will represent a single node (LED) in
    the final output. The constants are defined with defaults.
    '''
    # print image.shape
    height, width = image.shape[:2]
    horiz_pixels = width / horiz

    vert_pixels = height / vert
    mask = numpy.zeros((vert_pixels, horiz_pixels, 3))
    # print 'mask\n', mask

    # top row
    for col in range(horiz):
        bl = mask.shape[0]
        tl = mask.shape[1]*col
        tr = mask.shape[1] * (col + 1)
        # returns tuple of len 4, but we ignore alpha channel
        image[0:bl, tl:tr] = cv2.mean(image[0:bl, tl:tr])[:3]

    # left col
    for row in range(vert):
        rh = mask.shape[1]
        top = mask.shape[0] * row
        bot = mask.shape[0] * (row + 1)
        image[top:bot, 0:rh] = cv2.mean(image[top:bot, 0:rh])[:3]


    # right col
    for row in range(vert):
        rh = width
        lh = rh - mask.shape[1]
        top = mask.shape[0] * row
        bot = mask.shape[0] * (row + 1)
        image[top:bot, lh:rh] = cv2.mean(image[top:bot, lh:rh])[:3]

    # bottom row
    for col in range(horiz):
        bot = height
        top = bot - mask.shape[0]
        lh = mask.shape[1] * col
        rh = mask.shape[1] * (col + 1)
        image[top:bot, lh:rh] = cv2.mean(image[top:bot, lh:rh])[:3]
    return image

def save_output (output):
    '''
    For prototyping, save the output as an image as a novel representation
    of the scene and for demoing the capabilities of the system.
    '''
    cv2.imwrite('output2.jpg', output)

def send_array(output):
    '''
    send the output as a stream to the serial monitor, so a listener
    like an Arduino can read the stream and process the input to turn
    on some LEDs.
    '''
    pass

def add_corner(event, x, y, flags, param):
    '''
    Callback to capture a click event. User must select corners in
    the following order: Top Left, Top Right, Bottom Left, Bottom Right
    '''
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'add corner event'
        global corners, setup_frame_copy
        if len(corners) is 4:
            cv2.destroyWindow('corners')
            return
        else:
            corners.append([x, y])
            cv2.circle(setup_frame_copy,(x,y),5,(0,255,0),-1)
            print 'coords: (%d, %d)' % (x, y)
        cv2.imshow('corners', setup_frame_copy)

# test_image = open_file()
# output = average_pixels(test_image)
# save_output(output)

# Intended operation
capture = cv2.VideoCapture(0)
capture.set(3,640)
capture.set(4,480)
# Get a frame for picking corners
ret, setup_frame = capture.read()

setup_frame_copy = setup_frame.copy()
# capture.release()
cv2.namedWindow('corners')
cv2.setMouseCallback('corners', add_corner)
cv2.imshow('corners', setup_frame_copy)

cv2.waitKey(0)
cv2.destroyWindow('corners')

# now we have corners, so warp the image to fit the screen
cv2.imshow('result', transform_image(setup_frame_copy))
cv2.waitKey(0)

while True:
    ret, frame = capture.read()
    # this works
    # edges = find_edges(frame)
    # cv2.imshow('canny',edges)
    ## frame_edges = fill_screen(frame)

    # corners is set as global above
    bounded_frame = transform_image(frame)
    cv2.imshow('image', average_pixels(bounded_frame))
    # transformed_frame = transform_image(frame)
    # send_array(average_pixels(transformed_frame))
