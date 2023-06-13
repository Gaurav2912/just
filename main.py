# import some importatnt libraries
import RPi.GPIO as GPIO
import time
from gpiozero import LED
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils, sys
import pytz
import pickle
import time
import cv2
from datetime import datetime, date
import time
import pandas as pd
from create_sheet_script import create_df
import os
from recog_script import face_recognition_call
from capture_faceimg_script import capture_faceimg_call

# central key at GPIO17
slidePin = 17
# Green LED at GPIO27
green = LED(27)
# RED LED at GPIO22
red = LED(22)


# Define a setup function for some setup
def setup():
    # for GPIO numbering, choose BCM  
    GPIO.setmode(GPIO.BCM)
    # take slidePin as GPIO input
    GPIO.setup(slidePin, GPIO.IN)


def main():
    while True:
        # slide switch high
        if GPIO.input(slidePin) == 1:
            # print ("Recognition activated")
            face_recognition_call(slidePin=slidePin, greenPin= green, redPin= red)

        # slide switch low, led2 on
        if GPIO.input(slidePin) == 0:
            # print ("                Capture Activated")
            capture_faceimg_call(greenPin= green)        
        
        time.sleep(3)

def destroy():
    # Turn off LED
    # But we are using gpiozero library for led
    # GPIO.output(led1Pin, GPIO.LOW)
    # GPIO.output(led2Pin, GPIO.LOW)
    # Release resource
    GPIO.cleanup()
    cv2.destroyAllWindows()

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the child program
    # destroy() will be  executed.
    except KeyboardInterrupt:
        # print("\nCtrl + C is pressed")
        # print("Exit")
        destroy()