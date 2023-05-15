#define CON_DP1 24 
#define CON_SP1 25

void setup() 
{
  // put your setup code here, to run once:
  pinMode(CON_DP1,OUTPUT);
  pinMode(CON_SP1,OUTPUT);
 // StartA();
}
void StartA()
{
  float delA=500;
  while(delA>2)
  {
digitalWrite(CON_SP1,HIGH);
 delayMicroseconds(delA);
    digitalWrite(CON_SP1,LOW);
    delayMicroseconds(delA); 
   
    delA=delA-50;
  }
  
}

void loop() 
{
  
 digitalWrite(CON_DP1,HIGH);
 
 digitalWrite(CON_SP1,HIGH);
 delayMicroseconds(100);
 digitalWrite(CON_SP1,LOW);
 delayMicroseconds(100);

 
}
