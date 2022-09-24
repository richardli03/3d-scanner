
#include <Servo.h>
Servo pan_servo;
Servo tilt_servo;

const int analogInPin = A4;  // Analog input pin that the potentiometer is attached to
int pan_pos = 0;
int tilt_pos = 10;

int sensorValue = 0;        // value read from the pot

void setup() {
  // initialize serial communications at 9600 bps:
  pan_servo.attach(9);  // attaches the pan servo on pin 9 to the servo object
  tilt_servo.attach(8);  // attaches the tilt servo on pin 10 to the servo object
  Serial.begin(9600);
}

void loop() {  

  Serial.println("starting");
  for(pan_pos = 0; pan_pos <= 90; pan_pos += 1){
   
    for(tilt_pos = 70; tilt_pos < 71; tilt_pos +=1){  
       Serial.print("tilt ");
       Serial.println(tilt_pos);
       sensorValue = analogRead(analogInPin);
       // Serial.print("sensor ");
       Serial.println(sensorValue);
       tilt_servo.write(tilt_pos);
       delay(40);
    }
    Serial.print("pan ");
    Serial.println(pan_pos);
    pan_servo.write(pan_pos);
    delay(100);
  }
  // put your main code here, to run repeatedly:
  

  

  
}
