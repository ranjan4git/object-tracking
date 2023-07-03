from collections import deque
import numpy as np
import argparse
import cv2

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