#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEUUID.h>
#include <BLEAdvertisedDevice.h>
#include <BLEBeacon.h>
#include <esp_bt.h> // Include this library to set TX power

BLEScan* pBLEScan;
BLEBeacon id;
int scanTime = 1; // Change this line to set the scan time to 0.5 seconds
bool shouldScan = true; // Add this line to track whether we should scan

String reverse(String str) {
  String rev;
  for (int i = str.length() - 1; i >= 0; i--) {
    rev = rev + str[i];
  } 
  return rev;
}

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks
{
    void onResult(BLEAdvertisedDevice advertisedDevice)
    {
      String deviceName = advertisedDevice.getName().c_str();
      if(deviceName == "MyESP32") {
        Serial.print("Device found: ");
        Serial.println(advertisedDevice.toString().c_str());
        String bUUID = advertisedDevice.getServiceUUID().toString().c_str();
        if (bUUID == "4fafc201-1fb5-459e-8fcc-c5c9c331914b") {
          digitalWrite(2, HIGH);
          digitalWrite(16, HIGH); // Vibrate when MyESP32 is found
          Serial.println("Vibration motor should be ON"); // Debugging message
          shouldScan = false; // Stop scanning
          delay(30000); // Wait for 30 seconds
          digitalWrite(16, LOW); // Stop vibrating after 30 seconds
          Serial.println("Vibration motor should be OFF"); // Debugging message
          shouldScan = true; // Start scanning again
        } else {
          digitalWrite(2, LOW);
          digitalWrite(16, LOW); // Stop vibrating when MyESP32 is not found
          Serial.println("Vibration motor should be OFF"); // Debugging message
        }
      }
    }
};

void setup() {
  Serial.begin(115200);
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);

  // Set the TX power
  esp_ble_tx_power_set(ESP_BLE_PWR_TYPE_ADV, ESP_PWR_LVL_P9); // Set the TX power to maximum

  Serial.println("Scanning...");
  pinMode(2, OUTPUT);
  pinMode(16, OUTPUT); // Add this line to set GPIO16 as output
}

void loop()
{
  if (shouldScan) {
    BLEScanResults foundDevices = pBLEScan->start(scanTime);
    Serial.print("Devices found: ");
    Serial.println(foundDevices.getCount());
    Serial.println("Scan done!");
    pBLEScan->clearResults();
  }
}
