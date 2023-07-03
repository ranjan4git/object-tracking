from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

#Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optimal) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# initialize the list of tracked points
pts = deque(maxlen=args["buffer"])

#if no video path supplied, refer webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()

# otherwise, refer the video file (obviously)
else:
    vs = cv2.VideoCapture(args["video"])

#allow the webcam or video file to warm up
time.sleep(2.0)