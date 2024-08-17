import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import mediapipe as mp
import threading
import math
import cv2
import time
import configdata as configdata
from holosense import SpatialTracker
import numpy as np
from objloader import *

thisconf = configdata.config


hs_coords = (np.array((0,0,0)), np.array((0,0,0)), np.array((0,0,0)))
changed = 0

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


spatial_tracker = SpatialTracker(
    fov=78.5,
    aspectratio=16/9,
    eyedistance=4,
    eyenosedistance=3,
    single_output=False
    )

dilation = 1

cap = cv2.VideoCapture(thisconf.cameraname)
thisconf.configcamera(thisconf, cap)

dispw = thisconf.dispw
disph = thisconf.disph
screen_diagonal = thisconf.screen_diagonal # measurement is in inches
camera_y_offset = thisconf.camera_y_offset # vertical distance between the center of the screen and the center of the camera lens in inches
camera_x_offset = thisconf.camera_x_offset
camera_z_offset = thisconf.camera_z_offset
endist = thisconf.endist
eedist = thisconf.eedist




def camerastuff(): # VIDEO ANALYSIS - GETS FACIAL COORDINATES AND DOES SPICY MATH TO FIND SPATIAL POSITION OF POV
    global hs_coords
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
                hs_coords = spatial_tracker.calculatePosition(results.multi_face_landmarks[0])

                #print("detection")
            [e1x, e1y, e1z] = list((hs_coords[0] + hs_coords[1])/2)
            cv2.putText(image, "User Position: " + str(round(e1x, 3)) + "," + str(round(e1y, 3)) + "," + str(round(e1z, 3)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
            cv2.imshow('preview', image)
            cv2.waitKey(1)
            

ktranslation = [0,0,0]
verticies1 = (
    (-8, 5, 10),
    (8, 5, 10),
    (-8, -5, 10),
    (8, -5, 10),
    (-8, 5, 0),
    (8, 5, 0),
    (-8, -5, 0),
    (8, -5, 0)    
)

edges1 = (
    (0,1),
    (1,3),
    (0,2),
    (2,3),
    (4,5),
    (5,7),
    (4,6),
    (6,7),
    (0,4),
    (1,5),
    (2,6),
    (3,7)
    
)

def Cube():
    glBegin(GL_LINES)
    for edge in edges1:
        for vertex in edge:
            glColor3f(1, 0, 0)
            glVertex3fv(verticies1[vertex])


    glEnd()

def main():
    # viewport coordinates

    top = 0
    left = 0
    right = 3840
    bottom = 2400
    

    pygame.init()
    display = (dispw,disph)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    framenum = 0
    rotation = 0
    model = OBJ('katana/katana.obj')


    avgloc = model.avgarr
    max_scene_size = max([model.maxcoords[i] - model.mincoords[i] for i in range(3)])
    print(max_scene_size)
    object_length_irl = 12 # how long the object will appear, in inches.
    object_length_gamespace = max_scene_size # size in the game files.
    world2game = object_length_gamespace/object_length_irl
    monitor_height = screen_diagonal * disph / (dispw ** 2 + disph ** 2)**0.5
    monitor_width = screen_diagonal * dispw / (dispw ** 2 + disph ** 2)**0.5
    print("monitor width: " + str(monitor_width) + " inches.")
    thisloc = [0,0,20*world2game]
    pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=512) 
    sound0 = pygame.mixer.Sound('IVE_아이브_ AM_MV.mp3')
    channel = pygame.mixer.Channel(0)
    channel.play(sound0)

    while True:
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)       
        [e1x, e1y, e1z] = list((hs_coords[0] + hs_coords[1])/2)

        thisloc = [(e1x + camera_x_offset)*world2game , -(e1y + camera_y_offset)* world2game, (e1z + camera_z_offset) * world2game] # eye's position rel. to the screen's position
        # thisloc is relative to the dimension of the laptop scren - assuming it is 16 units wide and 9 units tall
        
        reloc = np.array([(hs_coords[0][0] + camera_x_offset)*world2game , -(hs_coords[0][1] + camera_y_offset)* world2game, (hs_coords[0][2] + camera_z_offset) * world2game])
        leloc = np.array([(hs_coords[1][0] + camera_x_offset)*world2game , -(hs_coords[1][1] + camera_y_offset)* world2game, (hs_coords[1][2] + camera_z_offset) * world2game])
        emitloc = np.array(avgloc)

        rsvec = emitloc - reloc
        rvvec = leloc - reloc

        r_int = (1 / (np.linalg.norm(rsvec) **2)) * 10 ** 5
        rsvec /= np.linalg.norm(rsvec)
        rvvec /= np.linalg.norm(rvvec)
        
        r_dotprod = (rsvec.dot(rvvec) + 1)/2
        r_int *= r_dotprod
        lsvec = emitloc - leloc
        lvvec = reloc - leloc


        l_int = (1 / (np.linalg.norm(lsvec) **2)) * 10 ** 5
        lsvec /= np.linalg.norm(lsvec)
        lvvec /= np.linalg.norm(lvvec)
        l_dotprod = (lsvec.dot(lvvec) + 1)/2
        l_int *= l_dotprod

        print(r_dotprod, l_dotprod)

        channel.set_volume(l_int, r_int)
        left = thisloc[0] - (monitor_width/2 * world2game)
        right = thisloc[0] + (monitor_width/2 * world2game)
        top = thisloc[1] + (monitor_height/2 * world2game)
        bottom = thisloc[1] - (monitor_height/2 * world2game)
        near = thisloc[2]
        try:
            glFrustum(left*0.1, right*0.1, bottom*0.1, top*0.1, near*0.1, 1000.0)
            glTranslatef(thisloc[0],thisloc[1],-thisloc[2])
                
            
            keypress = pygame.key.get_pressed()
            translation_mode = 0
            translated = 0
            if keypress[pygame.K_w]:
                ktranslation[2] -= 1
                translated = 1
            if keypress[pygame.K_s]:
                ktranslation[2] += 1
                translated = 1
            if keypress[pygame.K_d]:
                ktranslation[0] += 1
                translated = 1
            if keypress[pygame.K_a]:
                ktranslation[0] -= 1
                translated = 1
            if keypress[pygame.K_z]:
                ktranslation[1] -= 1
                translated = 1
            if keypress[pygame.K_x]:
                ktranslation[1] += 1
                translated = 1
            if keypress[pygame.K_j]:
                rotation += 0.1
                translated = 1
            if keypress[pygame.K_l]:
                rotation -= 0.1
                translated = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glRotate(rotation,0,1,0)
            glTranslate(ktranslation[0], ktranslation[1],ktranslation[2])        
            
            glPushMatrix()
            model.render()
            glPopMatrix()
        except:
            pass
        pygame.display.flip()
        pygame.time.wait(5)
    
th = threading.Thread(target=camerastuff)


th.start()

main()
