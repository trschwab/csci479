#First version eeq

import argparse
import datetime
import imutils
import math
import cv2
import numpy as np

#below imports are for keep track of how long experiment takes and for threading to make video run smooth
#video running smooth now without Threading
import threading
import time

def runTest(whichBee = "testBee"):

    #whichBee = "testBee"

    resultList = ["A", "B", "NO CHOICE"]  #will use for enumeration of choices

    endResult = "NO CHOICE"

    running = True

    outputList = []

    locationList = []

    camera = cv2.VideoCapture("bees_c_cut_rev.mp4")
    startTime = time.time()     #start the timer to track experiment

    #camera = cv2.VideoCapture(1) #this is webcam

    firstFrame = None

    #Manually enter coords for solutions
    sol_a_x = 100
    sol_a_y = 100

    width = 800

    sol_b_x = 100
    sol_b_y = 200

    distance_sol_a = 0
    distance_sol_b = 0

    # loop over the frames of the video
    while True:

        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:

            # if the contour is too small, ignore it
            if cv2.contourArea(c) > 1500 or cv2.contourArea(c) < 100:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            #DRAW CIRCLES FOR WHERE THE SOLUTIONS ARE
            cv2.circle(frame, (sol_a_x, sol_a_y), 1, (0, 0, 255), 30) #Solution A
            cv2.circle(frame, (sol_b_x, sol_b_y), 1, (0, 255, 0), 30) #Solution B

            #center of rectangle. Rectangle
            rectagleCenterPont = ((x + x + w) // 2, (y + y + h) // 2)


            #draw lines from bee to solutions
            cv2.line(frame, (sol_a_x, sol_a_y), rectagleCenterPont, (250, 0, 1), 2) #distance line A
            cv2.line(frame, (sol_b_x, sol_b_y), rectagleCenterPont, (0, 250, 1), 2) #distance line B

            #calculate distance from bee to
            distance_sol_a = np.sqrt((sol_a_x - rectagleCenterPont[0])**2 + (sol_a_y - rectagleCenterPont[1])**2)
            distance_sol_b = np.sqrt((sol_b_x - rectagleCenterPont[0])**2 + (sol_b_y - rectagleCenterPont[1])**2)

            cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


        if distance_sol_a < 30:     #if bee is on sol_a cap, end experiment
            endTime = time.time()

            endResult = "A"

            running = False

        if distance_sol_b < 30:
            endTime = time.time()

            endResult = "B"

            running = False

        if running == False:
            outputList += [whichBee]
            outputList += [endResult]
            outputList += [endTime]
            print("heyyy")

            #cleanup the camera and close any open windows, safeGuard to keep us from adding things to our list after we want to be done with experiment
            #camera.release()
            #cv2.destroyAllWindows()
            #return (outputList, locationList)

        else:
            
            locationList += [rectagleCenterPont]

        #Functions to display text on screen
        cv2.putText(frame, "Distance to Solution A: {}".format(str(distance_sol_a)), (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.putText(frame, "Distance to Solution B: {}".format(str(distance_sol_b)), (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        cv2.imshow("Security Feed", frame)




print(runTest())
