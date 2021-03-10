#!/usr/bin/env python
import time
import rospy
from std_msgs.msg import String
import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

def talker():
    calibration_params = bme280.load_calibration_params(bus, address)

    rospy.init_node("sensor")
    rospy.loginfo("Starting the sensor node")

    temperature = rospy.Publisher('/temperature', String, queue_size=1)
    pressure = rospy.Publisher('/pressure', String, queue_size=1)
    humidity = rospy.Publisher('/humidity', String, queue_size=1)

    while not rospy.is_shutdown():
        val = bme280.sample(bus, address, calibration_params)
        rospy.loginfo("T="+str(val.temperature) + " P="+ str(val.pressure) + " H="+ str(val.humidity))
        # temperature.publish(str(val.temperature))
        # pressure.publish(str(val.pressure))
        # humidity.publish(str(val.humidity))
        temperature.publish(f'{val.temperature:.2f }')
        pressure.publish(f'{val.pressure:.2f }')
        humidity.publish(f'{val.humidity:.2f }')
        rospy.sleep(1.0)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
    