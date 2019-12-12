const int red1 = 53;
const int blue1 = 51;
const int red2 = 49;
const int blue2 = 47;
const int red3 = 45;
const int blue3 = 43;
const int red4 = 41;
const int blue4  = 39;

const int trigPin = 40;
const int echoPin = 38;

const int pot = A0;
const int photo = A1;
const int mic = A2; 


float duration, distance;

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  pinMode(red1, INPUT_PULLUP);
  pinMode(blue1, INPUT_PULLUP);
  pinMode(red2, INPUT_PULLUP);
  pinMode(blue2, INPUT_PULLUP);
  pinMode(red3, INPUT_PULLUP);
  pinMode(blue3, INPUT_PULLUP);
  pinMode(red4, INPUT_PULLUP);
  pinMode(blue4, INPUT_PULLUP);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  int blueButtonValue1 = digitalRead(blue1);
  int redButtonValue1 = digitalRead(red1);

  int blueButtonValue2 = digitalRead(blue2);
  int redButtonValue2 = digitalRead(red2);

  int blueButtonValue3 = digitalRead(blue3);
  int redButtonValue3 = digitalRead(red3);

  int blueButtonValue4 = digitalRead(blue4);
  int redButtonValue4 = digitalRead(red4);

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = (duration * .0343) / 2;

  Serial.print(String(redButtonValue1) + "," +  String(blueButtonValue1) + "," + String(redButtonValue2) + "," + String(blueButtonValue2) + "," + String(redButtonValue3) + "," + String(blueButtonValue3) + "," + String(redButtonValue4) + "," + String(blueButtonValue4));
  Serial.println(","+String(analogRead(pot))+","+String(analogRead(photo))+","+String(analogRead(mic))+","+String(distance));
}
