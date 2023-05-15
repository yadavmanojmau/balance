#define mo 38       //Compresor pins
#define de 39
#define Compresor 33

void setup() 
{
  // put your setup code here, to run once:
pinMode(mo,OUTPUT);
pinMode(de,OUTPUT);
pinMode(Compresor,OUTPUT);
}

void loop() 
{

//one();
//
two();
delay(3  000);
one();
delay(2000);
}
void one()
{
   digitalWrite(mo,HIGH);
 digitalWrite(de,HIGH);
 digitalWrite(Compresor,HIGH);
}

void two()
{
  
  // put your main code here, to run repeatedly:
 digitalWrite(mo,LOW);
 digitalWrite(de,LOW);
 digitalWrite(Compresor,LOW);
 
}
