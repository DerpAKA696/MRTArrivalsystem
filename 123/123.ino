void setup() {
  Serial.begin(9600);
  pinMode(13,OUTPUT);
}
void loop() {
  if(Serial.available()>0)
  {
    int tmp = Serial.read()-48;
    if(tmp==1)
    {
      for(int i=0;i<100000;i++)
      {
        digitalWrite(13,HIGH);
        delay(1000);
        digitalWrite(13,LOW);
        delay(1000);
      }
    }
  }
}