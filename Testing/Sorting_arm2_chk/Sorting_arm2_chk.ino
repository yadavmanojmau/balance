
#define CSA2_DP 28 
#define CSA2_SP 29 

void setup() 
{
  // put your setup code here, to run once:

  pinMode(CSA2_DP,OUTPUT);
  pinMode(CSA2_SP,OUTPUT);
}

void loop() 
{
  // put your main code here, to run repeatedly:

   
  for(int i =0 ; i < 7700 ; i++) //going to station
    {
      digitalWrite(CSA2_DP,LOW);
      digitalWrite(CSA2_SP,HIGH);
      delayMicroseconds(300);
      digitalWrite(CSA2_SP,LOW);
      delayMicroseconds(300);
    }
    delay(1000);
    for(int i =0 ; i < 7700 ; i++) //going to station
    {
      digitalWrite(CSA2_DP,HIGH);
      digitalWrite(CSA2_SP,HIGH);
      delayMicroseconds(300);
      digitalWrite(CSA2_SP,LOW);
      delayMicroseconds(300);
    }
    delay(1000);
   //  while(1);
}
