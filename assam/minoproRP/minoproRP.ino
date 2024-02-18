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
const int PINClk =2;
const int PINDT =3;
const int SW_PIN = 4;
const int homePosition = 0; 
const int stepValue = 10;
const int servo_encoder = 9;
int servoAngel = homePosition;
int enco = 0;
Encoder encoder(PINClk, PINDT);

ros::NodeHandle nh;
/// encoder ส่งองศา
std_msgs::Int16 servo_msg;
ros::Publisher servo_pub("servo_angle", &servo_msg);

/// encoder ส่งองศาคำนวน
std_msgs::Int16 encoder_cal;
ros::Publisher encoder_pub("encoder_valuel", &encoder_cal);

/// poten ส่งองศาคำนวน
std_msgs::Int16 poten_cal;
ros::Publisher poten_value("poten_vul", &poten_cal);

/// poten ส่งองศา
std_msgs::Int16 poten_msg;
ros::Publisher poten_pub("poten_angle", &poten_msg);


void setup() {
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
  nh.advertise(poten_pub);
  nh.advertise(poten_value);
  nh.advertise(encoder_pub);
}
long oldPosition  = -999;
int p=0;

void loop() {
  //Potentiometer 
    val = analogRead(potentiometerPin);
    angle = map(val, 0, 1023, 0, 180);
    servopotentiometer.write(angle);
    poten_msg.data = angle;
    poten_pub.publish(&poten_msg);
//    nh.spinOnce();
//    delay(1);
    
    p=0.2722*angle;
    poten_cal.data = p;
    poten_value.publish(&poten_cal);
    nh.spinOnce();
    delay(1);
 

  //Encoder
  long newPosition = encoder.read();
 
  if (newPosition != oldPosition) {

    if(newPosition >  oldPosition)
    {
    int newStep = abs(newPosition - oldPosition);    
      servoAngel -= stepValue;
      if(servoAngel < 0){
          servoAngel =0;    
      }  
      servoencoder.write(servoAngel); //move servo to new angel
      servo_msg.data = servoAngel;
      servo_pub.publish(&servo_msg);
      
      enco = -(servoAngel*0.002181);
      encoder_cal.data = enco;
      encoder_pub.publish(&encoder_cal);
      nh.spinOnce(); 


    }
    if(newPosition <  oldPosition )
    {
    int newStep = abs(newPosition - oldPosition);        
      servoAngel += stepValue;
      if(servoAngel > 180)
          servoAngel =180;
      servoencoder.write(servoAngel); 
      servo_msg.data = servoAngel;
      servo_pub.publish(&servo_msg);

      enco = -(servoAngel*0.002181);
      encoder_cal.data = enco;
      encoder_pub.publish(&encoder_cal);
      nh.spinOnce();  

    }
   oldPosition = newPosition;
  }
  
//  if( digitalRead(SW_PIN) == LOW)
//  {
//    Serial.print("Home: ");
//    Serial.println("GO HOME");
//    servoAngel = homePosition;
//    servoencoder.write(servoAngel); 
//    Serial.print("SW Angle ");
//    Serial.println(servoAngel);
//    servo_msg.data = servoAngel;
//    servo_pub.publish(&servo_msg);
//    nh.spinOnce();
//  }

  delay(1);
}
