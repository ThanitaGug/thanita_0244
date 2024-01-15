#!/usr/bin/env python3
from tkinter import *
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_srvs.srv import Empty  # Import the Empty service from std_srvs package

rospy.init_node("Remote")

frame = Tk()
frame.title("REMOTE")
frame.geometry("200x300")

pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
sentpub = rospy.Publisher("ch1", String, queue_size=10)

def fw():
    cmd = Twist()
    cmd.linear.x = LinearVel.get()
    cmd.angular.z = 0.0
    pub.publish(cmd)
    sentpub.publish("FW")

def bw():
    cmd = Twist()
    cmd.linear.x = -LinearVel.get()
    cmd.angular.z = 0.0
    pub.publish(cmd)
    sentpub.publish("BW")

def lt():
    cmd = Twist()
    cmd.linear.x = LinearVel.get()
    cmd.angular.z = AngularVel.get()
    pub.publish(cmd)
    sentpub.publish("LT")

def rt():
    cmd = Twist()
    cmd.linear.x = LinearVel.get()
    cmd.angular.z = -AngularVel.get()
    pub.publish(cmd)
    sentpub.publish("RT")

LinearVel = Scale(frame, from_=0, to=2, orient=HORIZONTAL)
LinearVel.set(1)  # 1 is default value for scale
#LinearVel.pack()

AngularVel = Scale(frame, from_=0, to=2, orient=HORIZONTAL)
AngularVel.set(1)  # 1 is default value for scale
#AngularVel.pack()

B1 = Button(text="FW", command=fw)
B1.place(x=73, y=120)

B2 = Button(text="BW", command=bw)
B2.place(x=73, y=230)

B3 = Button(text="LT", command=lt)
B3.place(x=20, y=180)

B4 = Button(text="RT", command=rt)
B4.place(x=128, y=180)

frame.mainloop()