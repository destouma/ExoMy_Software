#!/usr/bin/env python
import rospy
import time
from sensor_msgs.msg import Joy
from exomy_msgs.msg import Joystick
import math
import enum

global mode
global last
global counter

mode,counter = 0,0
last = time.time()


def callback(data):
	global mode
	global counter
	global last

	joy_out = Joystick()

	# Function map for the Logitech F710 joystick 
	# Button on pad | function
	# --------------|----------------------
	# LT			| decrease the max speed
	# LB			| increase the max speed
	# RT			| increase the angular velocity
	# RB			| decrease the angular velocity
	# B				| Toggle crabbing mode
	# X				| Toggle point turn mode
	# left stick	| control speed and direction

	y =  data.axes[1]
	x =  data.axes[0]

	dpad = data.buttons[11:]
	if 1 in dpad: mode = dpad.index(1)
	now = time.time()

	#cmd = two_joy(x,y,rt)
	joy_out.vel = 100 * y #cmd[0]
	joy_out.steering = -100 * x#cmd[1]
	joy_out.mode = mode
	joy_out.connected = True
	pub.publish(joy_out)

def old(x,y):
	if y < 0: direction = -1
	else: direction = 1

	r = int(100*math.sqrt(x*x + y*y)) * direction

	if r > 100: r = 100
	elif r < -100: r = -100

	if -15 <= r <= 15:
		r = 0
		theta = 0
	#there is some small issue where every once and a while the steering
	#goes to max negative for one or two values at very small values of y
	#this eventually needs to be fixed
	elif -0.01 <= y <= 0.01:
		theta = 100 * direction
	else:
		try:
			theta = int(math.degrees(math.atan(x/y)) * direction * (10/9.0))
		except:
			theta = 0
	return r,theta

def cartesian2polar_45(x,y):
	if y < 0: direction = -1
	else: direction = 1

	r = math.sqrt(x*x + y*y)
	r = min(r,1.0)
	try:
		theta = math.degrees(math.atan2(x,y))
	except:
		if x >0: theta = 90
		else: theta = -90
	if (-45 <= theta <= 45) or (135 <=theta <= 180) or (-180 <=theta <= -135):
		vel = int(r * 100) * direction
	else:
		vel = (2.0/math.sqrt(2))*y*100
	vel = min(100,vel)
	vel = max(-100,vel)

	'''
	if y >= 0:
		steering = theta * 10/9.0
	else:
		if x >= 0: x_dir = 1
		else: x_dir = -1
		steering = (180 - abs(theta)) * (10/9.0) * x_dir
	'''
	steering = x * 2.0/math.sqrt(2) * 100
	steering = min(100,steering)
	steering = max(-100,steering)
	return (int(vel),int(steering))

def two_joy(x,y,rt):
	"""
	boost = 0
	if rt <= 0:
		boost = 50*-rt
	if y >=0: y = (y * 50) + boost
	else: y = (y *50) - boost
	x *= 100
	"""
	#x *=100
	#y *=
	return (int(y),int(x))

if __name__ == '__main__':
	global pub

	rospy.init_node('joystick')
	rospy.loginfo('joystick started')

	sub = rospy.Subscriber("/joy", Joy, callback)
	pub = rospy.Publisher('joystick', Joystick, queue_size=1)

	rospy.spin()

