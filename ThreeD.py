#SEcond version eeq
#sep 26 added cap detectiong

import argparse
import datetime
import imutils
import math
import cv2
import numpy as np



def convert_sphere_2_cartesian(theta_angle, phi_angle, rho_length):
    theta_angle   = np.radians(theta_angle)
    phi_angle     = np.radians(phi_angle)

    #Convert these into cartesian vector pointing from origin (ball) to camera
    x = rho_length*np.sin(phi_angle)  *np.cos(theta_angle)
    y = rho_length*np.sin(phi_angle)  *np.sin(theta_angle)
    z = rho_length*np.cos(phi_angle)
    return np.array([y,z,x]) # mixed because of perspective.


class Camera:
    '''
    calibrating_area: in cm
    '''
    def __init__(self, camera_feed, calibrating_area, camera_coords, camera_type):
        self.ball_origin_x = 0
        self.ball_origin_y = 0

        self.bee_position = [0,0,0]
        self.area = 0
        self.camera = camera_feed
        self.calibrating_area = calibrating_area
        self.camera_coords = camera_coords
        self.camera_type = camera_type
        self.prev_frame = None
        self.curr_frame = None

         #This will be the width that cv uses for all image operations
        #The larger the width the more precision -> higher resolution. But it also
        #is computationally more expensive since there is more pixels -> more data
        self.width = 500
        self.observed_rad = 0

        #specific things to camera model:
        self.aspect_ratio = 16.0 / 9.0
        self.view_angle = 78 # this is the horizontal Angle of View.

        self.focal_length = 0 # this is set using computer vision and a known distance

        #calculate degree confersions
        self.height = self.width / self.aspect_ratio # 1.77 is the aspect ratio = 16 / 9
        self.degree_conversion = self.width / self.view_angle #I see this as "pixels per degree" may not be reliable


        #data specific to experiment setup
        self.known_length   = 3.7   #radius of pingpong ball
        self.known_distance = None
        self.bee_size = 1.27
        self.focal_length_b = 448.74
        #self.camera_position_vector = None
        self.over_estimate = 4 * 24.13


        if(camera_type == "side_a"):
            #self.known_distance = 39.05 #distance from ball to camera
            self.known_distance = 35.96
            self.camera_position_vector = [0,-26.67,24.13]
            self.camera_shift = np.degrees(np.arctan(abs(self.camera_position_vector[2]) / abs(self.camera_position_vector[1])))
            self.camera_vector_multiplier = np.array([1,1,-1]) #inverts axis

        if(camera_type == "side_b"):
            #self.known_distance = 39.05
            #self.camera_position_vector = [0,30,25]
            self.known_distance = 35.96
            self.camera_position_vector = [0,26.67,24.13]
            self.camera_vector_multiplier = [-1,-1,-1] #inverts axis
            self.camera_shift = np.degrees(np.arctan(abs(self.camera_position_vector[2]) / abs(self.camera_position_vector[1])))


        if(camera_type == "top"):
            self.known_distance = 68
            self.camera_position_vector = [0,0,68]
            self.camera_shift = 0 #needs to be set
            self.camera_vector_multiplier = [-1,-1,-1] #inverts axis


    def get_theta_phi_rho_new(self, x_observed, y_observed):
        '''
            get theta and phi from observed x and y and from origin set at ball
            The rho returned is an overestimate since we only care about the position of the
            spherical vector NOT the length of it.
        '''

        ## Center coordinates making 0,0 be at the center of the ball instead of the upper
        ## corner
        x_normalized = (x_observed        - self.ball_origin_x)
        y_normalized = (y_observed        - self.ball_origin_y) # 50 is distance due to windows
                                                              #
        #print(x_normalized)
        #print(y_normalized)
        phi   = (y_normalized / self.degree_conversion + self.camera_shift)
        theta = (x_normalized / self.degree_conversion )


        #print("heyy")
        #print(known_length)
        #print(length_observed)
        #print(self.focal_length_b)

        rho = self.over_estimate #(known_length * self.focal_length_b) / length_observed  #D’ = (W x F) / P

        return (theta, phi, rho)



    def get_pos_vector(self, x_observed, y_observed):
        #Get cartesian vector of obeserved x y corrds and observed length

        (theta, phi, rho) = self.get_theta_phi_rho_new(x_observed,y_observed)

        #print("Test theta (should be near zero): "+str(theta))
        #print("Test phi (should be near zero): "+str(phi))
        #print("Test rho (should be the same as overestimate): "+str(rho))

        vector_cartesian = convert_sphere_2_cartesian(theta, phi, rho)
        return vector_cartesian *  self.camera_vector_multiplier


    def calibrate_origin_manual(self, camera_calibrate, coords = None):
        '''
        Find calibrating object in frame and set the percieved 3d coords
        as the origin. This way all cameras agree on that point.

        Notes:
           -This temporary solution uses user mouse clicks to calibrate cameras
        '''

        if(coords is not None):
            coords_center = coords[0]
            coords_radius = coords[1]
        else:

            #mouse = PyMouse()

            pass


        self.ball_origin_x = coords_center[0]
        self.ball_origin_y = coords_center[1]

        self.observed_rad = np.sqrt((coords_center[0]-coords_radius[0])**2 + (coords_center[1]-coords_radius[1])**2 )


        vector_cartesian = self.get_pos_vector(coords_center[0],coords_center[1])


        #Get first frame for frame difference
        (grabbed, frame) = camera_calibrate.read()
        if grabbed:
            frame = imutils.resize(frame, width=self.width)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (11, 11), 0)
            self.prev_frame = gray



    def reset_frame(self):
        (grabbed, frame) = self.camera.read()
        if grabbed:
            frame = imutils.resize(frame, width=self.width)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (11, 11), 0)
            self.prev_frame = gray
    def get_bee_coords(self):
        '''
        return x and y of bee in camera vision
        '''
        (grabbed, frame) = self.camera.read()

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not (grabbed and (self.prev_frame is not None)):
            #error
            print("Didnt have frames available to get frame difference")
            #break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=self.width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(self.prev_frame, gray)
        thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]

        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        vector_cartesian = None
        coords = None
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) > 1500 or cv2.contourArea(c) < 50:
                print("Warning: contour has been ignored since it was not in the correct range")
                continue

            # compute the bounding box for the contour, draw it on the frame,
            (x, y, w, h) = cv2.boundingRect(c)
            coords = [x,y]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.curr_frame = frame

        return coords

    def update_bee_position(self):
        ####______FIRST get camera perspective position of bee


        (grabbed, frame) = self.camera.read()

        #get fps of camera
        fps = self.camera.get(cv2.CAP_PROP_FPS)
        #capture.set(CV_CAP_PROP_FPS , 30);
        #print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
        #NOTE: fps changes based on recording settings and really affects cod


        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not (grabbed and (self.prev_frame is not None)):
            #error
            print("Didnt have frames available to get frame difference")
            #break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=self.width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)

        # compute the absolute difference between the current frame and
        # first frame

        frameDelta = cv2.absdiff(self.prev_frame, gray)

        thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        #   qthresh = cv2.dilate(thresh, None, iterations=2)
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        vector_cartesian = None
        cv2.circle(frame, (int(self.ball_origin_x)-2, int(self.ball_origin_y)-48), 1, (0, 0, 255), 3)
        cv2.circle(frame, (int(self.ball_origin_x)-2, int(self.ball_origin_y)-48), int(self.observed_rad), (0, 0, 255), 2)


        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) > 600 or cv2.contourArea(c) < 20:
                #print("Warning: contour has been ignored since it was not in the correct range")
                continue

            # compute the bounding box for the contour, draw it on the frame,
            (x, y, w, h) = cv2.boundingRect(c)


            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.imshow("Video Feed", thresh)

        ####Convert camera perspective position of bee to normalized coords
        #print(self.ball_origin_y)

        if(vector_cartesian is not None):
            self.bee_position = vector_cartesian + self.camera_position_vector
        #cv2.imshow("Security Feed", frame)
        return(frame, self.bee_position)


    def get_bee_position(self):
        return self.bee_position


def experiment_3d():
    camera_side_a = Camera(cv2.VideoCapture("videos/vid_1_a.mp4"),3.7,[1,2,3],"side_a")#
    camera_side_b = Camera(cv2.VideoCapture("videos/vid_1_b.mp4"),3.7,[1,2,3],"side_b")
    camera_top = Camera(cv2.VideoCapture("videos/vid_1_top.mp4"),3.7,[1,2,3],"top")

    camera_side_a.calibrate_origin_manual(cv2.VideoCapture("videos/vid_1_a.mp4"), coords = [(250.75, 289.83203125),(270.2890625, 288.5546875)])
    camera_side_b.calibrate_origin_manual(cv2.VideoCapture("videos/vid_1_b.mp4"), coords = [(254.24609375, 277.51953125),(274.60546875, 278.7734375)])
    camera_top.calibrate_origin_manual(cv2.VideoCapture("videos/vid_1_top.mp4"), coords = [(253.83203125, 287.27734375),(263.19921875, 286.43359375)])

    #Skip frames to sync
    for i in range(100):
        (grabbed, frame) = camera_side_a.camera.read()

    for i in range(135):
        (grabbed, frame) = camera_side_b.camera.read()

    for i in range(142):
        (grabbed, frame) = camera_top.camera.read()

    iter = 0
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        iter += 1
        if(iter == 30):
            camera_top.reset_frame()

        if(iter == 300):
            break
        camera_side_a.camera.read()
        camera_side_b.camera.read()
        camera_top.camera.read()

        (frame_side_a, pos_side_a) = camera_side_a.update_bee_position()
        (frame_side_b, pos_side_b) = camera_side_b.update_bee_position()
        (frame_top, pos_side_b) = camera_top.update_bee_position()

        numpy_vertical = np.vstack((frame_side_a, frame_side_b, frame_top))

        cv2.imshow("Security Feed", numpy_vertical)
