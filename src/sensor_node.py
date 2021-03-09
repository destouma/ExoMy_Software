#!/usr/bin/env python
import time
import rospy

import sensorBME280

sensor = sensorBME280()

def talker():
    rospy.init_node("sensor")
    rospy.loginfo("Starting the sensor node")

    temperature = rospy.Publisher('/temperature', float, queue_size=1)
    pressure = rospy.Publisher('/pressure', float, queue_size=1)
    humidity = rospy.Publisher('/humidity', float, queue_size=1)

    while not rospy.is_shutdown():
        val = sensor.getValue()
        rospy.loginfo("T="+val.temperature + " P="+val.pressure + " H="+val.humidity)
        temperature.publish(val.temperature)
        pressure.publish(val.pressure)
        humidity.publish(val.humidity)
        rospy.sleep(1.0)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
    