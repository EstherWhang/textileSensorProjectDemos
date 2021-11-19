/*
  Arduino Starter Kit example
  Project 6 - Light Theremin

  This sketch is written to accompany Project 6 in the Arduino Starter Kit

  Parts required:
  - photoresistor
  - 10 kilohm resistor
  - piezo

  created 13 Sep 2012
  by Scott Fitzgerald

  https://store.arduino.cc/genuino-starter-kit

  This example code is part of the public domain.
*/
//edited from above code to work with 

// variable to hold sensor value
int sensorValue;
// variable to calibrate low value
int sensorLow = 300;
// variable to calibrate high value
int sensorHigh = 350;
// LED pin
const int ledPin = 13;

void setup() {
    Serial.begin(9600);
  Serial.setTimeout(1);
  // Make the LED pin an output and turn it on
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  


  // calibrate for the first five seconds after program runs
  while (millis() < 10000) {
    // record the maximum sensor value
    sensorValue = analogRead(A2);
    if (sensorValue > sensorHigh) {
      sensorHigh = sensorValue;
    }
    // record the minimum sensor value
    if (sensorValue < sensorLow) {
      sensorLow = sensorValue;
    }
  }
  if(!Serial.available()){
   Serial.println(sensorLow, DEC);
   Serial.println(sensorHigh, DEC);}
  // turn the LED off, signaling the end of the calibration period
  digitalWrite(ledPin, LOW);
}

void loop() {
  //read the input from A0 and store it in a variable
  sensorValue = analogRead(A2);
  int flippedSensorValue = sensorHigh-sensorValue;
  if (sensorValue > sensorHigh) {
      flippedSensorValue = 0;
    }
  if (sensorValue < sensorLow){
    flippedSensorValue = (sensorHigh);
  }
  
  // map the sensor values to a wide range of pitches
  int pitch = map(flippedSensorValue, 0, sensorHigh, 50, 4000);
  if(!Serial.available()){
    Serial.println(sensorValue, DEC);
    Serial.println(sensorValue, DEC);}

  // play the tone for 20 ms on pin 8
  tone(8, pitch, 20);

  // wait for a moment
  delay(10);
}
