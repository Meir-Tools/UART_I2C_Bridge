#include <Wire.h>

#define BUFFER_SIZE 32

void setup() {
  Wire.begin(); // Master
  Serial.begin(115200);
  Serial.println("Ready: W:<slave>:<reg>:<value> or R:<slave>:<reg>:<num_bytes> or S:");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.startsWith("W:")) {
      // Parse: W:<slave_addr>:<reg_addr>:<data>
      int p1 = input.indexOf(':', 2);
      int p2 = input.indexOf(':', p1 + 1);
      if (p1 > 0 && p2 > p1) {
        String slaveStr = input.substring(2, p1);
        String regStr = input.substring(p1 + 1, p2);
        String dataStr = input.substring(p2 + 1);

        int slaveAddr = strtoul(slaveStr.c_str(), nullptr, 0);
        int regAddr = strtoul(regStr.c_str(), nullptr, 0);
        int dataVal  = strtoul(dataStr.c_str(), nullptr, 0);

        Wire.beginTransmission(slaveAddr);
        Wire.write(regAddr);    // כתובת הרגיסטר
        Wire.write(dataVal);    // הערך לכתיבה
        Wire.endTransmission();

        Serial.print("Wrote 0x");
        Serial.print(dataVal, HEX);
        Serial.print(" to reg 0x");
        Serial.print(regAddr, HEX);
        Serial.print(" at slave 0x");
        Serial.println(slaveAddr, HEX);
      } else {
        Serial.println("Invalid W format. Use W:<slave>:<reg>:<val>");
      }
    }

    else if (input.startsWith("R:")) {
      // Parse: R:<slave_addr>:<reg_addr>:<num_bytes>
      int p1 = input.indexOf(':', 2);
      int p2 = input.indexOf(':', p1 + 1);
      if (p1 > 0 && p2 > p1) {
        String slaveStr = input.substring(2, p1);
        String regStr = input.substring(p1 + 1, p2);
        String lenStr  = input.substring(p2 + 1);

        int slaveAddr = strtoul(slaveStr.c_str(), nullptr, 0);
        int regAddr   = strtoul(regStr.c_str(), nullptr, 0);
        int numBytes  = lenStr.toInt();

        if (numBytes > 0 && numBytes <= BUFFER_SIZE) {
          // שליחת כתובת רגיסטר לפני קריאה
          Wire.beginTransmission(slaveAddr);
          Wire.write(regAddr);
          Wire.endTransmission(false); // חיבור חוזר לקריאה

          Wire.requestFrom(slaveAddr, numBytes);

          Serial.print("Read from 0x");
          Serial.print(slaveAddr, HEX);
          Serial.print(" reg 0x");
          Serial.print(regAddr, HEX);
          Serial.print(": ");

          while (Wire.available()) {
            byte b = Wire.read();
            Serial.print("0x");
            Serial.print(b, HEX);
            Serial.print(" ");
          }
          Serial.println();
        } else {
          Serial.println("Invalid byte count");
        }
      } else {
        Serial.println("Invalid R format. Use R:<slave>:<reg>:<bytes>");
      }
    }

    else if (input.startsWith("S:")) {
      Serial.println("Scanning I2C bus...");
      byte count = 0;
      for (byte address = 1; address < 127; address++) {
        Wire.beginTransmission(address);
        byte error = Wire.endTransmission();
        if (error == 0) {
          Serial.print("I2C device found at address 0x");
          if (address < 16) Serial.print("0");
          Serial.print(address, HEX);
          Serial.println();
          count++;
        }
      }
      if (count == 0) {
        Serial.println("No I2C devices found.");
      } else {
        Serial.print("Scan complete. Found ");
        Serial.print(count);
        Serial.println(" device(s).");
      }
    }

    else {
      Serial.println("Unknown command. Use W:<s>:<r>:<v> or R:<s>:<r>:<n> or S:");
    }
  }
}
