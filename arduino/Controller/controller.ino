#include <Bluepad32.h>

#define DRIVE_A  5
#define DRIVE_B  4
#define STEER_A  21
#define STEER_B  22

#define TRIG_FRONT 16
#define ECHO_FRONT 18
#define TRIG_BACK  17
#define ECHO_BACK  19
#define SAFE_DISTANCE 50.0

#define BUZZER 25

ControllerPtr myControllers[BP32_MAX_GAMEPADS];

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
}

void driveBackward() {
  digitalWrite(DRIVE_A, LOW);
  digitalWrite(DRIVE_B, HIGH);
}

void driveStop() {
  digitalWrite(DRIVE_A, LOW);
  digitalWrite(DRIVE_B, LOW);
}

void steerLeft() {
  digitalWrite(STEER_A, HIGH);
  digitalWrite(STEER_B, LOW);
}

void steerRight() {
  digitalWrite(STEER_A, LOW);
  digitalWrite(STEER_B, HIGH);
}

void steerCenter() {
  digitalWrite(STEER_A, LOW);
  digitalWrite(STEER_B, LOW);
}

void onConnectedController(ControllerPtr ctl) {
  Serial.println("Controller verbonden!");
  for (int i = 0; i < BP32_MAX_GAMEPADS; i++) {
    if (myControllers[i] == nullptr) {
      myControllers[i] = ctl;
      break;
    }
  }
}

void onDisconnectedController(ControllerPtr ctl) {
  Serial.println("Controller losgekoppeld!");
  driveStop();
  steerCenter();
  noTone(BUZZER);
  for (int i = 0; i < BP32_MAX_GAMEPADS; i++) {
    if (myControllers[i] == ctl) {
      myControllers[i] = nullptr;
      break;
    }
  }
}

void processController(ControllerPtr ctl) {
  if (!ctl->isConnected() || !ctl->hasData()) return;

  int throttle = ctl->throttle();
  int brake = ctl->brake();
  bool noodstop = false;

  if (throttle > 50) {
    float distance = getDistance(TRIG_FRONT, ECHO_FRONT);
    if (distance > 0 && distance < 50.0) {
      driveStop();
      noodstop = true;
      ctl->playDualRumble(0, 500, 0xff, 0xff);
      Serial.println("NOODSTOP voor: " + String(distance) + "cm");
    } else {
      driveForward();
      Serial.println("Vooruit");
    }
  } else if (brake > 50) {
    float distance = getDistance(TRIG_BACK, ECHO_BACK);
    if (distance > 0 && distance < 50.0) {
      driveStop();
      noodstop = true;
      ctl->playDualRumble(0, 500, 0xff, 0xff);
      Serial.println("NOODSTOP achter: " + String(distance) + "cm");
    } else {
      driveBackward();
      Serial.println("Achteruit");
    }
  } else {
    driveStop();
  }

  if (ctl->a() && !noodstop) {
    tone(BUZZER, 1000);
    ctl->setColorLED(255, 165, 0);
    Serial.println("TOETER!");
  } else if (noodstop) {
    noTone(BUZZER);
    ctl->setColorLED(255, 0, 0);
  } else {
    noTone(BUZZER);
    if (throttle > 50 || brake > 50) {
      ctl->setColorLED(0, 255, 0);
    } else {
      ctl->setColorLED(0, 0, 255);
    }
  }

  int axisX = ctl->axisX();
  if (axisX < -50) {
    steerLeft();
  } else if (axisX > 50) {
    steerRight();
  } else {
    steerCenter();
  }
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
  pinMode(BUZZER, OUTPUT);

  driveStop();
  steerCenter();
  noTone(BUZZER);

  BP32.setup(&onConnectedController, &onDisconnectedController);
  BP32.forgetBluetoothKeys();

  Serial.println("Bluepad32 gestart, wacht op controller...");
}

void loop() {
  BP32.update();

  for (auto ctl : myControllers) {
    if (ctl && ctl->isConnected()) {
      processController(ctl);
    }
  }

  delay(10);
}