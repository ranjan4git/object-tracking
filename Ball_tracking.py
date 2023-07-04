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

#loop over every frame
while True:
    #grab the current frame
    frame = vs.read()
    #handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # define end statement
    if frame is None:
        break

    #resize the frame
    frame = imutils.resize(frame, width=600)
    #blur
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    #convert to hsv color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # mask the color and remove any blobs left
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contour (outline) in mask and initialize centre (X,y) of ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # if a contour is found
    if len(cnts) > 0:
        # find largest contour, compute minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        #if radius exceeds a minimum value
        if radius > 10:
            # draw the circle and centroid on the frame
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0,255,255), 2)
            cv2.circle(frame, center, 5, (0,0,255), -1)

    # update the list of tracked points
    pts.appendleft(center)

    #loop over the set of tracked points
    for i in range(1, len(pts)):
        #if either of points are 'None', ignore
        if pts[i-1] is None or pts[i] is None:
            continue
        #otherwise, compute the thickness of the line and draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i-1], pts[i], (0,0,255), thickness)

    #show the frame to our screen
    cv2.imshow("Frame", frame)
    #show the mask (optional) to the screen
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1) & 0xFF

    #break look if 'q' is pressed
    if key == ord("q"):
        break

#stop camera video stream if not using a video file
if not args.get("video", False):
    vs.stop()
#else, release the camera
else:
    vs.release()

#close all windows
cv2.destroyAllWindows()