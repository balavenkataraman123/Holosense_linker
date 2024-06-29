
import mediapipe as mp
import cv2
import time
import struct
from multiprocessing import shared_memory
from holosense import SpatialTracker
import configdata

thisconf = configdata.config
cap = cv2.VideoCapture(thisconf.cameraname)
thisconf.configcamera(thisconf, cap)

conf_shm = shared_memory.SharedMemory(name = "holosenseConfig", create=True, size=32) 
shm = shared_memory.SharedMemory(name = "holosenseData", create=True, size=32) # 4 floats of shared memory
buffer = shm.buf


e1x = 0
e1y = 0
e1z = 0
changed = 0

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

camw = thisconf.camw
camh = thisconf.camh
fov = thisconf.fov
dispw = thisconf.dispw
disph = thisconf.disph
screen_diagonal = thisconf.screen_diagonal # measurement is in inches
camera_y_offset = thisconf.camera_y_offset # vertical distance between the center of the screen and the center of the camera lens in inches
camera_x_offset = thisconf.camera_x_offset
camera_z_offset = thisconf.camera_z_offset
endist = thisconf.endist
eedist = thisconf.eedist


spatial_tracker = SpatialTracker(
    fov=fov,
    aspectratio=camw/camh,
    eyedistance=eedist,
    eyenosedistance=endist)

starttime = round(time.time() * 1000)


with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
    while True:
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            prc = list(spatial_tracker.calculatePosition(face_landmarks))
            prc.append(time.time())
            print(prc)
            cv2.putText(image, "User Position: " + str(round(prc[0], 3)) + "," + str(round(prc[1], 3)) + "," + str(round(prc[2], 3)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))     
            for iter1, valuezz in enumerate(prc):
                struct.pack_into('d', buffer, iter1 * 8, valuezz)
       
        cv2.imshow('preview', image)
        cv2.waitKey(1)
            
