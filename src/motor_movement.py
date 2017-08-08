import RPi.GPIO as GPIO
from time import sleep

class Motor:
    ''' Motor Class -- contains functions to determine motor's movements. '''

    def __init__(self):
        self.motor_right_A = 19
        self.motor_right_B = 21
        self.motor_right_E = 23

        self.motor_left_A = 16
        self.motor_left_B = 18
        self.motor_left_E = 22
    

    def setup_board(self):
        print "Setting up the board and pins..."
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.motor_right_A, GPIO.OUT)
        GPIO.setup(self.motor_right_B, GPIO.OUT)
        GPIO.setup(self.motor_right_E, GPIO.OUT)

        GPIO.setup(self.motor_left_A, GPIO.OUT)
        GPIO.setup(self.motor_left_B, GPIO.OUT)
        GPIO.setup(self.motor_left_E, GPIO.OUT)

        self.pwm_right = GPIO.PWM(self.motor_right_E, 100)
        self.pwm_left = GPIO.PWM(self.motor_left_E, 100)
    
        # Starts motor at 40% usage of power
        self.pwm_right.start(40)
        self.pwm_left.start(40)
        

    def run_until(self, duration):
        if duration == 0:
            sleep(999)
        else:  
            sleep(duration)
        
        self.stopping()


    def forward(self, duration=0):
        print "Forwarding..."
        self.setup_board()
        GPIO.output(self.motor_right_A, GPIO.LOW)
        GPIO.output(self.motor_right_B, GPIO.HIGH)
        GPIO.output(self.motor_right_E, GPIO.HIGH)
        
        GPIO.output(self.motor_left_A, GPIO.LOW)
        GPIO.output(self.motor_left_B, GPIO.HIGH)
        GPIO.output(self.motor_left_E, GPIO.HIGH)
        self.run_until(duration)  


    def face_right(self, duration=0):
        print "Facing right..."
        self.setup_board()
        GPIO.output(self.motor_right_A, GPIO.LOW)
        GPIO.output(self.motor_right_B, GPIO.LOW)
        GPIO.output(self.motor_right_E, GPIO.LOW)

        GPIO.output(self.motor_left_A, GPIO.LOW)
        GPIO.output(self.motor_left_B, GPIO.HIGH)
        GPIO.output(self.motor_left_E, GPIO.HIGH)
        self.run_until(duration)


    def face_left(self, duration=0):
        print "Facing left..."
        self.setup_board()
        GPIO.output(self.motor_right_A, GPIO.LOW)
        GPIO.output(self.motor_right_B, GPIO.HIGH)
        GPIO.output(self.motor_right_E, GPIO.HIGH)

        GPIO.output(self.motor_left_A, GPIO.LOW)
        GPIO.output(self.motor_left_B, GPIO.LOW)
        GPIO.output(self.motor_left_E, GPIO.LOW)
        self.run_until(duration)
            

    def backward(self, duration=0):
        print "Backwarding..."
        self.setup_board()
        GPIO.output(self.motor_right_A, GPIO.HIGH)
        GPIO.output(self.motor_right_B, GPIO.LOW)
        GPIO.output(self.motor_right_E, GPIO.HIGH)

        GPIO.output(self.motor_left_A, GPIO.HIGH)
        GPIO.output(self.motor_left_B, GPIO.LOW)
        GPIO.output(self.motor_left_E, GPIO.HIGH)
        self.run_until(duration)


    def stopping(self):
        print "Stopping..."
        GPIO.output(self.motor_right_E, GPIO.LOW)
        GPIO.output(self.motor_left_E, GPIO.LOW)
        self.pwm_right.start(50)
        self.pwm_left.start(50)
        GPIO.cleanup()


if __name__ == '__main__':
    m = Motor()
    m.forward(1)
#    m.face_left(0.7)
#    m.backward(1.5)
#    m.face_right(0.75)
