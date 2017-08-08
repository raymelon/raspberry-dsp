from multiprocessing import Process
import distance_finder as df
import shape_detector as sd
import motor_movement as mm
import numpy as np

import cv2
import time
import os

# Motor movement instance
motor = mm.Motor()

# Distance of the car to the arrow when stopping.
DISTANCE_THRESHOLD = 8.0 

# Loads focal length callibrated value.
if os.path.exists('.focal_length'):
    focal_length = float(open(".focal_length", "r").read())
else:
    focal_length = df.callibrate_camera()

cap = cv2.VideoCapture(0)
skip_frames = 5 # For better lighting

def get_frame():
    ret, frame = cap.read()
    return frame

def process_image():
    
    # Skips frames for better image lighting
    print "Skipping frames:", skip_frames
    for i in xrange(skip_frames):
        temp = get_frame()
    
    frame = get_frame()
    print "Frame captured!"

    cv2.imwrite("../img/tmp.jpg", frame)
    
    current_distance = df.get_distance(frame, focal_length)[0]
    print "Current Distance:", current_distance
        
    if current_distance <= DISTANCE_THRESHOLD:
        #cv2.imwrite("../img/tmp.jpg", frame)
        #print "Writing to ../img/tmp.jpg..."
        print "Threshold -", DISTANCE_THRESHOLD, "reached!"
        return frame, False, current_distance
    else:
        return frame, True, current_distance
    
        # The car stops.
    #    state = sd.get_shape(tmp_img)
        # The car will take action based on the "state":
        #   DEAD - LEFT - RIGHT
    #    print 'state: ' + state
        
    #    if state == 'LEFT':
    #        face_left(1.2)
    #        forward(2)
                        
    #    elif state == 'RIGHT':
    #        face_right(1.2)
    #        forward(2)

    #    else:
    #        break


def get_direction(frame):
    state, _ = sd.get_shape(frame)
    print 'State -', state
    if state == 'LEFT':
        print "Turning left..."
        motor.face_left(0.7)
        return True
    elif state == 'RIGHT':
        print "Turning right..."
        motor.face_right(0.7)
        return True
    else:
        return False


def move_car():
    motor.forward()

def process_car_movement():
    ret_val = True
    print "Starting motor movement process..."
    while ret_val:
        movement_process = Process(target=move_car)
        movement_process.start()
        frame, state, distance = process_image()
        while state:
            frame, state, distance = process_image()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print "Terminating motor movement process..."
        movement_process.terminate()
        ret_val = get_direction(frame)
        motor.forward(0.1)
    
    cap.release()
    return ret_val
        
        

if __name__ == '__main__':
    process_car_movement()
