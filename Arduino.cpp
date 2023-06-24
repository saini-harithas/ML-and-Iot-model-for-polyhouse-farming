/* Code for  Arduino */

#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include<dht.h>
#include<time.h>
dht DHT;

#define FIREBASE_HOST "arduinodata-83659.firebaseio.com"
#define FIREBASE_AUTH "eA4E0x8TN1qbFUmdBLZB5n6xkfpWgftWhAL7uJoS"
#define WIFI_SSID "Manohar"
#define WIFI_PASSWORD "12345678"

int timezone = 19800;
int dst = 0;

void setup() {
  Serial.begin(9600);
  pinMode(A0,INPUT);
  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  configTime(timezone, dst, "pool.ntp.org","time.nist.gov");
  Serial.println("\n Waiting for Internet time");

  while(!time(nullptr)){
    Serial.print("*");
    delay(1000);
    }
    
    Serial.println("Time response ....OK");
  
}

int n = 0;

void loop() {
 if(n!=0){                                   // if n==0 if prints 1970 date
 
  time_t now = time(nullptr);                // Date Time
  struct tm* p_tm = localtime(&now);
  int x1=p_tm->tm_mday;
  int y1=p_tm->tm_mon + 1;
  int z1=p_tm->tm_year + 1900;
String s1=String(x1)+"-"+String(y1)+"-"+String(z1);
  int x2=p_tm->tm_hour;
  int y2=p_tm->tm_min;
  int z2=p_tm->tm_sec;
String s2=String(x2)+":"+String(y2)+":"+String(z2);
String s3=s1+"  "+s2;
  Serial.println(s3);

 
 int x=DHT.read11(4);                                  // DHT
 Serial.println("temperature");
 Serial.println(DHT.temperature,1);
 Serial.println("humidity");
 Serial.println(DHT.humidity,1);
 
 
 float moist;                                         // Soil Moisture
 int anlread= analogRead(A0);
 moist=(100-((anlread/1024.00)*100));
 Serial.println("Moisture Percentage");
 Serial.println(moist);
 Serial.println();



  Firebase.pushFloat(s1+"/"+s2+"/Temperature", DHT.temperature);
  // handle error
  if (Firebase.failed()) {
      Serial.print("setting /number failed:");
      Serial.println(Firebase.error());  
      return;
  }
  
  
  Firebase.pushFloat(s1+"/"+s2+"/Humidity", DHT.humidity);
  // handle error
  if (Firebase.failed()) {
      Serial.print("setting /number failed:");
      Serial.println(Firebase.error());  
      return;
  }

  Firebase.pushFloat(s1+"/"+s2+"/SoilMoist", moist);
  // handle error
  if (Firebase.failed()) {
      Serial.print("setting /number failed:");
      Serial.println(Firebase.error());  
      return;
  }


  
  }
  n=n+1;
  delay(1000);
