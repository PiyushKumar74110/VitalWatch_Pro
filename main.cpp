#include <Arduino.h>
#include <DHT.h>

//DHT SENSOR DEFINING
#define DHTPIN 7        
#define DHTTYPE DHT11 
DHT dht(DHTPIN, DHTTYPE);

//SENSOR PINS
#define FLAME_PIN 8
#define LIGHT_PIN A0
#define SOUND_PIN A1
#define SHOCK_PIN 2
#define BALL_PIN 3
#define REED_PIN 4
#define TOUCH_PIN 5

void setup() {
  Serial.begin(9600);
  delay(1000);

  dht.begin();

  pinMode(FLAME_PIN, INPUT);
  pinMode(SHOCK_PIN, INPUT);
  pinMode(BALL_PIN, INPUT);
  pinMode(REED_PIN, INPUT);
  pinMode(TOUCH_PIN, INPUT);
}

void loop() {
  // Reading DHT Sensor Data
  float tempC = dht.readTemperature();
  int hum = dht.readHumidity();

  // Validating DHT sensor data
  if (isnan(tempC) || isnan(hum)) {
    Serial.println("Failed to read from DHT sensor!");
    // return;
  }

  // Read Data from Sensors
  String flame = digitalRead(FLAME_PIN) == HIGH ? "Fire Detected" : "No fire";
  String light = analogRead(LIGHT_PIN) > 35 ? "Bright" : "Dark";
  String sound = analogRead(SOUND_PIN) > 960 ? "Loud" : "Normal";
  String shock = digitalRead(SHOCK_PIN) == LOW ? "Impact" : "No impact";
  String ball = digitalRead(BALL_PIN) == HIGH ? "Active" : "Inactive";
  String reed = digitalRead(REED_PIN) == LOW ? "Closed" : "Open";
  String touch = digitalRead(TOUCH_PIN) == HIGH ? "Touched" : "No touch";

  // Changing format of data sent by arduino to string and Sending to Pyhton code
  String data = "TEMP:" + String(tempC, 1) + "°C" +
                ",HUM:" + String(hum) + "%" +
                ",FLAME:" + flame +
                ",LIGHT:" + light +
                ",SOUND:" + sound +
                ",SHOCK:" + shock +
                ",BALL:" + ball +
                ",REED:" + reed +
                ",TOUCH:" + touch;

  Serial.println(data);
  delay(100);
}                                                                                                                                                                               