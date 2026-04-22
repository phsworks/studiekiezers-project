#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

const char* ssid     = "Michiel de Router";
const char* password = "***REMOVED***";

#define DRIVE_A  4
#define DRIVE_B  5
#define STEER_A  6
#define STEER_B  7

#define TRIG_FRONT 16
#define ECHO_FRONT 18
#define TRIG_BACK  17
#define ECHO_BACK  19
#define SAFE_DISTANCE 30.0

WebServer server(80);

String driveState = "stop";
String steerState = "center";

float getDistance(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH, 5000);
  return duration * 0.034 / 2;
}

void driveForward() {
  digitalWrite(DRIVE_A, HIGH);
  digitalWrite(DRIVE_B, LOW);
  driveState = "forward";
}

void driveBackward() {
  digitalWrite(DRIVE_A, LOW);
  digitalWrite(DRIVE_B, HIGH);
  driveState = "backward";
}

void driveStop() {
  digitalWrite(DRIVE_A, LOW);
  digitalWrite(DRIVE_B, LOW);
  driveState = "stop";
}

void steerLeft() {
  digitalWrite(STEER_A, HIGH);
  digitalWrite(STEER_B, LOW);
  steerState = "left";
}

void steerRight() {
  digitalWrite(STEER_A, LOW);
  digitalWrite(STEER_B, HIGH);
  steerState = "right";
}

void steerCenter() {
  digitalWrite(STEER_A, LOW);
  digitalWrite(STEER_B, LOW);
  steerState = "center";
}

void handleDrive() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");

  if (!server.hasArg("cmd")) {
    server.send(400, "application/json", "{\"error\":\"missing cmd parameter\"}");
    return;
  }

  String cmd = server.arg("cmd");
  cmd.toLowerCase();

  if      (cmd == "forward")  driveForward();
  else if (cmd == "backward") driveBackward();
  else if (cmd == "stop")     driveStop();
  else if (cmd == "left")     steerLeft();
  else if (cmd == "right")    steerRight();
  else if (cmd == "center")   steerCenter();
  else {
    server.send(400, "application/json", "{\"error\":\"unknown command\"}");
    return;
  }

  String json = "{\"ok\":true,\"cmd\":\"" + cmd + "\",\"drive\":\"" + driveState + "\",\"steer\":\"" + steerState + "\"}";
  server.send(200, "application/json", json);
  Serial.println("CMD: " + cmd);
}

void handleStatus() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  float distFront = getDistance(TRIG_FRONT, ECHO_FRONT);
  float distBack = getDistance(TRIG_BACK, ECHO_BACK);
  String json = "{\"drive\":\"" + driveState + "\",\"steer\":\"" + steerState + "\",\"ip\":\"" + WiFi.localIP().toString() + "\",\"distance_front\":" + String(distFront) + ",\"distance_back\":" + String(distBack) + "}";
  server.send(200, "application/json", json);
}

void handleRoot() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  String html = R"(
    <html><body style='font-family:sans-serif;padding:20px;background:#111;color:#eee'>
    <h2>🚗 RC Car API</h2>
    <p>Send GET requests to control the car:</p>
    <ul>
      <li><a href='/drive?cmd=forward' style='color:#4ade80'>/drive?cmd=forward</a></li>
      <li><a href='/drive?cmd=backward' style='color:#4ade80'>/drive?cmd=backward</a></li>
      <li><a href='/drive?cmd=stop' style='color:#4ade80'>/drive?cmd=stop</a></li>
      <li><a href='/drive?cmd=left' style='color:#4ade80'>/drive?cmd=left</a></li>
      <li><a href='/drive?cmd=right' style='color:#4ade80'>/drive?cmd=right</a></li>
      <li><a href='/drive?cmd=center' style='color:#4ade80'>/drive?cmd=center</a></li>
      <li><a href='/status' style='color:#4ade80'>/status</a></li>
    </ul>
    </body></html>
  )";
  server.send(200, "text/html", html);
}

void setup() {
  Serial.begin(115200);

  pinMode(DRIVE_A, OUTPUT);
  pinMode(DRIVE_B, OUTPUT);
  pinMode(STEER_A, OUTPUT);
  pinMode(STEER_B, OUTPUT);
  pinMode(TRIG_FRONT, OUTPUT);
  pinMode(ECHO_FRONT, INPUT);
  pinMode(TRIG_BACK, OUTPUT);
  pinMode(ECHO_BACK, INPUT);

  driveStop();
  steerCenter();

  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Connected!");
  Serial.print("Your API is at: http://");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/drive", handleDrive);
  server.on("/status", handleStatus);
  server.begin();

  Serial.println("API server started!");
}

void loop() {
  server.handleClient();

  if (driveState == "forward") {
    float distance = getDistance(TRIG_FRONT, ECHO_FRONT);
    if (distance > 0 && distance < SAFE_DISTANCE) {
      driveStop();
      Serial.println("NOODSTOP voor: " + String(distance) + "cm");
    }
  }

  if (driveState == "backward") {
    float distance = getDistance(TRIG_BACK, ECHO_BACK);
    if (distance > 0 && distance < SAFE_DISTANCE) {
      driveStop();
      Serial.println("NOODSTOP achter: " + String(distance) + "cm");
    }
  }
}