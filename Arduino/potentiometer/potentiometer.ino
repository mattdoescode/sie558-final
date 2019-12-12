const int blueButton = 6;
const int redButton = 5;

const int potPin = A0;    // select the input pin for the potentiometer
int val = 0;       // variable to store the value coming from the sensor

int incomingByte = 0;


void setup() {
  Serial.begin(9600);

  // Define pin #12 as input and activate the internal pull-up , same for 13
  pinMode(blueButton, INPUT_PULLUP);
  pinMode(redButton, INPUT_PULLUP);
}

void loop() {

    if (Serial.available() > 0) {
      // read the incoming byte:
      incomingByte = Serial.read();
    
      int blueButtonValue = digitalRead(blueButton);
      int redButtonValue = digitalRead(redButton);
    
      val = analogRead(potPin);    // read the value from the sensor
    
      Serial.println(String(blueButtonValue)+","+String(redButtonValue) + "," + val);
    }
    
}
