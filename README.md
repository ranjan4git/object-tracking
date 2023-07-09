# Object detection and tracking
My self-project for detecting and tracking objects using OpenCV

Running the code:

>$ python object_tracking.py

### Importing the packages

'deque' to maintain a queue of past N locations of the object, helping to draw the contrail as it is tracked; 
'argparse' for parsing our command line arguments;
'imutils' for ease in basic resizing, blurring, and using contours;

### Parsing arguments from Terminal

The first switch, --video, tells if a video file is there to be used. If this switch is supplied, OpenCV will grab a pointer to the video file and read frames from it. If not, it will try to access our webcam.

The second switch, --buffer, is the maximum buffer size of the deque, i.e., the last (x,y) coordinates of the object (default is 64). This deque allows us to draw the contrail of the object; hence larger the buffer, the larger the deque leading to a larger tail (since more points are being tracked).

>python object_tracking.py --buffer <desired contrail length>

Both these switches are optional.
