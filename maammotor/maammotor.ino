#include<RMCS2303drive.h>

RMCS2303 rmcs;                      //object for class RMCS2303

SoftwareSerial myserial(2,3);     //Software Serial port For Arduino Uno. Comment out if using Mega.
#include<LiquidCrystal_I2C.h>
//Parameter Settings "Refer datasheet for details" - 
byte slave_id=7;                    //Choose the slave id of connected drive.
int INP_CONTROL_MODE=513;           //IMPORTANT: refer datasheet and set value(integer) according to application 
int PP_gain=32;
int PI_gain=16;
int VF_gain=32;
int LPR=334;
int acceleration=5000;
int speed=400;
LiquidCrystal_I2C lcd(0x27,16,2);
long int Current_position;
long int Current_Speed;
long int A;

void setup()
{
   rmcs.Serial_selection(1);       //Serial port selection:0-Hardware serial,1-Software serial
   rmcs.Serial0(9600);             //set baudrate for usb serial to monitor data on serial monitor
   Serial.println("RMCS-2303 Position control mode demo\r\n\r\n");
lcd.init();
lcd.backlight();
   //rmcs.begin(&Serial1,9600);    //Uncomment if using hardware serial port for mega2560:Serial1,Serial2,Serial3 and set baudrate. Comment this line if Software serial port is in use
   rmcs.begin(&myserial,9600);     //Uncomment if using software serial port. Comment this line if using hardware serial.
   rmcs.WRITE_PARAMETER(slave_id,INP_CONTROL_MODE,PP_gain,PI_gain,VF_gain,LPR,acceleration,speed);    //Uncomment to write parameters to drive. Comment to ignore.
   rmcs.READ_PARAMETER(slave_id);
   
}

void loop()
{
   Serial.println("Sending absolute position command to -50000");
   rmcs.Absolute_position(slave_id,-66300);   //enter position count with direction (CW:+ve,CCW:-ve) 
   
   while(1)       //Keep reading positions. Exit when reached.
   {
      Current_position=rmcs.Position_Feedback(slave_id); //Read current encoder position 
      Current_Speed=rmcs.Speed_Feedback(slave_id); //Read current speed      Serial.print(Current_position);

           
      Serial.print("Position Feedback :\t");
      Serial.print(Current_position);
       lcd.setCursor(0,0);
       lcd.print("pules=");
         lcd.setCursor(6,0);
      lcd.print(Current_position);
       A=(Current_position/184);
            Serial.print( "\tangle :");
            
            Serial.println(A);
            lcd.setCursor(10,1);
       lcd.print("A=");
      lcd.setCursor(12,1);
       lcd.print(A);
       //lcd.print("360");
      //Serial.print("\t\tSpeed Feedback :\t");
     // Serial.print(Current_position);
      //lcd.clear();  
      delay(1000);
      if(Current_position==-66300)
  
    
      {
         Serial.println("Position reached.");
         break;
          A=(Current_position/184);
lcd.setCursor(0,0);
       lcd.print("pules=");
         lcd.setCursor(6,0);
      lcd.print(Current_position);          
          Serial.println(A);
            lcd.setCursor(11,1);
       lcd.print("A=");
      lcd.setCursor(13,1);
     lcd.print(A);
      lcd.print("360");
      }
   }
  
   delay(2000);
   lcd.clear();
   
   Serial.println("Sending absolute position command to 50000");
   rmcs.Absolute_position(slave_id,66300);   //enter position count with direction (CW:+ve,CCW:-ve) 
   
   while(1)       //Keep reading positions. Exit when reached.
   {
      Current_position=rmcs.Position_Feedback(slave_id); //Read current encoder position 
      Current_Speed=rmcs.Speed_Feedback(slave_id);       //Read current speed
      Serial.print("Position Feedback :\t");
      Serial.print(Current_position);
      lcd.setCursor(0,0);
      lcd.print("pules=");
      lcd.setCursor(6,0);
      lcd.print(Current_position);
      
          A=(Current_position/184);
            Serial.print( "\tangle : ");
            Serial.println(A);
            lcd.setCursor(11,1);
       lcd.print("A=");

        lcd.setCursor(13,1);
       lcd.print(A);
      lcd.print("-360");
     // Serial.print("\t\tSpeed Feedback :\t");
     // Serial.println(Current_Speed);
    
      delay(2000);
      if(Current_position==66300) 
  
      {
         Serial.println("Position reached " );
         break;
          A=(Current_position/184);
          Serial.println(A);
          lcd.setCursor(0,0);
       lcd.print("pules=");
         lcd.setCursor(6,0);
      lcd.print(Current_position);
           lcd.setCursor(11,1);
      lcd.print("A");
      lcd.setCursor(13,1);
       lcd.print(A,1);
      }
   }
   
   delay(2000);
  lcd.clear();  

   
   Serial.println("Disabling motor.");
   rmcs.Disable_Position_Mode(slave_id);            //Disable postion control mode
   delay(1000);

    Serial.println(A);
}
           
