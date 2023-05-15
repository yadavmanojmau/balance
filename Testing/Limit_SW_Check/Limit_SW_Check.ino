
#define Limit1 3    
#define Limit2 2

void setup() 
{
  // put your setup code here, to run once:
  Serial.begin(9600);
 pinMode(Limit1,INPUT_PULLUP);
    pinMode(Limit2,INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
  int Lim1= digitalRead(Limit1);
  int Lim2= digitalRead(Limit2);

  Serial.print("Lim1:- ");
  Serial.print(Lim1);
  Serial.print("               ");
  Serial.print("Lim2:- ");
  Serial.print(Lim2);
  Serial.println("               ");
}
