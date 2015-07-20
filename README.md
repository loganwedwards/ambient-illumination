Ambient Illumination (or my not Ambilight clone)
=====

Philips released an interesting product with their Ambilight
technology. Unfortunately, it's proprietary to their hardware
only and other DIY solutions require running software on a PC
hooked up to a TV (and most of them require an analog signal
like s-video). Building on the great ideas of the diy community,
this solution uses a simple webcam to capture a scene to prevent
the need for having a computer hooked up to the video source.

Heck, this setup could even perform averaging of any scene in
general. Why limit it to just a TV (although that's my motivation)?

#### TODO
1. ~~Implement averaging for border~~
1. ~~Warp a quadrilaterial object to fill the scene~~
1. ~~User configurable zones for averaging.~~
1. Program the hardware
1. Exception handling
1. Simplify the UX
1. Automate the edge/corner detection and warping
1. White balance on stream
1. Exposure on stream
1. Let user reset points
1. Let user quit
1. CLI arguments

### Requirements
* Python, tested on v 2.7.x
* Numpy (and its deps)
* SciPy (and its deps)
* OpenCV (and its deps)

All of these bits can be installed via homebrew on Mac.

### Usage
1. run in root of project `python app.py`
1. Select 4 points of a scene in the following order:
  1. Top Left
  1. Top Right
  1. Bottom Left
  1. Bottom Right
1. Press any key to continue
1. Enjoy

### Resources
1. Quadrilateral Perspective Transform: http://opencv-code.com/tutorials/automatic-perspective-correction-for-quadrilateral-objects/
1. Capturing Mouse Events: http://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
1. OpenCV docs and warping: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
