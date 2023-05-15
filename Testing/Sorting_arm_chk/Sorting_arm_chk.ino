#define CSA1_DP 26 
#define CSA1_SP 27

void setup() 
{
  // put your setup code here, to run once:
  pinMode(CSA1_DP,OUTPUT);
  pinMode(CSA1_SP,OUTPUT);

}

void loop() 
{
  // put your main code here, to run repeatedly:
  for(int i =0 ; i < 7600 ; i++) //going to sort
    {
      digitalWrite(CSA1_DP,HIGH);
      digitalWrite(CSA1_SP,HIGH);
      delayMicroseconds(300);
      digitalWrite(CSA1_SP,LOW);
      delayMicroseconds(300);
    }

    delay(1000);
  for(int i =0 ; i < 7600 ; i++) //going to sort
    {
      digitalWrite(CSA1_DP,LOW);
      digitalWrite(CSA1_SP,HIGH);
      delayMicroseconds(300);
      digitalWrite(CSA1_SP,LOW);
      delayMicroseconds(300);
    }
     delay(1000);
    //while(1);

}
