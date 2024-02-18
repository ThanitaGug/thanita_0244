#!/usr/bin/env python3
import customtkinter,tkinter
from tkinter import*
import rospy
from std_msgs.msg import Int16
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
# import tf
# import threading

pubtojoint = rospy.Publisher('joint_states', JointState, queue_size=10)

def setup():
    msg = JointState()
    msg.name = ['joint1', 'joint2'];  
    msg.position = [0,0]
    pubtojoint.publish(msg)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
encoder_cal = None
poten_cal = None
frame = customtkinter.CTk()
# score = Tk()

frame.title("GUI REMOTE")
frame.geometry("1000x600")
rospy.init_node("GUI_EX", anonymous=True)
# pub = rospy.Publisher("servo_angle",Twist, queue_size=10)
rate = rospy.Rate(10)
rate.sleep()
system_state = "ON"
frame.after(1000,setup)
        
#pub = rospy.Publisher('joint_states', JointState, queue_size=10)

##Background
frame = customtkinter.CTkFrame(master = frame,fg_color= "#BEBEBE")
frame.pack(padx = 1,pady = 1,fill="both",expand=True)

##ฟังก์ชันรับค่าทั้งหมด##
## ตัวรับค่าโพเทนส่งให้ L1 encoder sensor ##
L1 = Label(frame,font = ('Arial',60),text ="00",bg="#BEBEBE")
L1.place(x=380, y=200)


def readS1(num):
    global system_state
    global servo_read
    servo_read = num.data 
    if system_state == "ON":
        L1.config(text = str(servo_read))## รับข้อความ encoder
        slider.set(servo_read)
        print(servo_read)
        

## ตัวรับค่าโพเทนส่งให้ L2 Pote##
L2 = Label(frame,font = ('Arial',60),text ="00",bg="#BEBEBE")
L2.place(x=730, y=200)

def readS2(num1):
    global system_state
    global poten_read
    poten_read = num1.data
    
    if system_state == "ON":
        L2.config(text=str(poten_read))
        slider2.set(poten_read)
        print(poten_read)

## ตัวรับค่าโพเทนส่งให้ L1 encoder cal ##
L3 = Label(frame,font = ('Arial',60),text ="00",bg="#BEBEBE")
L3.place(x=380, y=380)

def readenco_cal(num3):
    global encoder_cal
    encoder_cal = num3.data 
    L3.config(text= str(encoder_cal))## รับข้อความ
    # slider.set(encoder_cal)
    print(encoder_cal)
    # talker()
sub3 = rospy.Subscriber("encoder_valuel", Float64,callback=readenco_cal)


L4 = Label(frame,font = ('Arial',60),text ="00",bg="#BEBEBE")
L4.place(x=730, y=380)
def readpoten_cal(num2):
    global poten_cal
    poten_cal = num2.data 
    L4.config(text= str(poten_cal))## รับข้อความ
    # slider2.set(poten_cal)
    print(poten_cal)
sub4= rospy.Subscriber("poten_vul", Float64,callback=readpoten_cal)

# pub_poten = rospy.Publisher("int_poten",Int16, queue_size=10)
def slider_event(value):
    text_degree.set(f"{int(slider.get())}")
    text_degree2.set(f"{int(slider2.get())}")
    # V1 = text_var
    # V2 = text_var2
    print("encoder value = "+str(text_degree.get()))
    print("poten value = "+str(text_degree2.get()))

slider = customtkinter.CTkSlider(master=frame,from_=0,to=90,command=slider_event)
slider.place(x=320,y=510,anchor=tkinter.W)





def talker():
    global encoder_cal
    global poten_cal
    msg = JointState()
    rate = rospy.Rate(10) # 10hz
    msg.name = ['joint1', 'joint2']
    # msg.name = ['joint1', 'joint2']  
    # msg.position = [slider.get(),slider2.get()] 
    # pubtojoint.publish(msg)
    # rate.sleep()      
    
    #rospy.init_node('teat', anonymous=True)
    msg.position = [encoder_cal,poten_cal] 
    msg.header.stamp = rospy.Time.now()
    pubtojoint.publish(msg)
    rate.sleep()

# talker_thread = threading.Thread(target=talker)
# talker_thread.start()





def button_on():
    global system_state
    print("ON")
    system_state = "ON"
    cmd = Twist()
    cmd.linear.x = 1.0
    cmd.angular.z=0.0
    # pub.publish(cmd)

def button_off():
    # print("button OFF")
    global system_state
    print("OFF")
    system_state = "OFF"
    cmd = Twist()
    cmd.linear.x = -1.0
    cmd.angular.z = 0.0



def button_reset():
    # print("button OFF")
    global system_state
    print("RESET")
    # system_state = "RESET"
    talker()
    

sub1= rospy.Subscriber("poten_angle", Int16,callback=readS2)
sub= rospy.Subscriber("servo_angle", Int16,callback=readS1)


##เเถบข้อมูลด้านข้าง##
namepro = tkinter.StringVar(value="RP ROBOT")
label = customtkinter.CTkLabel(master=frame,
                               textvariable=namepro,
                               width=120,
                               height=25,
                               font=('Hello',30),
                               text_color="black",
                               fg_color=("white", "gray75"),
                               corner_radius=8)
label.place(x=55, y=55, anchor=tkinter.W)


frame1 = customtkinter.CTkFrame(frame,fg_color= "#DCDCDC", width=250,height=500, corner_radius=10)
# frame.place(relx=0, rely=0, anchor=tkinter.W)
frame1.grid(row=0, column=0, padx=0, pady=100, sticky="ew")

text_var = tkinter.StringVar(value=" MODE ")
label = customtkinter.CTkLabel(master=frame1,
                               textvariable=text_var,
                               width=225,
                               height=50,
                               fg_color=("#BEBEBE"),
                               text_color="black",
                               corner_radius=8)
label.place(x=10, y=40, anchor=tkinter.W)

##dropdown mode
optionmenu_var = customtkinter.StringVar(value="")  # set initial value
def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)
    

combobox = customtkinter.CTkOptionMenu(master=frame1,
                                       values=["GUI", "MANUAL"],
                                       command=optionmenu_callback,
                                       variable=optionmenu_var,
                                       height=30,
                                       width=225,
                                       fg_color=("#BEBEBE"),
                                       text_color="black",
                                       font=('Arial',15),
                                       dropdown_font=('Arial',15),
                                       dropdown_text_color="black",
                                       dropdown_fg_color=("white", "gray75"),
                                       dropdown_hover_color="green"
                                       )
combobox.place(x=10, y=85, anchor=tkinter.W)


button = customtkinter.CTkButton(master=frame1,
                                 width=80,
                                 height=32,
                                 fg_color="green", 
                                 hover_color="grey",
                                 border_width=0,
                                 corner_radius=8,
                                 text="ON",
                                 command=button_on)
button.place(x=10, y=400, anchor=tkinter.W)



button = customtkinter.CTkButton(master=frame1,
                                 width=80,
                                 height=32,
                                 fg_color="red", 
                                 hover_color="gray",
                                 border_width=0,
                                 corner_radius=8,
                                 text="OFF",
                                 command=button_off)
button.place(x=150, y=400, anchor=tkinter.W)

button = customtkinter.CTkButton(master=frame1,
                                 width=80,
                                 height=32,
                                 fg_color="yellow", 
                                 hover_color="gray",
                                 border_width=0,
                                 corner_radius=8,
                                 text="RESET",
                                 command=talker)
button.place(x=150, y=300, anchor=tkinter.W)

##จบเเถบข้อมูลด้านข้าง##

## JOINT 1 ##

nameJ1 = tkinter.StringVar(value=" JOINT 1 ")
label = customtkinter.CTkLabel(master=frame,
                               textvariable=nameJ1,
                               width=160,
                               height=50,
                               font=('Arial',15),
                               text_color="white",
                               fg_color=("#000000"),
                               corner_radius=30)
label.place(x=350, y=70, anchor=tkinter.W)

nameEn = tkinter.StringVar(value=" ENCODER ")
label = customtkinter.CTkLabel(master=frame,
                               textvariable=nameEn,
                               font=('Arial',20),
                               text_color="black",)
label.place(x=380, y=120, anchor=tkinter.W)

realvale_encoder = tkinter.StringVar(value="Real Value")
labelr = customtkinter.CTkLabel(master = frame,textvariable = realvale_encoder ,width=150,height=30,
                                fg_color=("#757575"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(x=350,y=160,anchor=tkinter.W)


usevale_encoder = tkinter.StringVar(value="Use Value")
labelr = customtkinter.CTkLabel(master = frame,textvariable = usevale_encoder ,width=150,height=30,
                                fg_color=("#757575"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)

text_degree = tkinter.StringVar(value="0")
labelr = customtkinter.CTkLabel(master = frame,textvariable = text_degree,width=120,height=25,
                                fg_color=("green","black"),
                                text_color="white",
                                font=('Arial',20),
                                corner_radius=8)
labelr.place(x=360,y=550,anchor=tkinter.W)
### END JOINT 1##



## JOINT 2 ##

nameJ2 = tkinter.StringVar(value=" JOINT 2 ")
label = customtkinter.CTkLabel(master=frame,
                               textvariable=nameJ2,
                               width=160,
                               height=50,
                               font=('Arial',15),
                               text_color="white",
                               fg_color=("#000000"),
                               corner_radius=30)
label.place(x=700, y=70, anchor=tkinter.W)

namePo = tkinter.StringVar(value=" POTENTIOMETER ")
label = customtkinter.CTkLabel(master=frame,
                               textvariable=namePo,
                               font=('Arial',20),
                               text_color="black",)
label.place(x=690, y=120, anchor=tkinter.W)

realvale_encoder = tkinter.StringVar(value="Real Value")
labelr = customtkinter.CTkLabel(master = frame,textvariable = realvale_encoder ,width=150,height=30,
                                fg_color=("#757575"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(x=700,y=160,anchor=tkinter.W)
    

usevale_poten = tkinter.StringVar(value="Use Value")
labelr = customtkinter.CTkLabel(master = frame,textvariable = usevale_poten ,width=150,height=30,
                                fg_color=("#757575"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(x=700,y=340,anchor=tkinter.W)

slider2 = customtkinter.CTkSlider(master=frame,from_=0,to=180,command=slider_event)
slider2.place(x=680,y=510,anchor=tkinter.W)

text_degree2 = tkinter.StringVar(value="0")
labelr2 = customtkinter.CTkLabel(master = frame, textvariable = text_degree2 ,width=120,height=25,
                                fg_color=("green","black"),
                                text_color="white",
                                font=('Arial',20),
                                corner_radius=8)
labelr2.place(x=720,y=550,anchor=tkinter.W)

##END JOINT 2##





frame.mainloop()
# frame.mainloop()

