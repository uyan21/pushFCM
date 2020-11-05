#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#define PORT 80/*수정*/
const char* ssid  = "ssid";/*수정*/
const char* password = "pw";/*수정*/
const char* server = "url";/*수정*/
String jsondata="";
StaticJsonBuffer<200> jsonBuffer;/*Json 클래스 할당*/
JsonObject&root=jsonBuffer.createObject();
int val[]={30,40,50,60,70,80,55,90,40,20,45,60,90,120,151,160,140,130,120,90,95};
void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    }
  Serial.println("");
  Serial.println("MCU has been connected.");
  Serial.println("Router name : "+String(ssid));  
  Serial.print("Allocated IP address from Router is ");
  Serial.println(WiFi.localIP());
}
void loop() {
  for (int i=0;i<sizeof(val)/ sizeof(int);i++){
act(1000,val[i]);/*매개변수가 딜레이*/
  }
}

void act(int del,int data){
  WiFiClient client;
  delay(del);
if(client.connect(server,PORT)){
  /*형식
    POST / HTTP/1.1
    Host: URL
    Connextion: close
    Content-Type: application/json
    Content-Length: sizeof(jsondata)
    jsondata
    */
  root["flow"]=data;
  root.printTo(jsondata);
  Serial.println(jsondata);
  String s="Host: "+String(server);
  client.println("POST /dstack HTTP/1.1");
  client.println(s);
  client.println("Connection: close");
  client.println("Content-Type: application/json");
  client.print("Content-Length: ");
  client.println(jsondata.length());
  client.println();
  client.println(jsondata);
  Serial.println("Free Heap: "+String(ESP.getFreeHeap()));
  jsondata="";
  
    }
    else{Serial.println("NO");}
    }
