import smbus2
import bme280
import time
from datetime import datetime

adress = 0x76  # I2C address of the BME280 sensor

# Create an I2C bus object (1 for Raspberry Pi 3 and later)
bus = smbus2.SMBus(1)
calibration_params = bme280.load_calibration_params(
    bus, adress)  # Load calibration parameters

sensor = bme280.BME280(i2c_dev=bus, address=adress)  # Create a BME280 object

# Create lists to store historical data
timestamps = []
temperatures = []
humidities = []
pressures = []

running = True

# Function to read sensor data and store it in lists


def read_sensor_data():
    global running
    while running:
        # Read sensor data
        data = sensor.get_data()
        temperature = data.temperature
        humidity = data.humidity
        pressure = data.pressure

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append the data to the lists
        timestamps.append(timestamp)
        temperatures.append(temperature)
        humidities.append(humidity)
        pressures.append(pressure)

        # Print the data to the console
        print(
            f"Timestamp: {timestamp}, Temperature: {temperature:.2f} °C, Humidity: {humidity:.2f} %, Pressure: {pressure:.2f} hPa")

        # Wait for 1 second before reading again
        time.sleep(1)


def save_sensor_data_to_file(filename="sensor_data.txt"):
    # Save the data to a file when the loop ends on a debian environment
    with open(filename, "w") as file:
        for i in range(len(timestamps)):
            file.write(
                f"{timestamps[i]}, {temperatures[i]:.2f}, {humidities[i]:.2f}, {pressures[i]:.2f}\n")
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    try:
        read_sensor_data()
    except KeyboardInterrupt:
        running = False  # Stop the loop when Ctrl+C is pressed
        print("Stopping sensor data collection...")
    finally:
        bus.close()  # Close the I2C bus when done
        print("I2C bus closed.")

        print("Program terminated.")

        # Call the function to save data
        save_sensor_data_to_file()
