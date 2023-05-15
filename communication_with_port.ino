int led =13;
int  data;
void setup() {
Serial.begin(9600);
pinMode(led,OUTPUT);

}

void loop() {
  
  while(Serial.available())
  {
    data=Serial.read();
     }
   if(data=='1')
    {
      digitalWrite(led,1);
     Serial.println("led is on");
      }
    else if(data=='0')
     {
      digitalWrite(led,0);
     Serial.println("led is off");
        }
}
