// =====================================
// NORTH SIGNAL
// =====================================

int N_RED = 4;
int N_YELLOW = 7;
int N_GREEN = 12;

// =====================================
// SOUTH SIGNAL
// =====================================

int S_RED = 8;
int S_YELLOW = 10;
int S_GREEN = 11;

// =====================================
// GLOBAL STATUS
// =====================================

String congestionStatus = "";

// =====================================
// SETUP
// =====================================

void setup() {

  pinMode(N_RED, OUTPUT);
  pinMode(N_YELLOW, OUTPUT);
  pinMode(N_GREEN, OUTPUT);

  pinMode(S_RED, OUTPUT);
  pinMode(S_YELLOW, OUTPUT);
  pinMode(S_GREEN, OUTPUT);

  Serial.begin(9600);

  allLightsOff();
}

// =====================================
// CHECK STOP COMMAND
// =====================================

bool stopReceived() {

  if (Serial.available()) {

    String cmd = Serial.readStringUntil('\n');

    cmd.trim();

    if (cmd == "STOP") {

      congestionStatus = "STOP";

      allLightsOff();

      return true;
    }
  }

  return false;
}

// =====================================
// LOOP
// =====================================

void loop() {

  if (Serial.available()) {

    congestionStatus =
      Serial.readStringUntil('\n');

    congestionStatus.trim();
  }

  // =====================================
  // ANALYZING MODE
  // =====================================

  if (congestionStatus == "ANALYZING") {

    allLightsOff();

    digitalWrite(N_GREEN, HIGH);
    digitalWrite(S_GREEN, HIGH);
  }

  // =====================================
  // HIGH CONGESTION
  // =====================================

  else if (congestionStatus == "HIGH") {

    highCongestionCycle();
  }

  // =====================================
  // LOW CONGESTION
  // =====================================

  else if (congestionStatus == "LOW") {

    lowCongestionCycle();
  }

  // =====================================
  // STOP
  // =====================================

  else if (congestionStatus == "STOP") {

    allLightsOff();

    congestionStatus = "";
  }

  else {

    allLightsOff();
  }
}

// =====================================
// LOW CONGESTION
// RED LONGER
// =====================================

void lowCongestionCycle() {

  // RED

  digitalWrite(N_RED, HIGH);
  digitalWrite(S_RED, HIGH);

  digitalWrite(N_YELLOW, LOW);
  digitalWrite(S_YELLOW, LOW);

  digitalWrite(N_GREEN, LOW);
  digitalWrite(S_GREEN, LOW);

  for (int i = 0; i < 100; i++) {

    if (stopReceived()) return;

    delay(100);
  }

  // GREEN

  digitalWrite(N_RED, LOW);
  digitalWrite(S_RED, LOW);

  digitalWrite(N_GREEN, HIGH);
  digitalWrite(S_GREEN, HIGH);

  for (int i = 0; i < 50; i++) {

    if (stopReceived()) return;

    delay(100);
  }

  // YELLOW

  digitalWrite(N_GREEN, LOW);
  digitalWrite(S_GREEN, LOW);

  digitalWrite(N_YELLOW, HIGH);
  digitalWrite(S_YELLOW, HIGH);

  for (int i = 0; i < 20; i++) {

    if (stopReceived()) return;

    delay(100);
  }

  digitalWrite(N_YELLOW, LOW);
  digitalWrite(S_YELLOW, LOW);
}

// =====================================
// HIGH CONGESTION
// GREEN LONGER
// =====================================

void highCongestionCycle() {

  // RED

  digitalWrite(N_RED, HIGH);
  digitalWrite(S_RED, HIGH);

  digitalWrite(N_YELLOW, LOW);
  digitalWrite(S_YELLOW, LOW);

  digitalWrite(N_GREEN, LOW);
  digitalWrite(S_GREEN, LOW);

  for (int i = 0; i < 50; i++) {

    if (stopReceived()) return;

    delay(100);
  }

  // GREEN

  digitalWrite(N_RED, LOW);
  digitalWrite(S_RED, LOW);

  digitalWrite(N_GREEN, HIGH);
  digitalWrite(S_GREEN, HIGH);

  for (int i = 0; i < 120; i++) {

    if (stopReceived()) return;

    delay(100);
  }

  // YELLOW

  digitalWrite(N_GREEN, LOW);
  digitalWrite(S_GREEN, LOW);

  digitalWrite(N_YELLOW, HIGH);
  digitalWrite(S_YELLOW, HIGH);

  for (int i = 0; i < 20; i++) {

    if (stopReceived()) return;

    delay(100);
  }

  digitalWrite(N_YELLOW, LOW);
  digitalWrite(S_YELLOW, LOW);
}

// =====================================
// ALL LIGHTS OFF
// =====================================

void allLightsOff() {

  digitalWrite(N_RED, LOW);
  digitalWrite(N_YELLOW, LOW);
  digitalWrite(N_GREEN, LOW);

  digitalWrite(S_RED, LOW);
  digitalWrite(S_YELLOW, LOW);
  digitalWrite(S_GREEN, LOW);
}