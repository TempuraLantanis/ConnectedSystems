#include <Arduino.h>
#include <WiFiClientSecure.h> // Include the WiFiClientSecure library for secure WiFi connections



RAM_ATTR void sendStop()
{
  if (client.connected())
  {
    // Send memssage. Do not use println introduces an empty line )
    client.print("STOP");
    client.flush();
  }
}

void setup(){
  Serial.begin(115200);
  Serial.print("\n Connecting");
  WiFi.begin("Tesla IoT", "fsL6HgjN");
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.print("\nConncected, IP address: ");
  Serial.println(WiFi.localIP());

  // NoodStop
  pinMode(D1, INPUT_PULLUP);
  attachInterrupt(D12, sendStop, FALLING); 
}

