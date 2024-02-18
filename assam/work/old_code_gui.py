#!/usr/bin/env python3
import customtkinter,tkinter
from tkinter import*
import rospy
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
# from std_srvs.srv import Empty
# from sensor_msgs.msg import JointState
# import tf
# import threading

# pub = rospy.Publisher("encoder_pub", Int16,queue_size=10)
# pub_poten = rospy.Publisher("poten_pub", Int16,queue_size=10)

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

L3 = Label(frame,font = ('Arial',60),text ="00")
L3.place(x=310, y=300)

# servo_read = None
# poten_read = None

def readS1(num):
    servo_read = num.data 
    L1.config(text = str(servo_read))## รับข้อความ encoder
    print(servo_read)
    encoder = -(servo_read*0.002181)
    # pub.publish(encoder)

sub = rospy.Subscriber("servo_angle", Int16,callback=readS1)

def readS2(num1):
    poten_read = num1.data 
    L2.config(text= str(poten_read))## รับข้อความ
    print(poten_read)
sub = rospy.Subscriber("poten_angle", Int16,callback=readS2)

def readpoten_cal(num2):
    poten_cal = num2.data 
    #L3.config(text= str(poten_cal))## รับข้อความ
    print(poten_cal)
sub = rospy.Subscriber("poten_vul", Int16,callback=readpoten_cal)

def readenco_cal(num3):
    encoder_cal = num3.data 
    #L4.config(text= str(poten_cal))## รับข้อความ
    print(encoder_cal)
sub = rospy.Subscriber("encoder_pub", Int16,callback=readenco_cal)


# def send():
#     global servo_read
#     pubtorvid = rospy.Publisher('joint_states', JointState, queue_size=10)
#     rate = rospy.Rate(10)
#     msg = JointState()
#     msg.name = ['joint1']
#     msg.position = [servo_read]
#     pubtorvid.publish(msg)
#     rate.sleep()


# จำเป็นต้องเปิด tf เพื่อให้มุฟ

# br = tf.TransformBroadcaster();
# def get_param(name, value=None):
#     private = "~%s" % name
#     if rospy.has_param(private):
#         return rospy.get_param(private)
#     elif rospy.has_param(name):
#         return rospy.get_param(name)
#     else:
#         return value

# def talker():
#     global servo_read
#     global poten_read
#     encoder = -(servo_read*0.002181)
#     print("PotantialToRVID = ",poten)

#     poten = (0.2722*poten_read)
#     print("EncoderToRVID = ",encoder)
    
#     pub = rospy.Publisher('joint_states', JointState, queue_size=10)
#     rospy.init_node('test', anonymous=True)
#     rate = rospy.Rate(10) # 10hz
#     msg = JointState()
#     msg.name = ['joint1', 'joint2'];
#     msg.position = [poten,encoder]
        
#     source_list = get_param("source_list", [])
#     rospy.loginfo(str(source_list))
#     while not rospy.is_shutdown():
#         msg.header.stamp = rospy.Time.now();
#         pub.publish(msg)
#         rate.sleep()
    
# talker_thread = threading.Thread(target=talker)
# talker_thread.start()

def ON():
    print("ON")
    cmd = Twist()
    cmd.linear.x = 1.0
    cmd.angular.z=0.0
    # calPoAEntorvid()
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
    
B1 = Button(text = "ON", command=ON)
B1.place(x=140, y=20)

B2 = Button(text = "OFF", command=OFF)
B2.place(x=330, y=20)


frame.mainloop()