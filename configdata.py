import cv2
import os
import math
class config: # configurations for the camera, display, and user
    
    # Default configurations.
    # Currently configured for display and webcam of Dell Precision 5570 Mobile Workstation

    # Camera ID and resolution
    cameraname = "/dev/video4"
    camw = 1920
    camh = 1080
    fov = 80
    # Display resolution.
    dispw = 3840 
    disph = 2400 
    # Measurements of real world space. All are in inches.
    screen_diagonal = 15.6 #in inches
    camera_y_offset = 4.25 # vertical distance between the center of the screen and the lens of the webcam.
    camera_x_offset = 0 # horizontal distance parallel to screen
    camera_z_offset = 0 # horizontal distance normal to screen

    # Measurements of your face. See reference image for details.
    eedist = 4
    endist = 3

    def configcamera(self, cap):
       
        cap.set(cv2.CAP_PROP_FPS, 60)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camw)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camh)
        ret_val, frame = cap.read()
        #print(cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0))
        #print(cap.set(cv2.CAP_PROP_EXPOSURE , 0))        
    
    # DATA LOGGING
    
    
