#include <Servo.h>

//servo PWM
#define SERVO1_PIN 9  
#define SERVO2_PIN 8 
#define SERVO3_PIN 7  
#define SERVO4_PIN 6
#define SERVO5_PIN 5
#define SERVO6_PIN 4

Servo myservo1 ;  //eyes
Servo myservo2 ;  //lids
Servo myservo3 ;  //brows
Servo myservo4 ;  //brows
Servo myservo5 ;  //mouth
Servo myservo6 ;  //nostrils

void setup() {
  Serial.begin(9600);

//servos
 myservo1.attach(9);
 myservo2.attach(8);
 myservo3.attach(7);
 myservo4.attach(6);
 myservo5.attach(5);
 myservo6.attach(4);
 
}

void loop() {
  if (Serial.available() > 0) {
    int emotionCode = Serial.read() - '0';

    // Process the received emotion code
    processEmotion(emotionCode);
  }
}

void processEmotion(int emotionCode) {
  // Define servo positions for each emotion code
  int myservo1Pos, myservo2Pos, myservo3Pos, myservo4Pos, myservo5Pos, myservo6Pos;

  switch (emotionCode) {
    case 1://angry
      myservo2.write(51);
      myservo3.write(20);
      myservo4.write(140);
      myservo6.write(90);
      myservo1.write(140);
      delay(500);
      myservo1.write(90);
      delay(1500);
      break;
    case 2: //sad
      myservo2.write(51);
      myservo3.write(90);
      myservo4.write(45);
      myservo6.write(90);
      myservo1.write(110);
      delay(500);
      myservo1.write(140);
      delay(1500); 
      break;
    case 3: //shocked
      myservo2.write(151);
      myservo3.write(90);
      myservo4.write(45);
      myservo6.write(90);
      myservo5.write(40);
      delay(1500); 
      break;
    case 4: //scared
      myservo2.write(120);
      myservo3.write(70);
      myservo4.write(70);
      myservo6.write(90);
      myservo5.write(40);
      myservo1.write(90);
      delay(100);
      myservo1.write(140);
      delay(1500); 
      myservo5.write(700);
      break;
    case 5: //uneasy
      myservo2.write(120);
      myservo3.write(70);
      myservo6.write(90);
      myservo1.write(140);
      delay(500);
      myservo1.write(90);
      delay(100);
      myservo3.write(50);
      myservo4.write(50);
      delay(1000); 
      break;
    case 6: //unknown
      myservo1.write(90);
      myservo3.write(700);
      delay(200);
      myservo1.write(140);
      myservo2.write(151);
      myservo4.write(90);
      delay(200);
      myservo1.write(90);
      delay(200);
      myservo1.write(140);
      myservo5.write(90);
      delay(200);
      myservo1.write(90);
      myservo2.write(51);
      delay(200);
      myservo1.write(140);
      myservo5.write(45);
      delay(1500); 
      break;
    default: //rest face
      myservo1.write(0);
      myservo2.write(0);
      myservo3.write(0);
      myservo4.write(0);
      myservo5.write(0);
      myservo6.write(0);
  }



  // Delay
  delay(1000);
  
  // Reset servos to a neutral position
  resetServos();
}

void resetServos() {
   myservo1.write(0);
   myservo2.write(0);
   myservo3.write(0);
   myservo4.write(0);
   myservo5.write(0);
   myservo6.write(0);
  
  delay(500);
}
