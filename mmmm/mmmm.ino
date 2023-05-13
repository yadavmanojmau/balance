const int hallPin = 2 ;     // initializing a pin for the sensor output

const int ledPin =  13 ;     // initializing a pin for the led. Arduino has built in led attached to pin 13
//#define enA 5 
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

// Variables for the duration and the distance


LiquidCrystal_I2C lcd(0x27,20,4);
  int count=0;  
  boolean state = true; 
void setup ( ) {

  pinMode ( ledPin , OUTPUT ) ; // This will initialize the LED pin as an output pin :
//  pinMode(enA, OUTPUT);
  lcd.init();                    
  lcd.backlight();
  lcd.setCursor(4,0);
  lcd.print("WELCOME");
  delay (2000);
  lcd.clear();
  
  pinMode ( hallPin , INPUT ) ;                        // This will initialize the hall effect sensor pin as an input pin to the Arduino :
  Serial.begin( 9600 ) ;
//  analogWrite (enA, 250);
  delay(1000);

}

void loop ( ) 

                        
{
  if ( digitalRead ( hallPin )== LOW) { 
     count++; 
      
     Serial.println ( " Magnet  dected " ) ; 
     Serial.print("Count: "); 
     lcd.setCursor(0,1);
     lcd.print("count="); 
     Serial.println(count);
     lcd.setCursor(6,1);
     lcd.print(count,1) ;
     lcd.setCursor(0,0);
     lcd.print("Magnet  dected");  
     delay(4000);
    }
  if ( digitalRead ( hallPin )==HIGH){
    lcd.setCursor(0,0);
    lcd.print("Magnet NOT dected"); 
}
}


 
