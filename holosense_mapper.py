
import mediapipe as mp
import math
import cv2
import time
import configdata
import struct
from multiprocessing import shared_memory

thisconf = configdata.config
shm = shared_memory.SharedMemory(name = "holosenseData", create=True, size=24) # 3 floats of shared memory
buffer = shm.buf


e1x = 0
e1y = 0
e1z = 0
changed = 0

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

dilation = 1

camw = thisconf.camw
camh = thisconf.camh
HFOV = thisconf.HFOV * math.pi / 180
VFOV = thisconf.VFOV * math.pi / 180
htan = - math.tan(HFOV/2)
vtan =  math.tan(VFOV/2)

dispw = thisconf.dispw
disph = thisconf.disph
screen_diagonal = thisconf.screen_diagonal # measurement is in inches
camera_y_offset = thisconf.camera_y_offset # vertical distance between the center of the screen and the center of the camera lens in inches
camera_x_offset = thisconf.camera_x_offset
camera_z_offset = thisconf.camera_z_offset
endist = thisconf.endist
eedist = thisconf.eedist

cap = cv2.VideoCapture(thisconf.cameraname)
thisconf.configcamera(thisconf, cap)
inference_interval = thisconf.inference_interval
lfp = thisconf.log_file
logs = []
starttime = round(time.time() * 1000)



numinf = 0
def eval_func(a, consts):
    [c1, c2, c3, c4, c5, c6] = consts
    bp = func_b(c1, c2, a)
    cp = func_b(c3, c4, a)
    return [(bp**2 + cp**2) - (2*cp*bp*c5) - (c6)**2, bp, cp]
def func_b(c1, c2, a):
    return ((2*a*c1) + ((2*a*c1) ** 2 + 4*(c2 **2 - a**2))**0.5) / 2
def nr_approx(first, last, step, consts):
    zeroes = []
    [zfirst, bd, cd] = eval_func(first, consts)
    for j in range(int((last - first) / step)):
        a = (j * step) + first
        [ff, bd,cd] = eval_func(a, consts)
        try:
            zz = int(ff)
        except:
            ff = zfirst * -1
        if ff > 0 and zfirst < 0 or ff < 0 and zfirst > 0:
            return [a, bd.real, cd.real]
        
lex = 0
ley = 0
rex = 0
rey = 0
nx = 0
ny = 0
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
            #print("detection")

            
            for face_landmarks in results.multi_face_landmarks:
                #print(face_landmarks)
                xcoords = [handmark.x for handmark in face_landmarks.landmark]
                ycoords = [handmark.y for handmark in face_landmarks.landmark]
                
                
                rex = (xcoords[33] * camw)
                rey = (ycoords[33] * camh)
                
                lex = (xcoords[263] * camw)
                ley = (ycoords[263] * camh)

                nx = (xcoords[19] * camw)
                ny = (ycoords[19] * camh)
                cv2.circle(image, (int(rex), int(rey)), 3, (255, 0, 0), -1)
                cv2.circle(image, (int(lex), int(ley)), 3, (255, 0, 0), -1)
                cv2.circle(image, (int(nx), int(ny)), 3, (255, 0, 0), -1)

        
        e1h = htan * ((camw/2) - rex)/(camw/2) 
        e1v = vtan * ((camh/2) - rey)/(camh/2)
        e2h = htan * ((camw/2) - lex)/(camw/2)
        e2v = vtan * ((camh/2) - ley)/(camh/2)
        nh = htan * ((camw/2) - nx)/(camw/2)
        nv = vtan * ((camh/2) - ny)/(camh/2)
        # angle cosine calculation by dot products 
        eec = ((e1h * e2h) + (e1v * e2v) + 1) / (((e1h ** 2 + e1v ** 2 + 1) ** 0.5) * ((e2h ** 2 + e2v ** 2 + 1) ** 0.5))
        en1 = ((e1h * nh) + (e1v * nv) + 1) / (((e1h ** 2 + e1v ** 2 + 1) ** 0.5) * ((nh ** 2 + nv ** 2 + 1) ** 0.5))
        en2 = ((e2h * nh) + (e2v * nv) + 1) / (((e2h ** 2 + e2v ** 2 + 1) ** 0.5) * ((nh ** 2 + nv ** 2 + 1) ** 0.5))
        #print("distance approximation")
        try:
            [nd1, led, red] = nr_approx(0,90,1,[en2, endist, en1, endist, eec, eedist])
            [nd, led, red] = nr_approx(nd1-1,nd1,0.01,[en2, endist, en1, endist, eec, eedist])
            #print("success")
            rer = (red / ((e1h ** 2 + e1v ** 2 + 1)**0.5))
            ler = (led / ((e2h ** 2 + e2v ** 2 + 1)**0.5))
            prc = [(e1h * rer + e2h * ler)/2 + camera_x_offset, (e1v * rer + e2v * ler)/2 + camera_y_offset, (ler + rer)/2 + camera_z_offset]           
            for iter1, valuezz in enumerate(prc):

                struct.pack_into('d', buffer, iter1 * 8, valuezz)
        except:
            pass
        cv2.putText(image, "User Position: " + str(round(prc[0], 3)) + "," + str(round(prc[1], 3)) + "," + str(round(prc[2], 3)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
        cv2.imshow('preview', image)
        cv2.waitKey(1)
            
