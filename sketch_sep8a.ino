#include <Servo.h>

Servo radarServo;

// Pin numbers
int servoPin = 9;
int trigPin = 6;
int echoPin = 3;

// Variables
int angle;
int distance;
long echoTime;

void setup() {
  Serial.begin(9600);

  radarServo.attach(servoPin);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {

  // Move servo from 15° to 165°
  for (angle = 15; angle <= 165; angle++) {

    radarServo.write(angle);
    delay(30);

    distance = measureDistance();

    sendData();
  }

  // Move servo from 165° back to 15°
  for (angle = 165; angle >= 15; angle--) {

    radarServo.write(angle);
    delay(30);

    distance = measureDistance();

    sendData();
  }
}

// Measure distance using ultrasonic sensor
int measureDistance() {

  // Send ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);

  // Measure echo time
  echoTime = pulseIn(echoPin, HIGH);

  // Convert time into distance
  int measuredDistance = echoTime * 0.034 / 2;

  // Processing displays objects only within 50 cm
  if (measuredDistance > 50 || measuredDistance <= 0) {
    measuredDistance = 999;
  }

  return measuredDistance;
}

// Send angle and distance to Processing
void sendData() {

  Serial.print(angle);
  Serial.print(",");
  Serial.println(distance);
}
