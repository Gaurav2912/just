def capture_faceimg_call(slidPin= None, greenPin= None):
    """
    This function is used for capturing face images to create the data set.
    Args: 
        slidePin : sildPin is either on (1) or off (0).
        greenPin : Position of green LED Pin at GPIO.
    """
    # import the necessary packages
    from imutils.video import VideoStream
    import face_recognition
    import cv2
    import os
    import sys
    import time
    from gpiozero import LED

    # green = LED(27)
    # red = LED(22)

    # Defining face_detector function 
    def face_detector(image):
        """Function detects faces and returns the image
        If no face detected, it returns None
        """
        # detect face using HOG with SVM
        # and return list of tuples with each tuples have location 
        # of faces in the image
        # Reduce the dimension of the frame
        current_frame_small = cv2.resize(image,(0,0),fx=0.5,fy=0.5)
        #detect all faces in the image
        #arguments are image,no_of_times_to_upsample, model
        all_face_locations = face_recognition.face_locations(current_frame_small,model='hog')
        
        # No face found in image/frame
        # Or more than one face is found
        if len(all_face_locations) != 1:
            return None
        
        return image

    # Take input from yhe user
    name = input('Enter your name: ')
    
    # If input is exit , then quit the programming
    if name.lower() == 'exit':
        sys.exit()
    
    # type pass or just press enter 
    # if you dont want to capture any image
    if (name.lower() != 'pass') and len(name) > 0:

        try:
            # image want maximun could be 10
            img_wnt = min(10, int(input("How many image do you want to capture : ")))
        except ValueError as msg:
            print(msg)
        
        # create a directory of that person
        # where all the image of that person will be save
        dir_name = os.path.join("/home/pi/dlib_face/dataset/", name) 
        print(dir_name)
        
        # check if directory is exist or not
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print("Directory created")
        else:
            print("Name already exist")

        # check the number of image that already exist in that folder of the person
        number_of_imgs = len(os.listdir(dir_name))

        if number_of_imgs != 0 :
            print(f"{number_of_imgs} images already exist of {name}")
        
        # Start video streaming from camera
        vs = VideoStream(src=0, framerate=32).start()
        # wait for two sec
        time.sleep(2.0)
        
        # iamge counter start from number of image already exist
        img_counter = number_of_imgs

        current_counter = 0
        # maximum 10 capture at a time
        while (current_counter < img_wnt):
            
            try:
                # grab the frame from the threaded video stream
                frame = vs.read()
                
                if frame is None:
                    print("Unable to load the frame, Camera is not properly connected.")
                    # sys.exit()
                    time.sleep(5.0)
                    continue
                    
                # if one face is found in current frame
                if face_detector(frame) is not None:
                    img_counter += 1
                    current_counter +=1 

                    img_name = "/home/pi/dlib_face/dataset/"+ name +"/image_{}.jpg".format(img_counter)
                    # save the face image in directory
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    # Green signal for sucessfully capture the image
                    greenPin.on()
                    time.sleep(1.0)
                    greenPin.off()
                    time.sleep(1.0)

                else:
                    print('No face detected or more faces detected.')
                    pass

            except AssertionError as msg:
                print(msg)

        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()

