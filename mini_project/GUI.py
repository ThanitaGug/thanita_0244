#!/usr/bin/env python3
from tkinter import*
import rospy
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
# from std_srvs.srv import Empty
from sensor_msgs.msg import JointState

frame = Tk()
frame.title("REMOTE")
frame.geometry("550x500")
rospy.init_node("GUI_RP")
rate = rospy.Rate(10)
rate.sleep()

L1 = Label(frame,font = ('Arial',60),text ="00")
L1.place(x=120, y=100)

L2 = Label(frame,font = ('Arial',60),text ="00")
L2.place(x=310, y=100)

servo_read = 0
poten_read = 0

def readS1(num):
    servo_read = num.data 
    L1.config(text = str(servo_read))## รับข้อความ encoder
    print(servo_read)
sub= rospy.Subscriber("servo_angle", Int16,callback=readS1)

def readS2(num1):
    poten_read = num1.data 
    L2.config(text= str(poten_read))## รับข้อความ
    print(poten_read)
sub= rospy.Subscriber("poten_angle", Int16,callback=readS2)

# def send():
#     global servo_read
#     pubtorvid = rospy.Publisher('joint_states', JointState, queue_size=10)
#     rate = rospy.Rate(10)
#     msg = JointState()
#     msg.name = ['joint1']
#     msg.position = [servo_read]
#     pubtorvid.publish(msg)
#     rate.sleep()

    
def calPoAEntorvid(num2,num3):  
    global servo_read #encoder
    global poten_read

    num2 = poten_read
    poten = -(num2*0.002181)
    print("PotantialToRVID = ",poten)

    num3 = servo_read
    enco = (0.2722*num3)
    print("EncoderToRVID = ",enco)

    pubtorvid = rospy.Publisher('joint_states', JointState, queue_size=10)
    rate = rospy.Rate(10)
    msg = JointState()
    msg.name['joint1','joint2']
    msg.position[enco.get(),poten.get()]
    pubtorvid.publish(msg)
    rate.sleep()

    # pubtorvid = rospy.Publisher('joint_states', JointState, queue_size=10)
    # rate = rospy.Rate(10)
    # msg = JointState()
    # msg.name['joint1','joint2']
    # msg.position[0,0]
    # pubtorvid.publish(msg)
    # rate.sleep()

def ON():
    print("ON")
    cmd = Twist()
    cmd.linear.x = 1.0
    cmd.angular.z=0.0
    calPoAEntorvid()
    # pub.publish(cmd)

def OFF():
    print("OFF")
    cmd = Twist()
    cmd.linear.x = -1.0
    cmd.angular.z=0.0
    # pub.publish(cmd)

def Degree():
    print("degree")
    cmd = Twist()
    # cmd.linear.x = 1.0
    # cmd.angular.z= 1.0
    cmd.linear.y = 1.0
    cmd.angular.z= 1.0

    # pub.publish(cmd)

# def rs():
#     print("Reset")
#     rospy.wait_for_service('/reset')  # รอให้บริการ "reset" พร้อมใช้งาน
#     try:
#         reset_service = rospy.ServiceProxy('/reset', Empty)
#         response = reset_service()
#         rospy.loginfo("Reset Turtlesim Service Response: %s", response)
#     except rospy.ServiceException as e:
#         rospy.logerr("Service call failed: %s", e)




    
B1 = Button(text = "ON", command=ON)
B1.place(x=140, y=20)

B2 = Button(text = "OFF", command=OFF)
B2.place(x=330, y=20)

# B3 = Button(text = "", command=Degree)
# B3.place(x=140, y=250)

# B3 = Button(text = "DG", command=Degree)
# B3.place(x=140, y=250)

# B4 = Button(text = "SR", command=rt)
# B4.place(x=300, y=80)

# B5 = Button(text = "Rotate L", command=rtl)
# B5.place(x=90, y=80)

# B6 = Button(text = "Rotate R", command=rtr)
# B6.place(x=190, y=80)

# B7 = Button(text = "RESET", command=calPoAEntorvid)
# B7.place(x=380, y=130)


frame.mainloop()