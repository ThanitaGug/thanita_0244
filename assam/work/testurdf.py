#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import Int16
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import tf

br = tf.TransformBroadcaster();
def get_param(name, value=None):
    private = "~%s" % name
    if rospy.has_param(private):
        return rospy.get_param(private)
    elif rospy.has_param(name):
        return rospy.get_param(name)
    else:
        return value

def talker(num10):
    nong1 = num10.data

    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('teat', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    msg = JointState()
    msg.name = ['joint1', 'joint2'];    
    msg.position = [nong1,0.04]
    source_list = get_param("source_list", [])
    rospy.loginfo(str(source_list))
    while not rospy.is_shutdown():
        msg.header.stamp = rospy.Time.now();
        pub.publish(msg)
        rate.sleep()
sub = rospy.Subscriber("int_poten", Int16,callback=talker)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass


# import rospy
# from std_msgs.msg import String
# from sensor_msgs.msg import JointState
# import tf
# from std_msgs.msg import Int16
# # จำเป็นต้องเปิด tf เพื่อให้มุฟ
# br = tf.TransformBroadcaster();
# def get_param(name, value=None):
#     private = "~%s" % name
#     if rospy.has_param(private):
#         return rospy.get_param(private)
#     elif rospy.has_param(name):
#         return rospy.get_param(name)
#     else:
#         return value

# def talker(numen):

#     # encoder = -(numen*0.002181)
#     # # print("PotantialToRVID = ",poten)

#     # # poten = (0.2722*numpo)
#     # print("EncoderToRVID = ",encoder)

#     pub = rospy.Publisher('joint_states', JointState, queue_size=10)
#     rospy.init_node('test', anonymous=True)
#     rate = rospy.Rate(10) # 10hz
#     msg = JointState()
#     msg.name = ['joint1', 'joint2'];
#     # msg.position = [encoder,0.04]
#     msg.position = [2,0.04]
    
#     source_list = get_param("source_list", [])
#     rospy.loginfo(str(source_list))
#     while not rospy.is_shutdown():
#         msg.header.stamp = rospy.Time.now();
#         # pub.publish(msg)
#         rate.sleep()
# # sub1 = rospy.Subscriber("servo_angle", Int16,callback=talker)
# # # sub2 = rospy.Subscriber("poten_angle", Int16,callback=talker)
# #     sub1=rospy.Subscriber("encoder_pub",Int16,callback=talker)

# if __name__ == '__main__':
#     try:
#         talker()
#     except rospy.ROSInterruptException:
#         pass