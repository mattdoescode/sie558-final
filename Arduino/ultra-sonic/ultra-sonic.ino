const int blueButton = 6;
const int redButton = 5;

const int trigPin = 9;
const int echoPin = 10;

float duration, distance;

void setup() {
  Serial.begin(9600);

  // Define pin #12 as input and activate the internal pull-up , same for 13
  pinMode(blueButton, INPUT_PULLUP);
  pinMode(redButton, INPUT_PULLUP);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  int blueButtonValue = digitalRead(blueButton);
  int redButtonValue = digitalRead(redButton);

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = (duration * .0343) / 2;

  Serial.println(String(blueButtonValue) + "," + String(redButtonValue) + "," + distance);
}
