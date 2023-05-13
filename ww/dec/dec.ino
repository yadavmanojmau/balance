#define enA 5//Enable1 L293 Pin enA 

#define in1 6 //Motor1  L293 Pin in1 

#define in2 7 //Motor1  L293 Pin in1 

#define in3 9 //Motor2  L293 Pin in1 

#define in4 10 //Motor2  L293 Pin in1 

#define enB 8 //Enable2 L293 Pin enB 

#define R_S 4//ir sensor Right

#define L_S 2 //ir sensor Left

void setup(){ 
  Serial.begin(9600);

pinMode(R_S, INPUT); 

pinMode(L_S, INPUT); 

pinMode(enA, INPUT); 

pinMode(in1, OUTPUT); 

pinMode(in2, OUTPUT); 

pinMode(in3, OUTPUT); 

pinMode(in4, OUTPUT); 

pinMode(enB, INPUT);

analogWrite(enA, 250); // Write The Duty Cycle 0 to 255 Enable Pin A for Motor1 Speed 
analogWrite(enB, 250); 

delay(1000);

}

void loop(){  

  int R=digitalRead(R_S);
   Serial.println("R_S" );
   Serial.println(R );
   
   int L=digitalRead(L_S);
   Serial.println("L_S");
   Serial.println(L);

if((digitalRead(R_S) == 0)&&(digitalRead(L_S) == 0)){forward();}   //if Right Sensor and Left Sensor are at White color then it will call forword function

if((digitalRead(R_S) == 1)&&(digitalRead(L_S) == 0)){turnRight();} //if Right Sensor is Black and Left Sensor is White then it will call turn Right function  

if((digitalRead(R_S) == 0)&&(digitalRead(L_S) == 1)){turnLeft();}  //if Right Sensor is White and Left Sensor is Black then it will call turn Left function

if((digitalRead(R_S) == 1)&&(digitalRead(L_S) == 1)){Stop();} //if Right Sensor and Left Sensor are at Black color then it will call Stop function

}

void forward(){  //forword

digitalWrite(in1, HIGH); //Right Motor forword Pin 

digitalWrite(in2, LOW);  //Right Motor backword Pin 

digitalWrite(in3, LOW);  //Left Motor backword Pin 

digitalWrite(in4, HIGH); //Left Motor forword Pin 

analogWrite(enA, 255); // Write The Duty Cycle 0 to 255 Enable Pin A for Motor1 Speed 
analogWrite(enB, 255); 

}

void turnRight(){ //turnRight

digitalWrite(in1, LOW);  //Right Motor forword Pin 

digitalWrite(in2, HIGH); //Right Motor backword Pin  

digitalWrite(in3, LOW);  //Left Motor backword Pin 

 digitalWrite(in4, HIGH); //Left Motor forword Pin 
 
analogWrite(enA, 200); // Write The Duty Cycle 0 to 255 Enable Pin A for Motor1 Speed 
analogWrite(enB, 200);  

}

void turnLeft(){ //turnLeft

digitalWrite(in1, HIGH); //Right Motor forword Pin 

digitalWrite(in2, LOW);  //Right Motor backword Pin 

digitalWrite(in3, HIGH); //Left Motor backword Pin 

digitalWrite(in4, LOW);  //Left Motor forword Pin 

analogWrite(enA, 200); // Write The Duty Cycle 0 to 255 Enable Pin A for Motor1 Speed 
analogWrite(enB, 200); 

}

void Stop(){ //stop

digitalWrite(in1, LOW); //Right Motor forword Pin 

digitalWrite(in2, LOW); //Right Motor backword Pin 

digitalWrite(in3, LOW); //Left Motor backword Pin 

digitalWrite(in4, LOW); //Left Motor forword Pin 
analogWrite(enA, 255); // Write The Duty Cycle 0 to 255 Enable Pin A for Motor1 Speed 
analogWrite(enB, 255); 
}
