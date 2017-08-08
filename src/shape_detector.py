import numpy as np
import cv2
import imutils


def get_shape(image):
    ''' Recognizes shape in an image and arrow(if it's an arrow) orientation.
        Returns what the shape means(which state the vehicle should behave
        based on the signs).
    '''
    
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])

    # Puts filters on image
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)
    edged = cv2.Canny(thresh, 35, 125)
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST,
               cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)

    state = ''
    
    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
    else:
        cX, cY = 0, 0

    #print M
    approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
    # print("POINTS", len(approx))
    if len(approx) in range(7, 20):
        if M["nu12"] > 0:
            state = 'RIGHT'
        else:
            state = 'LEFT'
    elif len(approx) == 4:
        state = 'DEAD'

    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, state, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (255, 255, 255), 2)

    return state, image


if __name__ == '__main__':
    state, image = get_shape(cv2.imread('../img/tmp.jpg'))
    print state
    cv2.imshow(state, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
