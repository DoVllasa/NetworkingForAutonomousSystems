#include <Wire.h>

int ledBlue = 13;                      // definiere Variable für Pin 13
int ledRed  = 12;                      // definiere Variable für Pin 12
int ledGreen = 11;     

void setup() {
  pinMode(ledBlue, OUTPUT);              //
  pinMode(ledRed, OUTPUT);             // definiere die LEDs als Ausgänge
  pinMode(ledGreen, OUTPUT);     
  
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void loop() {
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  Serial.println("Received: "); 
  String message = "";
  while (Wire.available() > 0) {
    char c = Wire.read(); 
    message += c;
    Serial.println(c); 
  }

  String led = getValue(message, ':', 0);
  String value = getValue(message, ':', 1);

  if (led == "red"){
    analogWrite(ledRed, value.toInt() -1);
  }else if (led == "green"){
    analogWrite(ledGreen, value.toInt() -1);
  }else if (led == "blue"){
    analogWrite(ledBlue, value.toInt() -1);
  }
}

String getValue(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
