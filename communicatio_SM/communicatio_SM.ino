
#include <Wire.h>
int led =13;
int  data;
void setup() {
  Wire.begin(20);                // join i2c bus with address #20
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);
  pinMode(led,OUTPUT);
  Serial.begin(9600);           // start serial for output
}

void loop() {
  delay(100);
      Wire.available() ; // loop through all but the last
     int a = Wire.read(); // receive byte as a character
    Serial.println(a);  
    
  if   (a==2)
    {
      digitalWrite(led,1);
     Serial.print("led is  yellow on");

     delay(4000);
     digitalWrite(led,0);
     delay(400);
      }
    else if(a==8)
     {
      digitalWrite(led,1);
     Serial.println("led is  green on");

     delay(4000);
     digitalWrite(led,0);
     delay(400);
        }
}


void receiveEvent(int howMany) {
  
    int a = Wire.read(); 
 
}
