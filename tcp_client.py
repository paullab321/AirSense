import socket
import plotter
import json
from datetime import datetime


def start_client(host='192.168.178.156', port=65432):
    """
    Connects to the TCP server on the Raspberry Pi and receives sensor data.
    :param host: The IP address of the Raspberry Pi.
    :param port: The port to connect to.
    """
    def data_source():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            try:
                while True:
                    data = client_socket.recv(1024).decode('utf-8').strip()
                    if not data:
                        break

                    # Parse the JSON data
                    for line in data.split("\n"):
                        if line.strip():
                            sensor_data = json.loads(line)
                            print(sensor_data)  # Print the parsed data
                            try:
                                timestamp = datetime.fromisoformat(
                                    sensor_data["timestamp"])
                                if sensor_data["sensor"] == "NovaPM":
                                    yield {
                                        "timestamp": timestamp,
                                        "pm2.5": sensor_data["data"]["pm2.5"],
                                        "pm10": sensor_data["data"]["pm10"]
                                    }
                                elif sensor_data["sensor"] == "BME280":
                                    yield {
                                        "timestamp": timestamp,
                                        "temperature": sensor_data["data"]["temperature"],
                                        "humidity": sensor_data["data"]["humidity"],
                                        "pressure": sensor_data["data"]["pressure"]
                                    }
                            except (KeyError, ValueError) as e:
                                print(
                                    f"Failed to parse data: {sensor_data} ({e})")
            except KeyboardInterrupt:
                print("Client shutting down.")

    # Pass the data source to the plotter
    plotter.plot_sensor_data(data_source())


if __name__ == "__main__":
    # Replace 'raspberry-pi-ip' with the actual IP
    start_client(host='192.168.178.156', port=65432)
