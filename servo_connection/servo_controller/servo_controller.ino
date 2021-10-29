#include <Servo.h>
Servo servo;
String serial_read;
String Temp;
float angle;

void setup()
{
  servo.attach(9);
  Serial.begin(9600);
  Serial.setTimeout(1);
  pinMode(A0, INPUT);

}

void loop()
{
  //this is for testing purposes

  if(!Serial.available()){
    
    Serial.println(analogRead(A0), DEC);
    delay(100);
  
    serial_read = Serial.readString();
    Temp = serial_read;
    if(Temp.startsWith("a")){
      angle = Temp.substring(1).toFloat();
      servo.write(angle);
    }
    

  }
}
