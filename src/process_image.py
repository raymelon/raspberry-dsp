import distance_finder as df
import shape_detector as sd
import time
import os

# Distance of the car to the arrow when stopping.
DISTANCE_THRESHOLD = 9.0 

# Loads focal length callibrated value.
if os.path.exists('.focal_length'):
    focal_length = float(open(".focal_length", "r").read())
else:
    focal_length = df.callibrate_camera()


while True:
    # The car captures photos while running... Implement a thread, maybe? 
    os.system('fswebcam -r 640x768 -S 5 --jpeg 95 --no-banner --save ../img/tmp.jpg')
    time.sleep(0.15)
    
    tmp_img = '../img/tmp.jpg'
    current_distance = df.get_distance(tmp_img, focal_length)[0]

    break
    if current_distance <= 9:
        # The car stops.
        state = sd.get_shape(tmp_img)
        # The car will take action based on the "state":
        #   DEAD - LEFT - RIGHT


