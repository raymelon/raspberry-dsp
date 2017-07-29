import numpy as np
import cv2


def find_marker(image):
    ''' Converts image to grayscale, blur it, detects edges, thresholds and
        innverts.
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)
    edged = cv2.Canny(thresh, 35, 125)

    # Finds the contours in the edged image and keeps the largest one.
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)

    # Computes the bounding box of the "paper" region and return it.
    return cv2.minAreaRect(c)


def get_distance_to_camera(known_width, focal_length, per_width):
    ''' Computes and returns the distance from the marker(arrow) to the camera.
    '''
    return (known_width * focal_length) / per_width


def get_distance(image, focal_length, callibrate=False):
    ''' Finds marker and returns the distance between the camera and the marker.
    '''
    image = cv2.imread(image_path)
    marker = find_marker(image)

    return get_distance_to_camera(KNOWN_WIDTH, focal_length, marker[1][0]), image, marker


def callibrate_camera():
    ''' Callibrates camera to initialize focal length. '''
    image = cv2.imread('../img/calib1.jpg')
    marker = find_marker(image)
    focal_length = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
    config = open(".focal_length", "w")
    config.write(str(focal_length))
    config.close()

    return focal_length


# Initialized value of distance from the marker(arrow) to the camera; in inches.
KNOWN_DISTANCE = 9.0

# Initialized value of the width of the marker(arrow); in inches.
KNOWN_WIDTH = 3.0

TEST = False

# Loads test image.
if TEST:
    import os.path

    IMAGES = ["../img/calib1.jpg", "../img/calib2.jpg", "../img/calib3.jpg"]

    if not os.path.exists(".focal_length"):
        image = cv2.imread(IMAGES[0])
        marker = find_marker(image)
        focal_length = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
        config = open(".focal_length", "w")
        config.write(str(focal_length))
        config.close()
    else:
        focal_length = float(open(".focal_length", "r").read())

    for image_path in IMAGES:
        inches, image, marker = get_distance(image_path, focal_length)

        # Draws a bounding box around the marker and display it.
        box = np.int0(cv2.boxPoints(marker))
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        cv2.putText(image, "%.2fin" % inches,
                (image.shape[1] - 200, image.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 255, 0), 3)
        cv2.imshow("image", image)
        cv2.waitKey(0)
