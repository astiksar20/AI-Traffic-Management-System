// =====================================
// LED PINS
// =====================================

const int RED = 13;
const int YELLOW = 14;
const int GREEN = 27;

// =====================================
// SENSOR PINS
// =====================================

const int NEAR_SENSOR = 34;
const int FAR_SENSOR = 32;

// =====================================
// MODES
// =====================================

enum Mode {
  OFF_MODE,
  IDLE_MODE,
  NEAR_MODE,
  FAR_MODE
};

Mode currentMode = IDLE_MODE;

// =====================================
// SETUP
// =====================================

void setup() {

  pinMode(RED, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(GREEN, OUTPUT);

  pinMode(NEAR_SENSOR, INPUT);
  pinMode(FAR_SENSOR, INPUT_PULLUP);

  Serial.begin(115200);

  idleState();
}

// =====================================
// LOOP
// =====================================

void loop() {

  // =====================
  // SERIAL COMMANDS
  // =====================

  if (Serial.available()) {

    char cmd = Serial.read();

    if (cmd == 'g') {

      currentMode = OFF_MODE;
      allOff();
    }

    if (cmd == 'x') {

      currentMode = IDLE_MODE;
      idleState();
    }
  }

  // =====================
  // OFF MODE
  // =====================

  if (currentMode == OFF_MODE) {

    allOff();
    return;
  }

  // =====================
  // IDLE MODE
  // =====================

  if (currentMode == IDLE_MODE) {

    idleState();

    // Near Sensor Trigger

    if (digitalRead(NEAR_SENSOR) == LOW) {

      currentMode = NEAR_MODE;
    }

    // Far Sensor Trigger

    else if (digitalRead(FAR_SENSOR) == LOW) {

      currentMode = FAR_MODE;
    }
  }

  // =====================
  // NEAR MODE
  // =====================

  if (currentMode == NEAR_MODE) {

    nearCycle();
  }

  // =====================
  // FAR MODE
  // =====================

  if (currentMode == FAR_MODE) {

    farCycle();
  }
}

// =====================================
// IDLE STATE
// =====================================

void idleState() {

  digitalWrite(RED, LOW);
  digitalWrite(YELLOW, LOW);
  digitalWrite(GREEN, HIGH);
}

// =====================================
// ALL OFF
// =====================================

void allOff() {

  digitalWrite(RED, LOW);
  digitalWrite(YELLOW, LOW);
  digitalWrite(GREEN, LOW);
}

// =====================================
// CHECK STOP
// =====================================

bool stopRequested() {

  if (Serial.available()) {

    char cmd = Serial.read();

    if (cmd == 'g') {

      currentMode = OFF_MODE;
      allOff();

      return true;
    }
  }

  return false;
}

// =====================================
// NEAR MODE CYCLE
// =====================================

void nearCycle() {

  digitalWrite(GREEN, LOW);

  digitalWrite(RED, HIGH);

  for (int i = 0; i < 100; i++) {

    if (stopRequested()) return;

    delay(100);
  }

  digitalWrite(RED, LOW);

  digitalWrite(GREEN, HIGH);

  for (int i = 0; i < 40; i++) {

    if (stopRequested()) return;

    delay(100);
  }

  digitalWrite(GREEN, LOW);

  digitalWrite(YELLOW, HIGH);

  for (int i = 0; i < 20; i++) {

    if (stopRequested()) return;

    delay(100);
  }

  digitalWrite(YELLOW, LOW);
}

// =====================================
// FAR MODE CYCLE
// =====================================

void farCycle() {

  digitalWrite(GREEN, LOW);

  digitalWrite(RED, HIGH);

  for (int i = 0; i < 40; i++) {

    if (stopRequested()) return;

    delay(100);
  }

  digitalWrite(RED, LOW);

  digitalWrite(GREEN, HIGH);

  for (int i = 0; i < 100; i++) {

    if (stopRequested()) return;

    delay(100);
  }

  digitalWrite(GREEN, LOW);

  digitalWrite(YELLOW, HIGH);

  for (int i = 0; i < 20; i++) {

    if (stopRequested()) return;

    delay(100);
  }

  digitalWrite(YELLOW, LOW);
}