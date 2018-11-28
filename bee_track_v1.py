#First version eeq

import argparse
import datetime
import imutils
import math
import cv2
import numpy as np
import os
import csv
import datetime

#below imports are for keep track of how long experiment takes and for threading to make video run smooth
#video running smooth now without Threading
import threading
import time

my_dir = "videos"
my_file = "bees_c_cut_rev.mp4"
video_path = os.path.join(my_dir, my_file)      #gets path of video to import

EXPERIMENT_ID = 1

#This function only needs to be run once on the first frame.
def detect_caps(frame):
    #input a frame and output the positions of two caps.

    #detect yellow cap
    circle_frame_a = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    (h, s, v) = cv2.split(circle_frame_a)
    s = s*1
    s = np.clip(s,0,255)
    imghsv = cv2.merge([h,s,v])
    imghsv = cv2.cvtColor(imghsv, cv2.COLOR_BGR2HSV).astype("float32")
    circle_frame_a = cv2.cvtColor(imghsv.astype("uint8"), cv2.COLOR_HSV2BGR)
    circle_frame_a = cv2.cvtColor(circle_frame_a, cv2.COLOR_BGR2GRAY)
    circle_frame_a = cv2.threshold(circle_frame_a, 140, 255, cv2.THRESH_BINARY)[1]
    circles_a = cv2.HoughCircles(circle_frame_a, cv2.HOUGH_GRADIENT, 22, minDist=1, maxRadius=50)

    #detecct purple cap
    circle_frame_b = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circle_frame_b = cv2.threshold(circle_frame_b, 80, 255, cv2.THRESH_BINARY)[1]
    circle_frame_b = cv2.erode(circle_frame_b, None, iterations=2)
    #kernel = np.ones((5,5),np.uint8)
    #circle_frame_b = cv2.morphologyEx(circle_frame_b, cv2.MORPH_OPEN,kernel)
    #circle_frame_b = cv2.morphologyEx(circle_frame_b, cv2.MORPH_OPEN,kernel)
    #circle_frame_b = cv2.morphologyEx(circle_frame_b, cv2.MORPH_OPEN,kernel)
    circles_b = cv2.HoughCircles(circle_frame_b, cv2.HOUGH_GRADIENT, 22, minDist=1, maxRadius=50)


    #np.concatenate((a, b))
    #for c in circles_b:
    #for c in np.concatenate((circles_b[:,0,:], circles_a[:,0,:]),axis = 0):
    #np.array(np.append(circles_a,circles_b,axis=0)):
        #print(c)
        #if cv2.contourArea(c) < 100:
            #continue
        # circle_x = c[0]
        # circle_y = c[1]
        # circle_rad = c[2]
        # cv2.circle(frame, (circle_x, circle_y), 1, (0, 0, 255), 30) #Solution A
        #cv2.circle(frame, (sol_b_x, sol_b_y), 1, (0, 255, 0), 30) #Solution B

    caps = [circles_a[:,0,:],circles_b[:,0,:]]
    #caps = [circles_b[:,0,:]]
    return caps

def end_experiment(outputList, locationList, whichBee, endResult,  startTime, endTime):
    outputList += [EXPERIMENT_ID]
    outputList += [whichBee]
    outputList += [endResult]
    totalTime = endTime - startTime
    outputList += [("%.2f" % totalTime)]

    locations = []
    locations += [whichBee]
    locations += [locationList]


    locationList = locations

    now = datetime.datetime.now()
    outputList += [now.strftime("%Y-%m-%d %H:%M")]

    #cleanup the camera and close any open windows, safeGuard to keep us from adding things to our list after we want to be done with experiment

    #print((outputList, locationList))   #prints as of now to help us see whats up, NEEDS TO BE RETURN
    #print(len(locationList)/endtime)

    if(os.path.isfile("results.csv")):
        with open('results.csv','a') as fd:
            wr = csv.writer(fd, dialect='excel')
            #for i in outputList:
                #wr.writerow(outputList)

            wr.writerow(outputList)             #whichBee, which Cap it picked, how long it took
        fd.close()

    else:
        print("here")
        with open('results.csv','w') as fd:
            wr = csv.writer(fd, dialect='excel')

            wr.writerow(["Experiment ID","Bee ID","Cap","Trail Time","Date/Time"])
            wr.writerow(outputList)             #whichBee, which Cap it picked, how long it took
        fd.close()

    if(os.path.isfile("locations.csv")):
        with open('locations.csv','a') as fd:
            wr = csv.writer(fd, dialect='excel')

            wr.writerow(locationList)             #whichBee, which Cap it picked, how long it took
        fd.close()

            #for i in outputList:
                #wr.writerow(outputList)

        wr.writerow(["Experiment ID","Bee ID","Cap","Trail Time","Date/Time"])
        wr.writerow(outputList)             #whichBee, which Cap it picked, how long it took
        fd.close()

    with open('locations.csv','a') as fd:
        wr = csv.writer(fd, dialect='excel')


        #for i in locationList:
            #wr.writerow(i)

        wr.writerow(locationList)   #first item is whichBee ran the test, rest of columns are location tuples
    fd.close()



def runTest(whichBee = "testBee"):

    #whichBee = "testBee"

    running = True
    resultList = ["A", "B", "NO CHOICE"]  #will use for enumeration of choices
    endResult = "NO CHOICE"
    outputList = []
    locationList = []
    timing_a = False
    timing_b = False
    caps = [] #structure that will hold cap positions

    camera = cv2.VideoCapture(video_path)
    #camera = cv2.VideoCapture(1) #this is webcam

    firstFrame = None
    width = 800

    #Manually enter coords for solutions
    num_caps = 2 # number of caps in experiment
    cap_radius = 30

    sol_a_x = 100
    sol_a_y = 100
    sol_b_x = 100
    sol_b_y = 230

    distance_sol_a = 0
    distance_sol_b = 0

    startTime = time.time()     #start the timer to track experiment
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
        #frame = imutils.resize(frame, width=width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        ##### BOTTLE CAP DETECTION BEGINNING----- COMMENT OUT TO REMOVE AUTOMATIC CAP DETECTION
        if(len(caps) < num_caps):
            caps = detect_caps(frame)
            #print(caps)
            #print(len(caps))

        if(len(caps) == num_caps):
            #print(caps[0])
            sol_a_x = caps[0][0][0]
            sol_a_y = caps[0][0][1]

            sol_b_x = caps[1][0][0]
            sol_b_y = caps[1][0][1]
            cv2.circle(frame, (sol_a_x, sol_a_y), 1, (0, 255, 255), cap_radius)
            cv2.circle(frame, (sol_b_x, sol_b_y), 1, (130,0,75), cap_radius) #Solution A

        ##### BOTTLE CAP DETECTION END----- COMMENT OUT TO REMOVE AUTOMATIC CAP DETECTION

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        # remember to implement a case for when there are no cntrs. WHen the bee is not on camera
        for c in cnts:

            # if the contour is too small, ignore it
            if cv2.contourArea(c) > 1500 or cv2.contourArea(c) < 100:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            #center of rectangle. Rectangle
            rectagleCenterPont = ((x + x + w) // 2, (y + y + h) // 2)
            locationList += [((x + x + w) / 2.0, (y + y + h) / 2.0)]

            #calculate distance from bee to
            distance_sol_a = np.sqrt((sol_a_x - rectagleCenterPont[0])**2 + (sol_a_y - rectagleCenterPont[1])**2)
            distance_sol_b = np.sqrt((sol_b_x - rectagleCenterPont[0])**2 + (sol_b_y - rectagleCenterPont[1])**2)



            if(distance_sol_a < cap_radius):     #if bee is on sol_a cap, end experiment
                if(not timing_a):
                    print("near cap a")
                    start_cap_time = time.time()
                    #end_experiment(outputList, locationList, whichBee, "Purple", startTime, endtime)
                    #running = False
                    near_cap = "Yellow"
                    timing_a = True
                    #break
            else:
                #We have distance between bee and cap
                if(timing_a):
                    print("moved away from cap a")
                    #Bee moved away from cap. It didnt stay long enough to end experiment
                    timing_a = False
                    near_cap = "none"


            if(distance_sol_b < cap_radius):
                if(not timing_b):
                    print("near cap b")
                    start_cap_time = time.time()
                    #end_experiment(outputList, locationList, whichBee, "Yellow", startTime, endtime)
                    #running = False
                    near_cap = "Purple"
                    timing_b = True
                    #break
            else:
                #We have distance between bee and cap
                if(timing_b):
                    print("moved away from cap b")
                    #Bee moved away from cap. It didnt stay long enough to end experiment
                    timing_b = False
                    near_cap = "none"

            if(timing_a or timing_b):
                near_cap_time = time.time() - start_cap_time
                print(near_cap_time)
                if(near_cap_time > NEAR_CAP_TIME):
                    #print("wow")
                    print(near_cap_time)
                    #Finish experiment
                    endTime = time.time()
                    #end_experiment(outputList, locationList, whichBee, near_cap, startTime, endTime)
                    running = False
            #print("in main loop")

            if distance_sol_a < cap_radius:     #if bee is on sol_a cap, end experiment
                endtime = time.time()
                end_experiment(outputList, locationList, whichBee, "Purple", startTime, endtime)
                running = False
                break

            if distance_sol_b < cap_radius:
                endtime = time.time()
                end_experiment(outputList, locationList, whichBee, "Yellow", startTime, endtime)
                running = False
                break


            #DRAW CIRCLES FOR WHERE THE SOLUTIONS ARE
            #cv2.circle(frame, (sol_a_x, sol_a_y), 1, (0, 0, 255), 30) #Solution A
            #cv2.circle(frame, (sol_b_x, sol_b_y), 1, (0, 255, 0), 30) #Solution B

            #draw lines from bee to solutions
            cv2.line(frame, (sol_a_x, sol_a_y), rectagleCenterPont, (0, 255, 255), 2) #distance line A
            cv2.line(frame, (sol_b_x, sol_b_y), rectagleCenterPont, (130,0,75), 2) #distance line B

            #draw small circle where bee is
            cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)


        if(not running):
            break

        #Press q to exit early.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            endtime = time.time()

            end_experiment(outputList, locationList, whichBee, "NO RESULT - QUIT", startTime, endtime)
            break


        #Functions to display text on screen
        cv2.putText(frame, "Distance to Solution A: {}".format(str(distance_sol_a)), (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.putText(frame, "Distance to Solution B: {}".format(str(distance_sol_b)), (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        cv2.imshow("Security Feed", frame)

    #Quit camera displays
    endtime = time.time()

    #print("location List: ", locationList)
    end_experiment(outputList, locationList, whichBee, near_cap, startTime, endtime)

    end_experiment(outputList, locationList, whichBee, "NO RESULT - QUIT", startTime, endtime)


    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys

    EXPERIMENT_ID = 1
    runTest()
