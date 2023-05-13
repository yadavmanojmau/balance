const int trigPin = 10;
const int echoPin = 11;
#include <LiquidCrystal_I2C.h>
#include <Servo.h>
LiquidCrystal_I2C lcd(0x27,20,4);
  int count=0;  
  boolean state = true; 
  const int hallPin = 2 ;     // initializing a pin for the sensor output
const int ledPin =  13 ;
// Variables for the duration and the distance
//long duration;
Servo myServo;
//int distance;
int duration = 0;
int distance = 0;
void setup() 
{ 
 pinMode(trigPin , OUTPUT);
 pinMode(echoPin , INPUT);
pinMode ( ledPin , OUTPUT ) ; 
  lcd.init();                    
  lcd.backlight();
  lcd.setCursor(4,0);
  lcd.print("WELCOME");
  delay (2000);
  lcd.clear();
  pinMode ( hallPin , INPUT ) ;                        // This will initialize the hall effect sensor pin as an input pin to the Arduino :
  Serial.begin( 9600 ) ;
  delay(1000);
  }

void loop()
{
  
 digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);  
  duration = pulseIn(echoPin, HIGH);
 
  distance = duration/58.2;
  Serial.println(distance); 
  lcd.clear();
   lcd.setCursor(0,0);
    lcd.print("Magnet not dected");
    lcd.setCursor(0,1);
     lcd.print("Dist=");
     lcd.setCursor(5,1);
   
    myServo.write(distance);
    lcd.print( distance,1);
     
   if ( digitalRead ( hallPin )== LOW) {
     count++;
     
      Serial.println ( "Magnet   dect. " ) ; 
     Serial.print("Count: ");
     Serial.println(count);
      lcd.setCursor(8,1);
     lcd.print("count=");
      lcd.print(count);
      Serial.println(distance); 
     lcd.setCursor(0,0);
     lcd.print("Magnet  dected  ");
      
      
     delay(4000);
     //lcd.clear();
    }
     if ( digitalRead ( hallPin )== HIGH) {
      Serial.println ( "Magnet NOT dected" ) ;
          }
         }
