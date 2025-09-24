void setup() {
  Serial.begin(115200);         // Start serial communication
  pinMode(6, OUTPUT);
  analogWriteResolution(12);  // If you're on a board like the Arduino Due
  analogWrite(6, 2048);       // 50% duty cycle on a 12-bit scale
}

void loop() {
  int sensorValue = analogRead(A0);   // Read from analog pin A0
  Serial.println(sensorValue);        // Send the value to the serial monitor
  delay(50);                         // Small delay for readability
}
