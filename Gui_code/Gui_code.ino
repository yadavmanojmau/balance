
#include <Servo.h>
//String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
int pos0 = 102;
int pos180 = 512;


#define debug 1
#define Servo1 3
#define Servo2 5
#define Servo3 6
#define Servo4 9
#define Servo5 0
#define Servo6 11
#define Servo7 2
#define Servo8 12
#define Servo9 13
#define Servo10 8
#define Servo11 10
#define Servo12 A5
#define BT_RX 2
#define BT_TX 4

#define Baud_Rate 9600

#define  pos1start 90 //estimated servo location on powerup
#define  pos1min 1 //minimum allowed 'angle' (must be at least 1)
#define  pos1max 180 //maximum allowed 'angle' (must be 180 max)

#define  pos2start 90
#define  pos2min 1
#define  pos2max 180

#define  pos3start 90
#define  pos3min 1
#define  pos3max 180

#define  pos4start 90
#define  pos4min 1
#define  pos4max 180

#define  pos5start 90
#define  pos5min 1
#define  pos5max 180

#define  pos6start 90
#define  pos6min 1
#define  pos6max 180

#define  pos7start 90
#define  pos7min 1
#define  pos7max 180

#define  pos8start 90
#define  pos8min 1
#define  pos8max 180

#define  pos9start 90
#define  pos9min 1
#define  pos9max 180

#define  pos10start 90
#define  pos10min 1
#define  pos10max 180

#define  pos11start 90
#define  pos11min 1
#define  pos11max 180

#define  pos12start 90
#define  pos12min 1
#define  pos12max 180

//==================================================================================================================================================//
//==================================================================================================================================================//

Servo m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12;

int servo1Completed = 1;
int servo2Completed = 1;
int servo3Completed = 1;
int servo4Completed = 1;
int servo5Completed = 1;
int servo6Completed = 1;
int servo7Completed = 1;
int servo8Completed = 1;
int servo9Completed = 1;
int servo10Completed = 1;
int servo11Completed = 1;
int servo12Completed = 1;
char inChar;
String SreadString = "";
String pos1String, pos2String, pos3String, pos4String, pos5String, pos6String, pos7String, pos8String, pos9String, pos10String, pos11String, pos12String;


int pos1 = pos1start;
int pos2 = pos2start;
int pos3 = pos3start;
int pos4 = pos4start;
int pos5 = pos5start;
int pos6 = pos6start;
int pos7 = pos7start;
int pos8 = pos8start;
int pos9 = pos9start;
int pos10 = pos10start;
int pos11 = pos11start;
int pos12 = pos12start;

int storedPos1 = pos1start; //guestimate of rest
int storedPos2 = pos2start; //guestimate of rest
int storedPos3 = pos3start; //guestimate of rest
int storedPos4 = pos4start; //guestimate of rest
int storedPos5 = pos5start; //guestimate of rest
int storedPos6 = pos6start; //guestimate of rest
int storedPos7 = pos7start; //guestimate of rest
int storedPos8 = pos8start; //guestimate of rest
int storedPos9 = pos9start; //guestimate of rest
int storedPos10 = pos10start; //guestimate of rest
int storedPos11 = pos11start; //guestimate of rest
int storedPos12 = pos12start; //guestimate of rest


void setup() {
  // initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  //SreadString.reserve(200);
  pwm.begin();
  pwm.setPWMFreq(50);
  pwm.setPWM(0, 0, 4096);
  delay(3000);
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    // clear the string:
    CheckIfStopCommand();
    char command = SreadString.charAt(0);
    SreadString.remove(0, 1);
    SerialdataToVariables();
    UpdateServos(command);
    delay(100);
    SreadString = "";
    Serial.print("F");
    stringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    inChar = (char)Serial.read();
    // add it to the inputString:
    SreadString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

//==================================================================================================================================================//
//==================================================================================================================================================//

void CheckIfStopCommand() {
  if (SreadString == "000000000000000000000000000000000000") {
    if (debug == 1) {
      Serial.println(SreadString);
      Serial.println("Servos Stoped");
    }
    m1.detach();
    m2.detach();
    m3.detach();
    m4.detach();
    m5.detach();
    m6.detach();
    m7.detach();
    m8.detach();
    m9.detach();
    m10.detach();
    m11.detach();
    m12.detach();
    SreadString = "";
  }
}

//==================================================================================================================================================//
//==================================================================================================================================================//

void SerialdataToVariables() {
  if (SreadString.length() > 0) {
    pos1String = SreadString;
    pos2String = SreadString;
    pos3String = SreadString;
    pos4String = SreadString;
    pos5String = SreadString;
    pos6String = SreadString;
    pos7String = SreadString;
    pos8String = SreadString;
    pos9String = SreadString;
    pos10String = SreadString;
    pos11String = SreadString;
    pos12String = SreadString;

    pos1String.remove(3, 33);
    pos2String.remove(0, 3);
    pos2String.remove(3, 30);
    pos3String.remove(0, 6);
    pos3String.remove(3, 27);
    pos4String.remove(0, 9);
    pos4String.remove(3, 24);
    pos5String.remove(0, 12);
    pos5String.remove(3, 21);
    pos6String.remove(0, 15);
    pos6String.remove(3, 18);
    pos7String.remove(0, 18);
    pos7String.remove(3, 15);
    pos8String.remove(0, 21);
    pos8String.remove(3, 12);
    pos9String.remove(0, 24);
    pos9String.remove(3, 9);
    pos10String.remove(0, 27);
    pos10String.remove(3, 6);
    pos11String.remove(0, 30);
    pos11String.remove(3, 3);
    pos12String.remove(0, 33);

    pos1 = pos1String.toInt();
    pos2 = pos2String.toInt();
    pos3 = pos3String.toInt();
    pos4 = pos4String.toInt();
    pos5 = pos5String.toInt();
    pos6 = pos6String.toInt();
    pos7 = pos7String.toInt();
    pos8 = pos8String.toInt();
    pos9 = pos9String.toInt();
    pos10 = pos10String.toInt();
    pos11 = pos11String.toInt();
    pos12 = pos12String.toInt();


    if (pos1 < 100) pos1String.remove(0, 1);
    if (pos1 < 010) pos1String.remove(0, 1);
    if (pos2 < 100) pos2String.remove(0, 1);
    if (pos2 < 010) pos2String.remove(0, 1);
    if (pos3 < 100) pos3String.remove(0, 1);
    if (pos3 < 010) pos3String.remove(0, 1);
    if (pos4 < 100) pos4String.remove(0, 1);
    if (pos4 < 010) pos4String.remove(0, 1);
    if (pos5 < 100) pos5String.remove(0, 1);
    if (pos5 < 010) pos5String.remove(0, 1);
    if (pos6 < 100) pos6String.remove(0, 1);
    if (pos6 < 010) pos6String.remove(0, 1);
    if (pos7 < 100) pos7String.remove(0, 1);
    if (pos7 < 010) pos7String.remove(0, 1);
    if (pos8 < 100) pos8String.remove(0, 1);
    if (pos8 < 010) pos8String.remove(0, 1);
    if (pos9 < 100) pos9String.remove(0, 1);
    if (pos9 < 010) pos9String.remove(0, 1);
    if (pos10 < 100) pos10String.remove(0, 1);
    if (pos10 < 010) pos10String.remove(0, 1);
    if (pos11 < 100) pos11String.remove(0, 1);
    if (pos11 < 010) pos11String.remove(0, 1);
    if (pos12 < 100) pos12String.remove(0, 1);
    if (pos12 < 010) pos12String.remove(0, 1);

    pos1 = pos1String.toInt();
    pos2 = pos2String.toInt();
    pos3 = pos3String.toInt();
    pos4 = pos4String.toInt();
    pos5 = pos5String.toInt();
    pos6 = pos6String.toInt();
    pos7 = pos7String.toInt();
    pos8 = pos8String.toInt();
    pos9 = pos9String.toInt();
    pos10 = pos10String.toInt();
    pos11 = pos11String.toInt();
    pos12 = pos12String.toInt();

    /* if(debug == 1){
       Serial.println(SreadString); // DEBUGGING

       Serial.println(pos1);
       Serial.println(pos2);
       Serial.println(pos3);
       Serial.println(pos4);
       Serial.println(pos5);
       Serial.println(pos6);
       Serial.println(pos7);
       Serial.println(pos8);
       Serial.println(pos9);
       Serial.println(pos10);
       Serial.println(pos11);
       Serial.println(pos12);
       }*/
    SreadString = "";

  }
}

void setServo(int servo, int angle) {
  int duty;
  duty = map(angle, 0, 180, pos0, pos180);
  pwm.setPWM(servo, 0, duty);
}
//==================================================================================================================================================//
//==================================================================================================================================================//

void UpdateServos(char command) {
  if (command == 'o') {

    if (pos1 > pos1min - 1 && pos1 < pos1max + 1) { // if within min and max
      if (storedPos1 > pos1) { //if stored position is greater than commanded position
        //servo1Completed = 0;
        //storedPos1--;
        for (int i = storedPos1; i >= pos1 ; i--) {
          m1.attach(Servo1);
          //    m1.write(storedPos1);
          setServo(Servo1, storedPos1 );
          //delay(50);
        }
        storedPos1 = pos1;
      }
      if (storedPos1 < pos1) { //if stored position is less than commanded position
        //servo1Completed = 0;
        //storedPos1++;
        for (int i = storedPos1; i <= pos1 ; i++) {
          m1.attach(Servo1);
          //    m1.write(storedPos1);
          setServo(Servo1, storedPos1 );
          //delay(50);
        }
        storedPos1 = pos1;
      }
    }
    //============================================================================//
    if (pos2 > pos2min - 1 && pos2 < pos2max + 1) { // if within min and max
      if (storedPos2 > pos2) { //if stored position is greater than commanded position
        //servo2Completed = 0;
        //storedPos2--;
        for (int i = storedPos2; i >= pos2; i--) {
          m2.attach(Servo2);
          //    m2.write(storedPos2);
          setServo(Servo2, storedPos2 );
          //delay(50);
        }
        storedPos2 = pos2;
      }
      if (storedPos2 < pos2) { //if stored position is less than commanded position
        //servo2Completed = 0;
        //storedPos2++;
        for (int i = storedPos2; i <= pos2; i++) {
          m2.attach(Servo2);
          //    m2.write(storedPos2);
          setServo(Servo2, storedPos2 );
          //delay(50);
        }
        storedPos2 = pos2;
      }
    }
    //============================================================================//

    if (pos3 > pos3min - 1 && pos3 < pos3max + 1) { // if within min and max
      if (storedPos3 > pos3) { //if stored position is greater than commanded position
        // servo3Completed = 0;
        //storedPos3--;
        for (int i = storedPos3; i >= pos3; i--) {
          m3.attach(Servo3);
          //    m3.write(storedPos3);
          setServo(Servo3, storedPos3 );
          //delay(1);
        }
        storedPos3 = pos3;
      }
      if (storedPos3 < pos3) { //if stored position is less than commanded position
        // servo3Completed = 0;
        //storedPos3++;
        for (int i = storedPos3; i <= pos3; i++) {
          m3.attach(Servo3);
          //          m3.write(storedPos3);
          setServo(Servo3, storedPos3 );
          //delay(1);
        }
        storedPos3 = pos3;
      }
    }
    //============================================================================//

    if (pos4 > pos4min - 1 && pos4 < pos4max + 1) { // if within min and max
      if (storedPos4 > pos4) { //if stored position is greater than commanded position
        //servo4Completed = 0;
        //storedPos4--;
        for (int i = storedPos4; i >= pos4; i--) {
          m4.attach(Servo4);
          //          m4.write(storedPos4);
          setServo(Servo4, storedPos4 );
          //delay(1);
        }
        storedPos4 = pos4;
      }
      if (storedPos4 < pos4) { //if stored position is less than commanded position
        //servo4Completed = 0;
        //storedPos4++;
        for (int i = storedPos4; i <= pos4; i++) {
          m4.attach(Servo4);
          //          m4.write(storedPos4);
          setServo(Servo4, storedPos4 );
          //delay(1);
        }
        storedPos4 = pos4;
      }
    }
    //============================================================================//
    if (pos5 > pos5min - 1 && pos5 < pos5max + 1) { // if within min and max
      if (storedPos5 > pos5) { //if stored position is greater than commanded position
        //servo4Completed = 0;
        //storedPos4--;
        for (int i = storedPos5; i >= pos4; i--) {
          m5.attach(Servo5);
          //          m5.write(storedPos5);
          setServo(Servo5, storedPos5 );
          //delay(1);
        }
        storedPos5 = pos5;
      }
      if (storedPos5 < pos5) { //if stored position is less than commanded position
        //servo4Completed = 0;
        //storedPos4++;
        for (int i = storedPos5; i <= pos5; i++) {
          m5.attach(Servo5);
          //          m5.write(storedPos5);
          setServo(Servo5, storedPos5 );
          //delay(1);
        }
        storedPos5 = pos5;
      }
    }
    //============================================================================//
    if (pos6 > pos6min - 1 && pos6 < pos6max + 1) { // if within min and max
      if (storedPos6 > pos6) { //if stored position is greater than commanded position
        //servo4Completed = 0;
        //storedPos4--;
        for (int i = storedPos6; i >= pos6; i--) {
          m6.attach(Servo6);
          //          m6.write(storedPos6);
          setServo(Servo6, storedPos6 );
          //delay(1);
        }
        storedPos6 = pos6;
      }
      if (storedPos6 < pos6) { //if stored position is less than commanded position
        //servo4Completed = 0;
        //storedPos4++;
        for (int i = storedPos6; i <= pos6; i++) {
          m6.attach(Servo6);
          setServo(Servo6, storedPos6 );
          //          m6.write(storedPos6);
          //delay(1);
        }
        storedPos6 = pos6;
      }
    }
    //============================================================================//
    if (pos7 > pos7min - 1 && pos7 < pos7max + 1) { // if within min and max
      if (storedPos7 > pos7) { //if stored position is greater than commanded position
        //servo4Completed = 0;
        //storedPos4--;
        for (int i = storedPos7; i >= pos7; i--) {
          m7.attach(Servo7);
          //          m7.write(storedPos7);
          setServo(Servo7, storedPos7 );
          //delay(1);
        }
        storedPos7 = pos7;
      }
      if (storedPos7 < pos7) { //if stored position is less than commanded position
        //servo4Completed = 0;
        //storedPos4++;
        for (int i = storedPos7; i <= pos7; i++) {
          m7.attach(Servo7);
          //          m7.write(storedPos7);
          setServo(Servo7, storedPos7 );
          //delay(1);
        }
        storedPos7 = pos7;
      }
    }
    //============================================================================//
    if (pos8 > pos8min - 1 && pos8 < pos8max + 1) { // if within min and max
      if (storedPos8 > pos8) { //if stored position is greater than commanded position
        //servo4Completed = 0;
        //storedPos4--;
        for (int i = storedPos8; i >= pos8; i--) {
          m8.attach(Servo8);
          //          m8.write(storedPos8);
          setServo(Servo8, storedPos8 );
          //delay(1);
        }
        storedPos8 = pos8;
      }
      if (storedPos8 < pos8) { //if stored position is less than commanded position
        //servo4Completed = 0;
        //storedPos4++;
        for (int i = storedPos8; i <= pos8; i++) {
          m8.attach(Servo8);
          setServo(Servo8, storedPos8 );
          //          m8.write(storedPos8);
          //delay(1);
        }
        storedPos8 = pos8;
      }
    }
    //============================================================================//

    if (pos9 > pos9min - 1 && pos9 < pos9max + 1) { // if within min and max
      if (storedPos9 > pos9) { //if stored position is greater than commanded position
        //servo4Completed = 0;
        //storedPos4--;
        for (int i = storedPos9; i >= pos9; i--) {
          m9.attach(Servo9);
          setServo(Servo9, storedPos9 );
          //          m9.write(storedPos9);
          //delay(1);
        }
        storedPos9 = pos9;
      }
      if (storedPos9 < pos9) { //if stored position is less than commanded position
        //servo4Completed = 0;
        //storedPos4++;
        for (int i = storedPos9; i <= pos9; i++) {
          m9.attach(Servo9);
          setServo(Servo9, storedPos9 );
          //          m9.write(storedPos9);
          //delay(1);
        }
        storedPos9 = pos9;
      }
    }
    //============================================================================//

    if (pos10 > pos10min - 1 && pos10 < pos10max + 1) { // if within min and max
      if (storedPos10 > pos10) { //if stored position is greater than commanded position
        //servo4Completed = 0;
        //storedPos4--;
        for (int i = storedPos10; i >= pos10; i--) {
          m10.attach(Servo10);
          setServo(Servo10, storedPos10 );
          //          m10.write(storedPos10);
          //delay(1);
        }
        storedPos10 = pos10;
      }
      if (storedPos10 < pos10) { //if stored position is less than commanded position
        //servo4Completed = 0;
        //storedPos4++;
        for (int i = storedPos10; i <= pos10; i++) {
          m10.attach(Servo10);
          setServo(Servo10, storedPos10 );
          //          m10.write(storedPos10);
          //delay(1);
        }
        storedPos10 = pos10;
      }
    }
    //============================================================================//

    if (pos11 > pos11min - 1 && pos11 < pos11max + 1) { // if within min and max
      if (storedPos11 > pos11) { //if stored position is greater than commanded position
        //servo4Completed = 0;
        //storedPos4--;
        for (int i = storedPos11; i >= pos11; i--) {
          m11.attach(Servo11);
          setServo(Servo11, storedPos11 );
          //          m11.write(storedPos11);
          //delay(1);
        }
        storedPos11 = pos11;
      }
      if (storedPos11 < pos11) { //if stored position is less than commanded position
        //servo4Completed = 0;
        //storedPos4++;
        for (int i = storedPos11; i <= pos11; i++) {
          m11.attach(Servo11);
          setServo(Servo11, storedPos11 );
          //          m11.write(storedPos11);
          //delay(1);
        }
        storedPos11 = pos11;
      }
    }
    //============================================================================//

    if (pos12 > pos12min - 1 && pos12 < pos12max + 1) { // if within min and max
      if (storedPos12 > pos12) { //if stored position is greater than commanded position
        //servo4Completed = 0;
        //storedPos4--;
        for (int i = storedPos12; i >= pos12; i--) {
          m12.attach(Servo12);
          setServo(Servo12, storedPos12 );
          //          m12.write(storedPos12);
          //delay(1);
        }
        storedPos12 = pos12;
      }
      if (storedPos12 < pos12) { //if stored position is less than commanded position
        //servo4Completed = 0;
        //storedPos4++;
        for (int i = storedPos12; i <= pos12; i++) {
          m12.attach(Servo12);
          setServo(Servo12, storedPos12 );
          //          m12.write(storedPos12);
          //delay(1);
        }
        storedPos12 = pos12;
      }
    }
    //============================================================================//
  } else {



    switch (command) {

      case 'a':
        storedPos1 = spinMotor(m1, storedPos1, pos1, Servo1);

        break;
      case 'b':
        storedPos2 = spinMotor(m2, storedPos2, pos2, Servo2);
        break;
      case 'c':
        storedPos3 = spinMotor(m3, storedPos3, pos3, Servo3);
        break;
      case 'd':
        storedPos4 = spinMotor(m4, storedPos4, pos4, Servo4);
        break;
      case 'e':
        storedPos5 = spinMotor(m5, storedPos5, pos5, Servo5);
        break;
      case 'f':
        storedPos6 = spinMotor(m6, storedPos6, pos6, Servo6);
        break;
      case 'g':
        storedPos7 = spinMotor(m7, storedPos7, pos7, Servo7);
        break;
      case 'h':
        storedPos8 = spinMotor(m8, storedPos8, pos8, Servo8);
        break;
    }

  }
}

int spinMotor(Servo motor, int strdPos, int ps, int pin) {

  if (strdPos > ps) { //if stored position is greater than commanded position
    //servo4Completed = 0;
    //storedPos4--;
    for (int i = strdPos; i >= ps; i--) {
      motor.attach(pin);
      //      motor.write(i);
      setServo(pin,i);
      //delay(1);
    }
    strdPos = ps;
  }
  if (strdPos < ps) { //if stored position is less than commanded position
    //servo4Completed = 0;
    //storedPos4++;
    for (int i = strdPos; i <= ps; i++) {
      motor.attach(pin);
      //      motor.write(i);
      setServo(pin,i);
      //delay(1);
    }
    strdPos = ps;
  }
  return strdPos;
}
