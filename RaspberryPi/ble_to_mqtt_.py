import asyncio
import struct
from bleak import BleakScanner, BleakClient
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_TEMP = "arduino/temperature"
MQTT_TOPIC_HUMIDITY = "arduino/humidity"
MQTT_TOPIC_PRESSURE = "arduino/pressure"
MQTT_TOPIC_ACCEL_X = "arduino/accel/x"
MQTT_TOPIC_ACCEL_Y = "arduino/accel/y"
MQTT_TOPIC_ACCEL_Z = "arduino/accel/z"
MQTT_TOPIC_GYRO_X = "arduino/gyro/x"
MQTT_TOPIC_GYRO_Y = "arduino/gyro/y"
MQTT_TOPIC_GYRO_Z = "arduino/gyro/z"
MQTT_TOPIC_MAG_X = "arduino/mag/x"
MQTT_TOPIC_MAG_Y = "arduino/mag/y"
MQTT_TOPIC_MAG_Z = "arduino/mag/z"

TEMP_UUID = "00002a1c-0000-1000-8000-00805f9b34fb"
HUMIDITY_UUID = "00002a6f-0000-1000-8000-00805f9b34fb"
PRESSURE_UUID = "00002a6d-0000-1000-8000-00805f9b34fb"
ACCEL_X_UUID = "00002a58-0000-1000-8000-00805f9b34fb"
ACCEL_Y_UUID = "00002a59-0000-1000-8000-00805f9b34fb"
ACCEL_Z_UUID = "00002a5a-0000-1000-8000-00805f9b34fb"
GYRO_X_UUID = "00002a5b-0000-1000-8000-00805f9b34fb"
GYRO_Y_UUID = "00002a5c-0000-1000-8000-00805f9b34fb"
GYRO_Z_UUID = "00002a5d-0000-1000-8000-00805f9b34fb"
MAG_X_UUID = "00002a5e-0000-1000-8000-00805f9b34fb"
MAG_Y_UUID = "00002a5f-0000-1000-8000-00805f9b34fb"
MAG_Z_UUID = "00002a60-0000-1000-8000-00805f9b34fb"

mqtt_client = mqtt.Client()

async def main():
    
    print("Connexion au broker MQTT")
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        print("Connecte au MQTT")
    except Exception as e:
        print(f"ERREUR MQTT: {e}")
        return
    
    print("\nRecherche de l'Arduino via BLE")
    devices = await BleakScanner.discover(timeout=10.0)
    arduino_address = None
    
    for device in devices:
        print(f"  Trouve: {device.name} ({device.address})")
        if device.name and "Arduino" in device.name:
            arduino_address = device.address
            print(f"Arduino detecte: {device.name}")
            break
    
    if not arduino_address:
        print("Arduino non trouve")
        mqtt_client.loop_stop()
        return
    
    print(f"\nConnexion BLE a {arduino_address}...")
    try:
        async with BleakClient(arduino_address) as client:
            print("Connecte a l'Arduino via BLE\n")
            print("Reception des donnees")
            
            while True:
                try:
                    temp_bytes = await client.read_gatt_char(TEMP_UUID)
                    humidity_bytes = await client.read_gatt_char(HUMIDITY_UUID)
                    pressure_bytes = await client.read_gatt_char(PRESSURE_UUID)
                    accel_x_bytes = await client.read_gatt_char(ACCEL_X_UUID)
                    accel_y_bytes = await client.read_gatt_char(ACCEL_Y_UUID)
                    accel_z_bytes = await client.read_gatt_char(ACCEL_Z_UUID)
                    gyro_x_bytes = await client.read_gatt_char(GYRO_X_UUID)
                    gyro_y_bytes = await client.read_gatt_char(GYRO_Y_UUID)
                    gyro_z_bytes = await client.read_gatt_char(GYRO_Z_UUID)
                    mag_x_bytes = await client.read_gatt_char(MAG_X_UUID)
                    mag_y_bytes = await client.read_gatt_char(MAG_Y_UUID)
                    mag_z_bytes = await client.read_gatt_char(MAG_Z_UUID)
                    
                    temp = struct.unpack('<f', temp_bytes)[0]
                    humidity = struct.unpack('<f', humidity_bytes)[0]
                    pressure = struct.unpack('<f', pressure_bytes)[0]
                    accel_x = struct.unpack('<f', accel_x_bytes)[0]
                    accel_y = struct.unpack('<f', accel_y_bytes)[0]
                    accel_z = struct.unpack('<f', accel_z_bytes)[0]
                    gyro_x = struct.unpack('<f', gyro_x_bytes)[0]
                    gyro_y = struct.unpack('<f', gyro_y_bytes)[0]
                    gyro_z = struct.unpack('<f', gyro_z_bytes)[0]
                    mag_x = struct.unpack('<f', mag_x_bytes)[0]
                    mag_y = struct.unpack('<f', mag_y_bytes)[0]
                    mag_z = struct.unpack('<f', mag_z_bytes)[0]
                    
                    mqtt_client.publish(MQTT_TOPIC_TEMP, f"{temp:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_HUMIDITY, f"{humidity:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_PRESSURE, f"{pressure:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_ACCEL_X, f"{accel_x:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_ACCEL_Y, f"{accel_y:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_ACCEL_Z, f"{accel_z:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_GYRO_X, f"{gyro_x:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_GYRO_Y, f"{gyro_y:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_GYRO_Z, f"{gyro_z:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_MAG_X, f"{mag_x:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_MAG_Y, f"{mag_y:.2f}")
                    mqtt_client.publish(MQTT_TOPIC_MAG_Z, f"{mag_z:.2f}")
                    
                    print(f"T:{temp:.1f}C H:{humidity:.0f}% P:{pressure:.1f}kPa | A[{accel_x:.2f},{accel_y:.2f},{accel_z:.2f}] G[{gyro_x:.1f},{gyro_y:.1f},{gyro_z:.1f}] M[{mag_x:.0f},{mag_y:.0f},{mag_z:.0f}]")
                    
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"ERREUR lecture: {e}")
                    break
                    
    except Exception as e:
        print(f"ERREUR BLE: {e}")
    
    mqtt_client.loop_stop()
    print("\nArret : BLE to MQTT bridge")

if __name__ == "__main__":
    asyncio.run(main())