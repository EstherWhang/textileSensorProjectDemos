void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(1);
  pinMode(A0, INPUT);

}

void loop()
{
  //this is for testing purposes

  if(!Serial.available()){
    
    Serial.println(analogRead(A0), DEC);
    delay(100);}

}
