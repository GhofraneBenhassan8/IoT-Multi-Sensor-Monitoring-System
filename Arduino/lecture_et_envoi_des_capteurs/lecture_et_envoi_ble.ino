#include <ArduinoBLE.h>
#include <Arduino_BMI270_BMM150.h>
#include <Arduino_HS300x.h>
#include <Arduino_LPS22HB.h>

BLEService sensorService("180C");

BLEFloatCharacteristic tempChar("2A1C", BLERead | BLENotify);
BLEFloatCharacteristic humidityChar("2A6F", BLERead | BLENotify);
BLEFloatCharacteristic pressureChar("2A6D", BLERead | BLENotify);
BLEFloatCharacteristic accelXChar("2A58", BLERead | BLENotify);
BLEFloatCharacteristic accelYChar("2A59", BLERead | BLENotify);
BLEFloatCharacteristic accelZChar("2A5A", BLERead | BLENotify);
BLEFloatCharacteristic gyroXChar("2A5B", BLERead | BLENotify);
BLEFloatCharacteristic gyroYChar("2A5C", BLERead | BLENotify);
BLEFloatCharacteristic gyroZChar("2A5D", BLERead | BLENotify);
BLEFloatCharacteristic magXChar("2A5E", BLERead | BLENotify);
BLEFloatCharacteristic magYChar("2A5F", BLERead | BLENotify);
BLEFloatCharacteristic magZChar("2A60", BLERead | BLENotify);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("ERREUR IMU");
    while (1);
  }

  if (!HS300x.begin()) {
    Serial.println("ERREUR temperature et humidite");
    while (1);
  }

  if (!BARO.begin()) {
    Serial.println("ERREUR pression");
    while (1);
  }

  if (!BLE.begin()) {
    Serial.println("ERREUR BLE");
    while (1);
  }

  BLE.setLocalName("Arduino_Nano33");
  BLE.setAdvertisedService(sensorService);
  
  sensorService.addCharacteristic(tempChar);
  sensorService.addCharacteristic(humidityChar);
  sensorService.addCharacteristic(pressureChar);
  sensorService.addCharacteristic(accelXChar);
  sensorService.addCharacteristic(accelYChar);
  sensorService.addCharacteristic(accelZChar);
  sensorService.addCharacteristic(gyroXChar);
  sensorService.addCharacteristic(gyroYChar);
  sensorService.addCharacteristic(gyroZChar);
  sensorService.addCharacteristic(magXChar);
  sensorService.addCharacteristic(magYChar);
  sensorService.addCharacteristic(magZChar);
  
  BLE.addService(sensorService);
  
  tempChar.writeValue(0.0);
  humidityChar.writeValue(0.0);
  pressureChar.writeValue(0.0);
  accelXChar.writeValue(0.0);
  accelYChar.writeValue(0.0);
  accelZChar.writeValue(0.0);
  gyroXChar.writeValue(0.0);
  gyroYChar.writeValue(0.0);
  gyroZChar.writeValue(0.0);
  magXChar.writeValue(0.0);
  magYChar.writeValue(0.0);
  magZChar.writeValue(0.0);
  
  BLE.advertise();
  Serial.println();
  Serial.println("Le BLE est actif et en attente de connexion");
  Serial.println();
}

void loop() {
  BLEDevice central = BLE.central();
  
  if (central) {
    Serial.print("Connecte a: ");
    Serial.println(central.address());
    
    while (central.connected()) {
      float temperature = HS300x.readTemperature();
      float humidity = HS300x.readHumidity();
      float pressure = BARO.readPressure();
      
      float accelX = 0, accelY = 0, accelZ = 0;
      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(accelX, accelY, accelZ);
      }
      
      float gyroX = 0, gyroY = 0, gyroZ = 0;
      if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(gyroX, gyroY, gyroZ);
      }
      
      float magX = 0, magY = 0, magZ = 0;
      if (IMU.magneticFieldAvailable()) {
        IMU.readMagneticField(magX, magY, magZ);
      }
      
      tempChar.writeValue(temperature);
      humidityChar.writeValue(humidity);
      pressureChar.writeValue(pressure);
      accelXChar.writeValue(accelX);
      accelYChar.writeValue(accelY);
      accelZChar.writeValue(accelZ);
      gyroXChar.writeValue(gyroX);
      gyroYChar.writeValue(gyroY);
      gyroZChar.writeValue(gyroZ);
      magXChar.writeValue(magX);
      magYChar.writeValue(magY);
      magZChar.writeValue(magZ);
      
      Serial.print("T:"); Serial.print(temperature, 1);
      Serial.print("C H:"); Serial.print(humidity, 0);
      Serial.print("% P:"); Serial.print(pressure, 1);
      Serial.print("kPa Accel X:"); Serial.print(accelX, 2);
      Serial.print(" Y:"); Serial.print(accelY, 2);
      Serial.print(" Z:"); Serial.print(accelZ, 2);
      Serial.print(" Gyro X:"); Serial.print(gyroX, 1);
      Serial.print(" Y:"); Serial.print(gyroY, 1);
      Serial.print(" Z:"); Serial.print(gyroZ, 1);
      Serial.print(" Mag X:"); Serial.print(magX, 1);
      Serial.print(" Y:"); Serial.print(magY, 1);
      Serial.print(" Z:"); Serial.println(magZ, 1);
      
      delay(1000);
    }
    
    Serial.println("Deconnecte");
  }
}