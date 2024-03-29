const int blueButton = 6;
const int redButton = 5;

const int photoPin = A0;    // select the input pin for the potentiometer
int val = 0;       // variable to store the value coming from the sensor

void setup() {
  Serial.begin(9600);

  // Define pin #12 as input and activate the internal pull-up , same for 13
  pinMode(blueButton, INPUT_PULLUP);
  pinMode(redButton, INPUT_PULLUP);
}

void loop() {
  int blueButtonValue = digitalRead(blueButton);
  int redButtonValue = digitalRead(redButton);

  val = analogRead(photoPin);    // read the value from the sensor

  Serial.println(String(blueButtonValue)+","+String(redButtonValue) + "," + val);
  delay(500);
}
