import socket
import plotter
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
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    # Parse the received data
                    decoded_data = data.decode('utf-8').strip()
                    try:
                        # Assuming the data format is: "timestamp, PM2.5: value µg/m³, PM10: value µg/m³"
                        parts = decoded_data.split(", ")
                        timestamp = datetime.strptime(
                            parts[0], "%Y-%m-%d %H:%M:%S.%f")
                        pm25 = float(parts[1].split(": ")[1].split(" ")[0])
                        pm10 = float(parts[2].split(": ")[1].split(" ")[0])

                        yield {"timestamp": timestamp, "pm2.5": pm25, "pm10": pm10}
                    except (IndexError, ValueError) as e:
                        print(f"Failed to parse data: {decoded_data} ({e})")
            except KeyboardInterrupt:
                print("Client shutting down.")

    # Pass the data source to the plotter
    plotter.plot_sensor_data(data_source())


if __name__ == "__main__":
    # Replace 'raspberry-pi-ip' with the actual IP
    start_client(host='192.168.178.156', port=65432)
