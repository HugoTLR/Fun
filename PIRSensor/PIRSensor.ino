#include <Arduino.h>
#include <TM1637Display.h>


#define CLK 2
#define DIO 3

//Additional Ground and VCC
#define VCC2  5 // define pin 5 or any other digial pin here as VCC2
#define GND2  4 // define pin 2 or any other digital pin as Ground 2


/*
 * PIR sensor tester
 */
 
int ledPin = 13;                // choose the pin for the LED
int inputPin = 7;               // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;                    // variable for reading the pin status


#define TEST_DELAY  1000        //ms

uint16_t counter = 0;

TM1637Display display(CLK,DIO);

void setup() {

  //PIR SENSOR
  pinMode(ledPin, OUTPUT);      // declare LED as output
  pinMode(inputPin, INPUT);     // declare sensor as input
 
  Serial.begin(9600);

  //DEFINING ADDITIONAL 5V AND GROUND
  pinMode(VCC2,OUTPUT); // Define a digital pin as an output
  digitalWrite(VCC2,HIGH); // set the aboce pin as HIGH for 5V
  pinMode(GND2,OUTPUT); // Define a digital pin as an output
  digitalWrite(GND2,LOW); // set the aboce pin as HIGH for 5V


  // Initializing display
  uint8_t data[] = { 0xff, 0xff, 0xff, 0xff };
  display.setBrightness(0x0f);

  // All segments on
  display.setSegments(data);
  delay(TEST_DELAY);
  
}

void loop() {
  // put your main code here, to run repeatedly:

  val = digitalRead(inputPin);  // read input value
  if (val == HIGH) {            // check if the input is HIGH
    digitalWrite(ledPin, HIGH);  // turn LED ON
    if (pirState == LOW) {
      // we have just turned on
      Serial.println("Motion detected!")
      
      counter += 1;
      display.showNumberDec(counter, true);  // Expect: 0000   
      if (counter >= 10000)
      {
        counter = 1;
      }
      pirState = HIGH;
    }
  } else {
    digitalWrite(ledPin, LOW); // turn LED OFF
    if (pirState == HIGH){
      // we have just turned of
      Serial.println("Motion ended!");
      pirState = LOW;
    }
  }
}
