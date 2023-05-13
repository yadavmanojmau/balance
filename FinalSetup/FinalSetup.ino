
/****************************************Copyright(c)*****************************************************
**                            Shenzhen Yuejiang Technology Co., LTD.
**
**                                 http://www.dobot.cc
**
**--------------File Info---------------------------------------------------------------------------------
** File name:           main.cpp
** Latest modified Date:2016-10-24
** Latest Version:      V2.0.0
* 
** Descriptions:        main body
**
**--------------------------------------------------------------------------------------------------------
** Modify by:           Edward
** Modified date:       2016-11-25
** Version:             V1.0.0
** Descriptions:        Modified,From DobotDemoForSTM32
**--------------------------------------------------------------------------------------------------------
*********************************************************************************************************/
#include "stdio.h"
#include "Protocol.h"
#include "command.h"
#include "FlexiTimer2.h"
#include <Wire.h>
//Set Serial TX&RX Buffer Size
#define SERIAL_TX_BUFFER_SIZE 64
#define SERIAL_RX_BUFFER_SIZE 256


//#define JOG_STICK 
/*********************************************************************************************************
** Global parameters
*********************************************************************************************************/
EndEffectorParams gEndEffectorParams;

JOGJointParams  gJOGJointParams;
JOGCoordinateParams gJOGCoordinateParams;
JOGCommonParams gJOGCommonParams;
JOGCmd          gJOGCmd;

PTPCoordinateParams gPTPCoordinateParams;
PTPCommonParams gPTPCommonParams;
PTPCmd          gPTPCmd;

uint64_t gQueuedCmdIndex;





#define DOB_DP 22  //Dobot slider pins
#define DOB_SP 23

#define CON_DP 24  //Conv Pins
#define CON_SP 25
 
#define CSA1_DP 26 //Sorting Arm 1 pins
#define CSA1_SP 27

#define CSA2_DP 28 //Sorting arm 2 pins
#define CSA2_SP 29 

#define Limit1 3  //Limit switchs pins
#define Limit2 2

#define mo 38       //Compresor pins
#define de 39

#define sliderLED 37
#define SortingArm1 34
#define SortingArm2 32
#define Conveyor 35
#define Compresor 33

int flag = 7;       
int cFlag = 2;

int start,a,ack,b,c,d,e,f,g,bin=8,color=0,task=0;

int ack1=23,ack2,ack3,ack4,ack5,ack6,ack7,ack8,ack9,ack10;

int x=156 ,y=-56 ,z=136 ;

int delA=400;

/*********************************************************************************************************
** Function name:       setup
** Descriptions:        Initializes Serial
** Input parameters:    none
** Output parameters:   none
** Returned value:      none
*********************************************************************************************************/
void setup() 
{
    Wire.begin(20);
    Serial.begin(115200);
    Serial1.begin(115200); 
    printf_begin();
    //Set Timer Interrupt
    FlexiTimer2::set(100,Serialread); 
    FlexiTimer2::start();
    Wire.onRequest(requestEvent);
    Wire.onReceive(receiveEvent);

    pinMode(mo,OUTPUT);
    pinMode(de,OUTPUT);

    digitalWrite(mo,HIGH);
    digitalWrite(de,HIGH);
    digitalWrite(sliderLED,HIGH);
    digitalWrite(Compresor,HIGH);
    digitalWrite(SortingArm1,HIGH);
    digitalWrite(SortingArm2,HIGH);
    digitalWrite(Conveyor,HIGH);
    digitalWrite(Compresor,HIGH);
    
    pinMode(DOB_SP ,OUTPUT);
    pinMode(DOB_DP,OUTPUT);
    
    pinMode(Limit1,INPUT_PULLUP);
    pinMode(Limit2,INPUT_PULLUP);
    
    pinMode(CON_DP,OUTPUT);
    pinMode(CON_SP,OUTPUT);
    
    pinMode(CSA1_DP,OUTPUT);
    pinMode(CSA1_SP,OUTPUT);
    pinMode(CSA2_DP,OUTPUT);
    pinMode(CSA2_SP,OUTPUT);

     pinMode(sliderLED,OUTPUT);
     pinMode(Compresor,OUTPUT);
     pinMode(SortingArm1,OUTPUT);
     pinMode(SortingArm2,OUTPUT);
     pinMode(Conveyor,OUTPUT);
    
attachInterrupt(digitalPinToInterrupt(Limit2), pause, CHANGE);
}

void pause()
{
 while(1);   
}
/*********************************************************************************************************
** Function name:       Serialread
** Descriptions:        import data to rxbuffer
** Input parametersnone:
** Output parameters:   
** Returned value:      
*********************************************************************************************************/
void Serialread()
{
  while(Serial1.available()) 
  {
        uint8_t data = Serial1.read();
        if (RingBufferIsFull(&gSerialProtocolHandler.rxRawByteQueue) == false) 
        {
            RingBufferEnqueue(&gSerialProtocolHandler.rxRawByteQueue, &data);
        }
  }
}
/*********************************************************************************************************
** Function name:       Serial_putc
** Descriptions:        Remap Serial to Printf
** Input parametersnone:
** Output parameters:   
** Returned value:      
*********************************************************************************************************/
int Serial_putc( char c, struct __file * )
{
    Serial.write( c );
    return c;
}

/*********************************************************************************************************
** Function name:       printf_begin
** Descriptions:        Initializes Printf
** Input parameters:    
** Output parameters:
** Returned value:      
*********************************************************************************************************/
void printf_begin(void)
{
    fdevopen( &Serial_putc, 0 );
}

/*********************************************************************************************************
** Function name:       InitRAM
** Descriptions:        Initializes a global variable
** Input parameters:    none
** Output parameters:   none
** Returned value:      none
*********************************************************************************************************/
void InitRAM(void)
{
    //Set JOG Model
    gJOGJointParams.velocity[0] = 100;
    gJOGJointParams.velocity[1] = 100;
    gJOGJointParams.velocity[2] = 100;
    gJOGJointParams.velocity[3] = 100;
    gJOGJointParams.acceleration[0] = 80;
    gJOGJointParams.acceleration[1] = 80;
    gJOGJointParams.acceleration[2] = 80;
    gJOGJointParams.acceleration[3] = 80;

    gJOGCoordinateParams.velocity[0] = 100;
    gJOGCoordinateParams.velocity[1] = 100;
    gJOGCoordinateParams.velocity[2] = 100;
    gJOGCoordinateParams.velocity[3] = 100;
    gJOGCoordinateParams.acceleration[0] = 80;
    gJOGCoordinateParams.acceleration[1] = 80;
    gJOGCoordinateParams.acceleration[2] = 80;
    gJOGCoordinateParams.acceleration[3] = 80;

    gJOGCommonParams.velocityRatio = 50;
    gJOGCommonParams.accelerationRatio = 50;
   
    gJOGCmd.cmd = AP_DOWN;
    gJOGCmd.isJoint = JOINT_MODEL;

    

    //Set PTP Model
    gPTPCoordinateParams.xyzVelocity = 100;
    gPTPCoordinateParams.rVelocity = 100;
    gPTPCoordinateParams.xyzAcceleration = 80;
    gPTPCoordinateParams.rAcceleration = 80;

    gPTPCommonParams.velocityRatio = 50;
    gPTPCommonParams.accelerationRatio = 50;

    gPTPCmd.ptpMode = MOVL_XYZ;
    gPTPCmd.x = 169;
    gPTPCmd.y = -160;
    gPTPCmd.z = 78;
    gPTPCmd.r = -19;

    gQueuedCmdIndex = 0;

    
}
void receiveEvent(int howMany) 
{  
    int crap = Wire.read();

      a = Wire.read(); 
     b = Wire.read(); 
     c = Wire.read();
     d = Wire.read();
     e = Wire.read();
     f = Wire.read();
     g = Wire.read();  //Suction
     bin = Wire.read();//Bin Index
     color =Wire.read();//color Index
     task=Wire.read();//Task Index

      Serial.print("X index:-       ");
      Serial.println(a);
      Serial.print("X coordinate:-  ");
      Serial.println(b);
      Serial.print("Y index:-       ");
      Serial.println(c);
      Serial.print("Y coordinate:-  "); 
      Serial.println(d);     
      Serial.print("Z index:-       ");
      Serial.println(e);
      Serial.print("Z coordinate:-  "); 
      Serial.println(f);
      Serial.print("Suction index:- ");
      Serial.println(g);
      Serial.print("Bin index:- ");
      Serial.println(bin);
      Serial.print("Color index:- ");
      Serial.println(color);
      Serial.print("Task index:- ");
      Serial.println(color);
}

void requestEvent()
{
  Wire.write(ack);
  Wire.write(ack1);
  Wire.write(ack2);
  Wire.write(ack3);
  Wire.write(ack4);
  Wire.write(ack5);
  Wire.write(ack6);
  Wire.write(ack7);
  Wire.write(ack8);
  Wire.write(ack9);
    Wire.write(ack10);
}
/*********************************************************************************************************
** Function name:       loop
** Descriptions:        Program entry
** Input parameters:    none
** Output parameters:   none
** Returned value:      none
*********************************************************************************************************/
void moveDobot(float x,float y,float z,float g)
{
  //digitalWrite(Compresor,LOW);
   static uint32_t timer = millis();
        static uint32_t count = 0;
        #ifdef JOG_STICK
        if(millis() - timer > 1000)
        {
            timer = millis();
            count++;
            switch(count){
                case 1:
                    gJOGCmd.cmd = AP_DOWN;
                    gJOGCmd.isJoint = JOINT_MODEL;
                    SetJOGCmd(&gJOGCmd, true, &gQueuedCmdIndex);
                    break;
                case 2:
                    gJOGCmd.cmd = IDEL;
                    gJOGCmd.isJoint = JOINT_MODEL;
                    SetJOGCmd(&gJOGCmd, true, &gQueuedCmdIndex);
                    break;
                case 3:
                    gJOGCmd.cmd = AN_DOWN;
                    gJOGCmd.isJoint = JOINT_MODEL;
                    SetJOGCmd(&gJOGCmd, true, &gQueuedCmdIndex);
                    break;
                case 4:
                    gJOGCmd.cmd = IDEL;
                    gJOGCmd.isJoint = JOINT_MODEL;
                    SetJOGCmd(&gJOGCmd, true, &gQueuedCmdIndex);
                    break;
                default:
                    count = 0;
                    break;
              }
        }
        #else
        
        gPTPCmd.x = x;
        gPTPCmd.y = y;
        gPTPCmd.z = z;
        SetPTPCmd(&gPTPCmd, true, &gQueuedCmdIndex);
               
        #endif
        ProtocolProcess();

        if(g==1)
        {
           digitalWrite(mo,LOW);
          digitalWrite(de,LOW);
          digitalWrite(Compresor,LOW);
          
        }
        else
        {
         digitalWrite(mo,HIGH);
          digitalWrite(de,HIGH);
          digitalWrite(Compresor,HIGH);
        }
        //digitalWrite(Compresor,HIGH);
}




void loop() 
{



    InitRAM();

    ProtocolInit();
    
    SetJOGJointParams(&gJOGJointParams, true, &gQueuedCmdIndex);
    
    SetJOGCoordinateParams(&gJOGCoordinateParams, true, &gQueuedCmdIndex);
    
    SetJOGCommonParams(&gJOGCommonParams, true, &gQueuedCmdIndex);
    
    printf("\r\n======Enter demo application======\r\n");
    
    SetPTPCmd(&gPTPCmd, true, &gQueuedCmdIndex);
    
    for(; ;)
    {

        if(
//      delay(1000);
//      moveDobot(23,-142,120,0);
//      delay(3000);
//      
//      delay(2000);


     //flat ellips
     moveDobot(209,74,-31,1);
     delay(3000);
     moveDobot(196,74,-31,1);
     delay(3000);
     moveDobot(200,-71,-33,1);
     delay(3000);
     moveDobot(120,-175,-33,1);
     delay(3000);
     moveDobot(29,-214,-14,1);
     delay(3000);
     moveDobot(105,-149,4,1);
     delay(3000);
     moveDobot(206,-110,5,1);
     delay(3000);
     moveDobot(247,-29,-22,1);
     delay(3000);
     moveDobot(191,-55,-40,1);
     delay(3000);
     moveDobot(244,-70,-8,1);
     delay(3000);
    


//    moveDobot(116,-226,79,0);
//    delay(3000);
//    moveDobot(116,-226,-39,1);
//    delay(3000);
//    moveDobot(116,-226,79,1);
//    delay(3000);
//    moveDobot(-50,-228,79,1);
//    delay(3000);
//    moveDobot(-54,-239,7,1);
//    delay(3000);
//    moveDobot(-54,-239,-47,1);
//    delay(3000);
//    moveDobot(-54,-239,7,0);
//    delay(3000);
//    
//    moveDobot(-50,-228,79,0);
//     delay(3000);

//    //Square
//    moveDobot(64,-216,107,0);
//    delay(3000);
//    moveDobot(64,-216,-9,1);
//    delay(3000);
//    moveDobot(64,-216,-39,1);
//    delay(3000);
//    moveDobot(64,-216,107,1);
//    delay(3000);
//    moveDobot(10,-215,107,1);
//    delay(3000);
//    moveDobot(-105,-238,-3,1);
//    delay(3000);
//    moveDobot(-105,-238,-43,1);
//    delay(3000); 
//
//   moveDobot(-105,-238,-3,0);
//    delay(3000);
//    moveDobot(10,-215,107,0);
//    delay(3000);
//  
//
//    //triangle
//    moveDobot(51,-153,107,0);
//    delay(3000);
//    moveDobot(51,-153,-4,1);
//    delay(3000);
//    moveDobot(51,-153,-40,1);
//    delay(3000);
//    moveDobot(51,-153,107,1);
//    delay(3000);
//    moveDobot(-2,-157,107,1);
//    delay(3000);
//    moveDobot(-110,-177,-20,1);
//    delay(3000);
//    moveDobot(-110,-177,-45,1);
//    delay(3000);
//    
//    moveDobot(-110,-177,-20,0);
//    delay(3000);
//    moveDobot(-2,-157,107,0);
//
//   
      
  //  }
        
      }
