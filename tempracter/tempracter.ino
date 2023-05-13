#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display



const int sensor=A0; // Assigning analog pin A1 to variable 'sensor'
float tempc; //variable to store temperature in degree Celsius
float tempf; //variable to store temperature in Fahreinheit 
float vout; //temporary variable to hold sensor reading
//const int rs = 12, en = 11, d4 = 5, d5 = 2, d6 = 3, d7 = 4;
//LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
void setup()
{
pinMode(sensor,INPUT); // Configuring pin A1 as input
pinMode(13,OUTPUT);
 lcd.init();  
 lcd.backlight(); 
lcd.begin(16, 2);
Serial.begin(9600);
}
void loop() 
{
vout=analogRead(sensor);
vout=(vout*360)/1023;
Serial.println(vout);
tempc=vout; // Storing value in Degree Celsius
tempf=(vout*1.8)+32; // Converting to Fahrenheit 
lcd.print("Wellcome");
lcd.setCursor(0,1);
lcd.print("Temp in DegreeC=");
delay(800);
lcd.clear();
lcd.print(tempc);
delay(800);
lcd.clear();

//Serial.println(vout--);
if (vout>32 ){
 digitalWrite(13,HIGH);
//Temperature controlled fan kit

 Serial.println("Temperature HIGH");
 Serial.println("FAN is ON");
 lcd.print("Temperature HIGH");
 lcd.setCursor(0, 1);
 lcd.print("Turn ON FAN");
 delay(800);
 lcd.clear();

delay(1000);
}
else{
 digitalWrite(13,LOW);
Serial.print("in DegreeC=");
lcd.print("Temperature LOW");
lcd.setCursor(0,1);
lcd.print("Turn OFF FAN");
delay(800);
lcd.clear();
delay(1000); 
}
}
