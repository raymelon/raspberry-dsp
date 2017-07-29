import numpy as np
import cv2


def get_shape(image):
    ''' Recognizes shape in an image and arrow(if it's an arrow) orientation.
        Returns what the shape means(which state the vehicle should behave
        based on the signs).
    '''
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (_, thresh) = cv2.threshold(gray, 127, 255, 1)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts:
        state = ''

        # Approximately gets number of points in each contours.
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        rect = cv2.minAreaRect(cnt)
        box = np.int0(cv2.boxPoints(rect))
        if len(approx) == 7:
            (x, y), (MA, ma), angle = cv2.fitEllipse(cnt)

            if angle >= 90:
                state = 'RIGHT'
            else:
                state = 'LEFT'
        elif len(approx) == 4:
            state = 'DEAD'

        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        cv2.putText(image, state, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2)

        return state, image


TEST = False 
if TEST:
    state, image = get_shape('../img/right.jpg')
    cv2.imshow(state, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
