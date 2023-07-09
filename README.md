# object-tracking
My self-project for detecting and tracking objects using OpenCV

Running the code:

>$ python ball_tracking.py --video test_video.mp4

or

>$ python ball_tracking.py

### Importing the packages

'deque' to maintain a queue of past N locations of the object, helping to draw the contrail of the ball as it is tracked; 
'argparse' for parsing our command line arguments;
'imutils' for ease in basic resizing, blurring and using contours;
