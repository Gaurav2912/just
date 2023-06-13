# import the necessary packages
def face_recognition_call(slidePin, redPin, greenPin):
    """
    This function is used for rrcognition of face in current frame.
    Args: 
        slidePin : sildPin is either on (1) or off (0).
        greenPin : Position of green LED Pin in GPIO.
		redPin : Position of red LED in GPIO.
    """     
    
    from imutils.video import VideoStream
    # from imutils.video import FPS
    import face_recognition
    import imutils
    import sys
    import pytz
    import pickle
    import time
    import cv2
    from datetime import datetime, date
    import time
    import pandas as pd
    from gpiozero import LED
    from create_sheet_script import create_df
    import os
    import RPi.GPIO as GPIO
    import numpy as np

    def check_time_diff(old_time, currt_time, ref_day):
        """
        Return True if time diff. between current to old time is more than 60 sec 
        else Return False.
        Args:
            ref_day:  is any reference day.
			old_time: previous time.
			currt_time: current time.
        """
        # convert string to datetime object '%H:%M:%S' format
        old_objt = datetime.strptime(old_time, '%H:%M:%S').time()
        curr_objt = datetime.strptime(currt_time, '%H:%M:%S').time()
        # take time difference
        time_difft = datetime.combine(
            ref_day, curr_objt) - datetime.combine(ref_day, old_objt)
        # if grater than 60 second
        if time_difft.total_seconds() > 60:
            return True
        else:
            return False

    def know_MonthDayTime(arg_timezone="Asia/Kolkata"):
        '''Know current month, day and time'''
        # extract name of the month in form of string
        today_info = datetime.now(pytz.timezone(arg_timezone))
        current_month = today_info.strftime("%B")
        # current day of month
        current_day = int(today_info.strftime("%-d"))
        current_time = today_info.strftime("%H:%M:%S")

        return current_month, current_day, current_time

    def create_sheet(month, abs_path, data):
        '''Create Attendance sheet if not exist for that month.
                data : encoding file.
                month: current month
				abs_path: abslute path where the attendance sheet exist
        '''
        try:
            # check that if same file exist or not
            isExisting = os.path.exists(abs_path + f'Attendance_{month}.csv')

            if not isExisting:
                df = create_df(data)
                df.to_csv(
                    abs_path + f'Attendance_{month}.csv', index_label=['Date', 'Status'])

        except Exception as e:
            pass


    # import the csv file

    # Initialize 'currentname' to trigger only when a new person is identified.
    currentname = "unknown"
    abs_path = "/home/pi/dlib_face/"
    # Determine faces from encodings.pickle file model created from train_model.py
    encodingsP = abs_path + "encodings.pickle"

    # load the known faces and embeddings along with OpenCV's Haar
    # cascade for face detection
    # print("[INFO] loading encodings + face detector...")
    # print("[INFO] loading csv file...")

    try:
        data = pickle.loads(open(encodingsP, "rb").read())
        # unable to load pickle file or attendance file
    except Exception as e:
        print(e)
        # pass

    # Hyper parameters
    upsample = 1
    # 60 % confidence level
    confidance = 0.60
    # distance between faces
    dist = 1 - confidance

    # define a variable
    counter_un = 0

    # list of known faces and known encodings 
    known_face_names = data['names']
    known_face_encodings = data['encodings']

    # initialize the video stream and allow the camera sensor to warm up
    # Set the ser to the followng
    # src = 0 : for the build in single web cam
    vs = VideoStream(src=0).start()
    time.sleep(1.0)

    # start the FPS counter
    # fps = FPS().start()
    reference_day = date.today()
    # loop over frames from the video file stream if slidePin is high
    while GPIO.input(slidePin) == 1:

        # grab the frame from the threaded video stream
        frame = vs.read()

        # reduce the frame to its 50 percent size
        sml_frame = cv2.resize(frame, (0, 0), fx= 0.5, fy= 0.5)
        # sml_frame = imutils.resize(frame, width=500)
        # Change Opencv default BGR to RGB format for better accuracy
        sml_frame = cv2.cvtColor(sml_frame, cv2.COLOR_BGR2RGB)

        # if current_time_hr >= 18:
        #     # increase brightness
        #     sml_frame = np.uint8(255 * np.power((sml_frame / 255), 3/4))

        # Detect the bounding box around faces
        boxes = face_recognition.face_locations(sml_frame, upsample)

    # if more than 3 face is found than reduce it to 3 faces
        #if len(boxes) > 3:
            #boxes = boxes[:2]

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(sml_frame, boxes)
        # initilize names for each frame
        # this list contains name of all known person in
        # current frame
        names = []

        # loop over the facial embeddings
        # encoding is current face encoding
        # encodings can have maximum 3 face encodings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(known_face_encodings,
                                                     encoding, dist)
            name = "Unknown"  # if face is not recognized, then print Unknown

            # check to see if we have found a match
            if True in matches:
                # find the first match index 
                # of all matched faces 
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

 
            # update the list of names
            names.append(name)

        # Print name after end of for loop
        # print(names)


        # loop over the recognized faces
        # if name = [] then loop will not run
        for name in names:
        # for ((top, right, bottom, left), name) in zip(boxes, names):
        	# draw the predicted face name on the image - color is in BGR
        	# top = 2 * top
        	# right = 2 * right
        	# bottom  = 2 * bottom
        	# left = 2 * left
            # y = top - 15 if top - 15 > 15 else top + 15

            # cv2.rectangle(sml_frame, (left, top), (right, bottom),(0, 255, 225), 2)

        	
            # cv2.putText(sml_frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
        	# 	.8, (0, 255, 255), 2)

            # update the attendance in sheet

            if name != 'Unknown':

                # check if all name present in list csf
                # blink green LED for 1 sec
                greenPin.on()
                time.sleep(1.0)
                greenPin.off()
                
                # know the current month
                month, current_day, current_time = know_MonthDayTime("Asia/Kolkata")
                # # cearte attendance sheet if not exist
                create_sheet(month, abs_path, data)
                # import csv file with its multi index
                df = pd.read_csv(
                    abs_path + f"Attendance_{month}.csv",  index_col=['Date', 'Status'])
                # if name exist in data frame
                try:
                    # if entry time is not updated
                    # .iloc[0] for entry time and .iloc[1] for exit time
                    if pd.isnull(df[name].loc[current_day].iloc[0]):
                        # Entry and exit time is updated
                        df[name].loc[current_day] = current_time
                        # print(f"Entry time of {name} is updated. which is {current_time}")


                    # Previous exit time
                    old_exit_time = df[name].loc[current_day].iloc[1]
                    # If exit time difference is greater than 60 sec
                    # Than update new time
                    if check_time_diff(old_exit_time, current_time, reference_day):
                        # blink green LED for 1 sec
                        # greenPin.on()
                        # time.sleep(1.0)
                        # greenPin.off()
                        df[name].loc[current_day].iloc[1] = current_time
                        # print(f"Exit time of {name} is updated. which is {current_time}")

                    # export csv file
                    df.to_csv(
                        abs_path + f"Attendance_{month}.csv", index_label=['Date', 'Status'])

                except Exception as e:
                    # If name is not found in dataframe
                    # or LED can't glow
                    print(e)
                    # pass

        if set(names) == {'Unknown'}:
            counter_un += 1
            if counter_un == 5:
                # print("Unknown Person Detected")
                # blink red LED for 1 sec
                redPin.on()
                time.sleep(1.0)
                redPin.off()
                counter_un = 0
        # known or no person , than set counter to zero
        else:
            counter_un = 0

        # display the image to our screen
        #cv2.imshow("Facial Recognition is Running", frame)
        #key = cv2.waitKey(1) & 0xFF

        # quit when 'q' key is pressed
        #if key == ord("q"):
        #    break

        # update the FPS counter
        # fps.update()

    # stop the timer and display FPS information
    # fps.stop()
    # print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    # print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
