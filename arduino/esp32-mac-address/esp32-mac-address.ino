/*
 * Description: Using this sketch you can get your Arduino mac address through Serial Monitor.
 *              The mac address can be used for connection to the IoT-network.
 *              Prints the mac address every 5 seconds in the Serial Monitor.
 *              Serial speed: 9600
 * Author:  Mats Otten
 * Date:    8 sep 2021
 * Updated 22 oct 2024; changed the code to work with the ESP32.
 * Updated 26 sep 2025; changed to esp_wifi_get_mac()-function, which works with a larger amount of different esp32 boards. 
 */

 #include <WiFi.h>
 #include <esp_wifi.h>
 
 void setup() {
   Serial.begin(9600);
   WiFi.mode(WIFI_STA);
   WiFi.STA.begin();
 }
 
 void loop() {
   uint8_t macAddress[6] = {};
   esp_err_t response = esp_wifi_get_mac(WIFI_IF_STA, macAddress);
 
   if(response == ESP_OK) {
     Serial.printf("MAC-address of your ESP32: %02X:%02X:%02X:%02X:%02X:%02X\n", macAddress[0], macAddress[1], macAddress[2], macAddress[3], macAddress[4], macAddress[5], macAddress[6]);
   } else {
     Serial.println("Failed to read the MAC-address of your ESP32.");
   }
   delay(5000);
 }