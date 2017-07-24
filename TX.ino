
#include <SoftwareSerial.h> 
#define BUFSIZE 128
SoftwareSerial loraSerial(10, 11);
String str;

void setup() {
  //output LED pin
  pinMode(13, OUTPUT);

  // Open serial communications and wait for port to open:

  Serial.begin(57600);

  loraSerial.begin(9600);
  loraSerial.setTimeout(1000);
  lora_autobaud();

  delay(1000);

  Serial.println("Initing LoRa");

  loraSerial.listen();
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);
  loraSerial.println("sys get ver");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("mac pause");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);
  loraSerial.println("radio set mod lora");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);


  loraSerial.println("radio set freq 868100000");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("radio set pwr 14");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("radio set sf sf7");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("radio set afcbw 41.7");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("radio set rxbw 250");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  //  loraSerial.println("radio set bitrate 50000");
  //  wait_for_ok();

  //  loraSerial.println("radio set fdev 25000");
  //  wait_for_ok();

  loraSerial.println("radio set prlen 8");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("radio set crc on");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("radio set iqi off");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("radio set cr 4/5");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("radio set wdt 60000"); 
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("radio set sync 12");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  loraSerial.println("radio set bw 125");
  str = loraSerial.readStringUntil('\n');
  Serial.println(str);

  Serial.println("starting loop");
}

void loop() {
  // Check for user input
  char n, inputs[BUFSIZE + 1];

  if (Serial.available()) {
    n = Serial.readBytes(inputs, BUFSIZE);
    inputs[n] = 0;
    // Send characters to Bluefruit
    //Serial.print("Sending: ");
    //Serial.println(inputs);
    String cmd = "radio tx " + String(inputs);
    Serial.println(cmd);
    // Send input data to host via 
    loraSerial.println(cmd);
    str = loraSerial.readStringUntil('\n');
    Serial.println(str);
    str = loraSerial.readStringUntil('\n');
    Serial.println(str);
  } else {

    loraSerial.println("radio tx AA");
    str = loraSerial.readStringUntil('\n');
    Serial.println(str);
    str = loraSerial.readStringUntil('\n');
    Serial.println(str);
  }
  delay(5000);
}

void lora_autobaud() {
  String response = "";
  while (response == "") {
    delay(1000);
    loraSerial.write((byte) 0x00);
    loraSerial.write(0x55);
    loraSerial.println();
    loraSerial.println("sys get ver");
    response = loraSerial.readStringUntil('\n');
  }
}


int wait_for_ok() {
  str = loraSerial.readStringUntil('\n');
  if (str.indexOf("ok") == 0) {
    return 1;
  } else return 0;
}
