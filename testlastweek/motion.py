#!/usr/bin/env python3
from tkinter import *
import rospy
from std_msgs.msg import String
from std_srvs.srv import Empty  # Import the Empty service from std_srvs package

root = Tk()
root.geometry("300x300")
root.title("Show Action")

# Callback function for handling the response from the reset service
def reset_response(response):
    print("Turtle reset successful")
    

def reset_turtle():
    try:
        #Call the "reset" service
        rospy.wait_for_service('/reset')
        reset_service = rospy.ServiceProxy('/reset', Empty)
        reset_service()
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

def clearToTextInput():
    reset_turtle()  # Call reset_turtle function when Clear button is pressed
    ActOut.delete("1.0", "end")

def run_motion(val):
    ActOut.insert("Received from Motion GUI:", val.data + "\n")
    #print("Received from Motion GUI:", val.data)

if __name__ == "__main__":
    sub = rospy.Subscriber("ch1", String, callback=run_motion)

    ActLabel = Label(text="Motion", font=("", 18))
    ActLabel.place(x=113, y=10)

    ActOut = Text(root, height=7, width=10, bg="light cyan", font=("", 16))
    ActOut.place(x=83, y=50)

    ClearBtn = Button(root, height=1, width=10, text="Clear", command=clearToTextInput)
    ClearBtn.place(x=103, y=250)


    root.mainloop()
