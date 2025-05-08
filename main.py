import sensor_novaPM_read
import sensor_bme280_read
import tcp_server
import threading


# Function to save the data to a file
def save_data_to_file(data, file):
    file.write(f"{data['timestamp']}, {data}\n")


# Function to format and save sensor data
def process_and_save_sensor_data(data_source_novaPM, data_source_bme280, filename="sensor_data.txt"):
    with open(filename, "a") as file:
        while True:
            try:
                # Get NovaPM data
                novaPM_data = next(data_source_novaPM)
                # Get BME280 data
                bme280_data = next(data_source_bme280)

                # Format the data
                formatted_data = {
                    "timestamp": novaPM_data["timestamp"],
                    "pm2.5": novaPM_data["pm2.5"],
                    "pm10": novaPM_data["pm10"],
                    "temperature": bme280_data["temperature"],
                    "humidity": bme280_data["humidity"],
                    "pressure": bme280_data["pressure"],
                }

                # Save to file
                save_data_to_file(formatted_data, file)
                print(f"Saved data: {formatted_data}")

            except StopIteration:
                print("One of the data sources has stopped producing data.")
                break
            except Exception as e:
                print(f"Error processing sensor data: {e}")


# Function to start the server in a separate thread
def start_server_thread():
    server_thread = threading.Thread(
        target=tcp_server.start_server, daemon=True)
    server_thread.start()
    print("TCP server started in a separate thread.")


def main():
    # Start the TCP server
    start_server_thread()

    # Initialize data sources
    data_source_novaPM = sensor_novaPM_read.read_sds011()
    data_source_bme280 = sensor_bme280_read.read_sensor_data()

    # Process and save sensor data
    process_and_save_sensor_data(data_source_novaPM, data_source_bme280)


if __name__ == "__main__":
    main()
