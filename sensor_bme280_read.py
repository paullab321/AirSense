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
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append the data to the lists
        timestamps.append(timestamp)
        temperatures.append(temperature)
        humidities.append(humidity)
        pressures.append(pressure)

        # Print the data to the console
        print(
            f"Timestamp: {timestamp}, Temperature: {temperature:.2f} °C, Humidity: {humidity:.2f} %, Pressure: {pressure:.2f} hPa"
        )

        # Wait for 1 second before reading again
        time.sleep(1)


def save_sensor_data_to_file(filename="sensor_data.txt"):
    # Save the data to a file when the loop ends
    with open(filename, "w") as file:
        for i in range(len(timestamps)):
            file.write(
                f"{timestamps[i]}, {temperatures[i]:.2f}, {humidities[i]:.2f}, {pressures[i]:.2f}\n"
            )
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    try:
        read_sensor_data()
    except KeyboardInterrupt:
        running = False  # Stop the loop when Ctrl+C is pressed
        print("Stopping sensor data collection...")
    finally:
        print("Program terminated.")

        # Call the function to save data
        save_sensor_data_to_file()
