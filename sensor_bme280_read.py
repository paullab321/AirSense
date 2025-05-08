import time
from datetime import datetime
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create BME280 object
bme280 = adafruit_bme280.Adafruit_BME280_I2C(
    i2c, address=0x77)  # Use the detected address


def read_sensor_data():
    """
    Generator function to read sensor data from the BME280 sensor.
    Yields a dictionary containing timestamp, temperature, humidity, and pressure.
    """
    while True:
        # Read sensor data
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Yield the data as a dictionary
        yield {
            "timestamp": timestamp,
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
        }

        # Wait for 1 second before reading again
        time.sleep(1)
