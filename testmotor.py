import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

motor_right_A = 23
motor_right_B = 21
motor_right_E = 19

motor_left_A = 16
motor_left_B = 18
motor_left_E = 22

GPIO.setup(motor_right_A, GPIO.OUT)
GPIO.setup(motor_right_B, GPIO.OUT)
GPIO.setup(motor_right_E, GPIO.OUT)

GPIO.setup(motor_left_A, GPIO.OUT)
GPIO.setup(motor_left_B, GPIO.OUT)
GPIO.setup(motor_left_E, GPIO.OUT)

def forward(duration):
	print "Forwarding..."
	GPIO.output(motor_right_E, GPIO.LOW)
	GPIO.output(motor_right_B, GPIO.HIGH)
	GPIO.output(motor_right_A, GPIO.HIGH)
	
	GPIO.output(motor_left_A, GPIO.LOW)
	GPIO.output(motor_left_B, GPIO.HIGH)
	GPIO.output(motor_left_E, GPIO.HIGH)
	sleep(duration)
	
def face_right(duration):
	print "Facing right..."
	GPIO.output(motor_right_A, GPIO.LOW)
	GPIO.output(motor_right_B, GPIO.HIGH)
	GPIO.output(motor_right_E, GPIO.HIGH)
	
	GPIO.output(motor_left_A, GPIO.LOW)
	GPIO.output(motor_left_B, GPIO.HIGH)
	GPIO.output(motor_left_E, GPIO.HIGH)
	sleep(duration)
	
def face_left(duration):
	print "Facing left..."
	GPIO.output(motor_right_E, GPIO.LOW)
	GPIO.output(motor_right_B, GPIO.HIGH)
	GPIO.output(motor_right_A, GPIO.HIGH)
	sleep(duration)
	
def backward(duration):
	print "Backwarding..."
	GPIO.output(motor_left_A, GPIO.HIGH)
	GPIO.output(motor_left_B, GPIO.LOW)
	GPIO.output(motor_left_E, GPIO.HIGH)
	
	GPIO.output(motor_right_A, GPIO.HIGH)
	GPIO.output(motor_right_B, GPIO.LOW)
	GPIO.output(motor_right_E, GPIO.HIGH)
	sleep(duration)

backward(2)

print "Stopping..."
GPIO.output(motor_right_E, GPIO.LOW)
GPIO.output(motor_left_E, GPIO.LOW)

GPIO.cleanup()
