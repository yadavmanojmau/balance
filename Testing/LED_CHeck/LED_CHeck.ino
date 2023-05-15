
#define sliderLED 37
#define SortingArm1 34
#define SortingArm2 32
#define Conveyor 35
#define Compresor 33
void setup() {
  // put your setup code here, to run once:
 pinMode(sliderLED,OUTPUT);
     pinMode(Compresor,OUTPUT);
     pinMode(SortingArm1,OUTPUT);
     pinMode(SortingArm2,OUTPUT);
     pinMode(Conveyor,OUTPUT);
}

void loop() 
{
  // put your main code here, to run repeatedly:
  digitalWrite(sliderLED,HIGH);
delay(1000);
digitalWrite(Compresor,HIGH);
delay(1000);
digitalWrite(Conveyor,HIGH);
delay(1000);
digitalWrite(SortingArm1,HIGH);
delay(1000);
digitalWrite(SortingArm2,HIGH);
delay(1000);

digitalWrite(sliderLED,LOW);
delay(1000);
digitalWrite(Compresor,LOW);
delay(1000);
digitalWrite(Conveyor,LOW);
delay(1000);
digitalWrite(SortingArm1,LOW);
delay(1000);
digitalWrite(SortingArm2,LOW);
delay(1000);
}
