# IoT Multi-Sensor Monitoring System

A complete IoT monitoring system that collects data from 12 sensors via Bluetooth Low Energy (BLE), transmits it through MQTT, stores it in a time-series database, and visualizes it in real-time.

## Project Overview

This project implements a hierarchical IoT architecture that captures environmental and motion data from an Arduino Nano 33 BLE Sense Rev2, processes it through a Raspberry Pi 4 gateway, and provides real-time visualization through a Node-RED dashboard.

### System Architecture

```
Arduino Nano 33 BLE ──[BLE]──> Raspberry Pi 4 ──[MQTT]──> InfluxDB
                                      │
                                      └──[HTTP]──> Node-RED Dashboard
```

## Hardware Components

- **Arduino Nano 33 BLE Sense Rev2**: Multi-sensor acquisition board with 12 integrated sensors
- **Raspberry Pi 4**: Central gateway and server
- **Power supplies** for both devices

## Sensors & Data Collected

| Category | Sensors | Units |
|----------|---------|-------|
| **Environment** | Temperature, Humidity, Pressure | °C, %, kPa |
| **Accelerometer** | X, Y, Z axes | m/s² |
| **Gyroscope** | X, Y, Z axes | deg/s |
| **Magnetometer** | X, Y, Z axes | µT |

**Total: 12 simultaneous data streams**

## Technology Stack

### Arduino
- **Language**: C++ (Arduino Framework)
- **Libraries**: 
  - ArduinoBLE
  - Arduino_BMI270_BMM150 (IMU)
  - Arduino_HS300x (Temperature/Humidity)
  - Arduino_LPS22HB (Pressure)

### Raspberry Pi
- **Language**: Python 3
- **Key Libraries**: 
  - `bleak` (BLE communication)
  - `paho-mqtt` (MQTT client)
- **Services**:
  - Mosquitto MQTT Broker
  - Node-RED
  - InfluxDB

## Project Structure

```
.
├── Arduino/
│   ├── lecture_et_envoi_ble/
│   │   ├── lecture_et_envoi_ble.ino
├── RaspberryPi/
│   ├── ble_to_mqtt_.py
│   └── requirements.txt
├── docs/
│   └── Dashboard.png
│   └── donnees_capteurs.csv
│   └── envoi_arduino.png
│   └── flows.json
│   └── NodeRed.png
│   └── reception_raspberry.png
```

## Installation & Setup

### 1. Arduino Setup

1. Install [Arduino IDE](https://www.arduino.cc/en/software) or Arduino CLI
2. Install required board: Arduino Mbed OS Nano Boards
3. Install required libraries via Library Manager:
   - ArduinoBLE
   - Arduino_BMI270_BMM150
   - Arduino_HS300x
   - Arduino_LPS22HB
4. Upload `lecture_et_envoi_des_capteurs.ino` to your Arduino Nano 33 BLE

### 2. Raspberry Pi Setup

#### Install System Dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-pip mosquitto mosquitto-clients
```

#### Install InfluxDB
```bash
wget -q https://repos.influxdata.com/influxdata-archive_compat.key
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
sudo apt update && sudo apt install -y influxdb
sudo systemctl start influxdb
sudo systemctl enable influxdb
```

#### Install Node-RED
```bash
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
sudo systemctl start nodered
sudo systemctl enable nodered
```

#### Install Python Dependencies
```bash
cd RaspberryPi
pip3 install -r requirements.txt
```

### 3. Configure InfluxDB

```bash
influx
> CREATE DATABASE donnees_capteurs_arduino
> exit
```

### 4. Configure Node-RED

1. Access Node-RED at `http://<raspberry-pi-ip>:1880`
2. Install required nodes:
   - node-red-dashboard
   - node-red-contrib-influxdb
3. Import the flow configuration (create flows with MQTT In nodes for each topic)
4. Configure InfluxDB connection in Node-RED

## Running the System

### Start Mosquitto Broker
```bash
sudo systemctl start mosquitto
```

### Start the BLE to MQTT Bridge
```bash
cd RaspberryPi
python3 ble_to_mqtt_.py
```

The script will:
1. Connect to the MQTT broker
2. Scan for the Arduino device
3. Establish BLE connection
4. Read sensor data every second
5. Publish to MQTT topics

### Access the Dashboard
Navigate to `http://<raspberry-pi-ip>:1880/ui`

## MQTT Topics

The system publishes to the following topics:

```
arduino/temperature
arduino/humidity
arduino/pressure
arduino/accel/x
arduino/accel/y
arduino/accel/z
arduino/gyro/x
arduino/gyro/y
arduino/gyro/z
arduino/mag/x
arduino/mag/y
arduino/mag/z
```

## BLE Characteristics (UUIDs)

| Sensor      | UUID |
|-------------|------|
| Temperature | 00002a1c-0000-1000-8000-00805f9b34fb |
| Humidity    | 00002a6f-0000-1000-8000-00805f9b34fb |
| Pressure    | 00002a6d-0000-1000-8000-00805f9b34fb |
| Accel X/Y/Z | 00002a58/59/5a-0000-1000-8000-00805f9b34fb |
| Gyro X/Y/Z  | 00002a5b/5c/5d-0000-1000-8000-00805f9b34fb |
| Mag X/Y/Z   | 00002a5e/5f/60-0000-1000-8000-00805f9b34fb |

## Features

- Real-time data acquisition from 12 sensors
- Low-power BLE communication
- MQTT publish/subscribe architecture
- Time-series data storage in InfluxDB
- Live dashboard with gauges and charts
- Historical data analysis capability
- CSV export support

## Troubleshooting

### Arduino not detected
- Ensure BLE is enabled on Arduino (check serial monitor)
- Verify Arduino name is "Arduino_Nano33"
- Check Bluetooth is enabled on Raspberry Pi: `sudo systemctl status bluetooth`

### MQTT connection issues
- Verify Mosquitto is running: `sudo systemctl status mosquitto`
- Check MQTT topics: `mosquitto_sub -t "arduino/#" -v`

### BLE connection errors
- Ensure only one device is connected to Arduino at a time
- Try restarting the BLE service: `sudo systemctl restart bluetooth`
- Check Python dependencies are installed correctly

**Academic Year**: 2025/2026  
**Supervised by**: Mr. Khaled Jelassi

## License

This project was developed as part of an academic course on Local Networks.
