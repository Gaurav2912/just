from imutils.video import VideoStream
from imutils.video import FPS
import cv2
import imutils
import time
import face_recognition
import numpy as np

# src = 0 : for the build in single web cam
vs = VideoStream(src=0).start()

time.sleep(2.0)


# start the FPS counter
fps = FPS().start()


img_counter = 0

while True:

    current_frame = vs.read()
    # display the image to our screen
    current_frame = imutils.resize(current_frame, width=500)    
    # current_frame
    cv2.imshow("Facial Recognition is Running", current_frame)
        
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    elif k%256 == 32:
        # SPACE pressed
        img_name = "set"+"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, current_frame)
        print("{} written!".format(img_name))
        img_counter += 1

    # update the FPS counter
    fps.update()


# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
