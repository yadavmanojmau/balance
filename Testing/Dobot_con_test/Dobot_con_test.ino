#define DOB_DP 22  
#define DOB_SP 23
#define Limit1 3  //Limit switchs pins
int flag = 7; 
void setup() {
  // put your setup code here, to run once:
 pinMode(DOB_SP ,OUTPUT);
    pinMode(DOB_DP,OUTPUT);
         pinMode(Limit1,INPUT_PULLUP);
     Serial.begin(9600);
}
int del=80;
void DobotHome()
{ 
   if(flag!=0)
    {
       while(digitalRead(Limit1)== 0)
      {
          digitalWrite(DOB_DP,LOW);
          digitalWrite(DOB_SP,HIGH);
          delayMicroseconds(800);
          digitalWrite(DOB_SP,LOW);
          delayMicroseconds(800); 
      }
    }
   flag=0;  
}
void dobotbin1()
{
  if(flag!=1)
  {
     for (int i =0; i<4510 ; i++)    
      {
         digitalWrite(DOB_DP,HIGH);
         digitalWrite(DOB_SP,HIGH);
         delayMicroseconds(800);
         digitalWrite(DOB_SP,LOW);
         delayMicroseconds(800);
     }    
  }
  flag=1;
}
void dobotbin2()
{
  if(flag!=2)
  {  
  for (double i =0; i<2250; i++)
  {
    digitalWrite(DOB_DP,HIGH);
    digitalWrite(DOB_SP,HIGH);
    delayMicroseconds(800);
    digitalWrite(DOB_SP,LOW);
    delayMicroseconds(800);
  }
  }
   flag=2;
   
}
void dobotbin3()
{
  if(flag!=3)
  {
  
  for (double i =0; i<2250 ; i++)
  {
    
    digitalWrite(DOB_DP,HIGH);
    digitalWrite(DOB_SP,HIGH);
    delayMicroseconds(del);
    digitalWrite(DOB_SP,LOW);
    delayMicroseconds(del);
  }
  }
   flag=3;
  
}

void dobotbin23()
{
  if(flag!=3)
  {
 
  for (double i =0; i<29005; i++)    //29005
  {
    
    digitalWrite(DOB_DP,HIGH);
    digitalWrite(DOB_SP,HIGH);
    delayMicroseconds(del);
    digitalWrite(DOB_SP,LOW);
    delayMicroseconds(del);
  }
  }
   flag=3;
   
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.println(digitalRead(Limit1));
  DobotHome();
  delay(1000);
    dobotbin3();
   delay(5000);
     dobotbin2();
   delay(5000);
  
  while(1);
}
