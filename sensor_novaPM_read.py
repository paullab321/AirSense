import serial
import struct
import time
from datetime import datetime


def read_sensor_data():
    while True:
        try:
            ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=2)
            print("NovaPM sensor connected.")
        except serial.SerialException as e:
            print(
                f"Error initializing NovaPM sensor: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            continue

        try:
            while True:
                # Read 10 bytes from the sensor
                data = ser.read(10)

                # Check if the data packet is valid
                if len(data) == 10 and data[0] == 0xAA and data[1] == 0xC0 and data[9] == 0xAB:
                    # Extract PM2.5 and PM10 values
                    pm25 = struct.unpack('<H', data[2:4])[0] / 10.0
                    pm10 = struct.unpack('<H', data[4:6])[0] / 10.0

                    # Yield the values as a dictionary
                    yield {"timestamp": datetime.now(), "pm2.5": pm25, "pm10": pm10}

                # Wait 1 second before the next reading
                time.sleep(1)
        except serial.SerialException as e:
            print(f"Error reading from NovaPM sensor: {e}. Reconnecting...")
        except KeyboardInterrupt:
            print("Exiting...")
            break
        finally:
            ser.close()
