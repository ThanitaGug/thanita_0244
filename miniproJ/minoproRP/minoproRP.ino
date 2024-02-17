#include <Servo.h>
#include <Encoder.h>
#include <Wire.h>
#include <ros.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Empty.h>

Servo servopotentiometer;
Servo servoencoder;

//potentiometer
int servo_potentiometer = A3;
int potentiometerPin = A0;
int val;
int angle;

//Encoder
const int PINClk = 2;
const int PINDT = 3;
const int SW_PIN = 4;
const int homePosition = 0; 
const int stepValue = 10;
const int servo_encoder = 9;
int servoAngel = homePosition;

Encoder encoder(PINClk, PINDT);
bool sendValue_proten = false;

ros::NodeHandle nh;

std_msgs::Int16 servo_msg;
ros::Publisher servo_pub("servo_angle", &servo_msg);

std_msgs::Empty reset_msg;
ros::Publisher reset_pub("reset_signal", &reset_msg);

void resetCallback(const std_msgs::Empty& msg) {
  servopotentiometer.write(0);
}
//ros::Subscriber<std_msgs::Empty> reset_sub("reset_button", &resetCallback)

//void sendPotentiometer(const std_msgs::Empty &msg)
//{
//  sendValue_proten = true;
//}
//
//ros::Subscriber<std_msgs::Empty> send_potentiometer_value_sub("send_potentiometer_value", &sendPotentiometer);

std_msgs::Int16 poten_msg;
ros::Publisher poten_pub("poten_angle", &poten_msg);


void setup() {
  Serial.begin(9600);
  //potentiometer
  servopotentiometer.attach(servo_potentiometer);
  pinMode(servo_potentiometer,OUTPUT);
  pinMode(potentiometerPin,INPUT);

  //Encoder
  pinMode(SW_PIN,INPUT_PULLUP);
//  Serial.println("Robojax Encoder with Servo");
  servoencoder.attach(servo_encoder);  
//  servo.write(servoAngel);
//  delay(2000);  

  nh.initNode();
  nh.advertise(servo_pub);
  nh.advertise(reset_pub);
//  nh.subscribe(reset_pub);
  nh.advertise(poten_pub);
  

}
long oldPosition  = -999;

void loop() {
  //Potentiometer 
    val = analogRead(potentiometerPin);
    angle = map(val, 0, 1023, 0, 180);
    servopotentiometer.write(angle);
    poten_msg.data = angle;
    poten_pub.publish(&poten_msg);
    nh.spinOnce();
    delay(1);
// 

  //Encoder
  long newPosition = encoder.read();
 
  if (newPosition != oldPosition) {

    if(newPosition >  oldPosition)
    {
    int newStep = abs(newPosition - oldPosition);
      Serial.print("N!W Angle ");
      Serial.println(servoAngel);      
      servoAngel -= stepValue;
      if(servoAngel < 0){
          servoAngel =0;    
      }  
      servoencoder.write(servoAngel); //move servo to new angel
      Serial.print("newPosition: ");  
      Serial.println(newPosition);  
      
      Serial.println(servoAngel);
      servo_msg.data = servoAngel;
      servo_pub.publish(&servo_msg);
      nh.spinOnce();
      

    }
    if(newPosition <  oldPosition )
    {
    int newStep = abs(newPosition - oldPosition);
      Serial.print("N<W Angle ");
      Serial.println(servoAngel);        
      servoAngel += stepValue;
      if(servoAngel > 180)
          servoAngel =180;
      servoencoder.write(servoAngel); 
      Serial.print("newPosition: ");  
      Serial.println(newPosition);
      servo_msg.data = servoAngel;
      servo_pub.publish(&servo_msg);
      nh.spinOnce();  
      
      Serial.println(servoAngel);
    }
   oldPosition = newPosition;
  }
  if( digitalRead(SW_PIN) == LOW)
  {
    Serial.print("Home: ");
    Serial.println("GO HOME");
    servoAngel = homePosition;
    servoencoder.write(servoAngel); 
    Serial.print("SW Angle ");
    Serial.println(servoAngel);
    servo_msg.data = servoAngel;
    servo_pub.publish(&servo_msg);
    nh.spinOnce();
  }

  delay(10);
}
