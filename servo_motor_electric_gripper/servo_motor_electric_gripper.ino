

#include <Servo.h>
 const int a=8;
 const int b=10;
Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos ;    // variable to store the servo position

void setup() {
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  pinMode(b,INPUT);
   pinMode(a,INPUT);
}

void loop() {
 const int c = digitalRead( a);
//const int d = digitalRead( b);

//Serial.println(d);
 Serial.println(c);
  if(c==1){
  for (pos = 90; pos >= 130; pos --) { 
    // in steps of 1 degree
    // Serial.println(pos );
    myservo.write(pos);              
   // delay(15);            
  }
 // delay(1000);
  }
  
//  if(d==1){
//  for (pos = 40; pos >= 38; pos --) { // goes from 180 degrees to 0 degrees  pos = 0; pos >= 0; pos -= 1
//    myservo.write(pos);              
//    delay(15);                       
//  }
// // delay(5000);
//}
else{
 for (pos = 130; pos <= 90; pos ++) { // goes from 0 degrees to 180 degrees    pos = 120; pos <= 120; pos += 1
    // in steps of 1 degree
  // Serial.println(pos );
    myservo.write(pos);              
   // delay(15);          
  }
  //delay(1000);
  }
}
  
